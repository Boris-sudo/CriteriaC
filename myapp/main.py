"""Импорты"""
import math
import pygame
import time
import cv2
import numpy
import struct
"""Параметры"""
from lib.parameters import *
from lib.labirint_generator import generate_labyrinth
from lib.input import *
from lib.imagebutton import *

"""Функции"""
##########Рисование лабиринта
def draw_labyrinth(matrix, start, finish):
    width = (len(matrix) // 2 + 1) * WIDTH_LINE + (len(matrix) // 2) * WIDTH_WALL + WIDTH_BORDER * 2
    height = (len(matrix[0]) // 2 + 1) * WIDTH_LINE + (len(matrix[0]) // 2) * WIDTH_WALL + WIDTH_BORDER * 2

    for i in range(width):
        for j in range(height):
            if i < WIDTH_BORDER or width - i <= WIDTH_BORDER or j < WIDTH_BORDER or height - j <= WIDTH_BORDER:  # отображение границ лабиринта
                pygame.draw.line(window, COLOR_WALL, [i, j], [i, j], 1)
            else:
                if (i - WIDTH_BORDER) % (WIDTH_LINE + WIDTH_WALL) <= WIDTH_LINE:
                    x = (i - WIDTH_BORDER) // (WIDTH_LINE + WIDTH_WALL) * 2
                else:
                    x = (i - WIDTH_BORDER) // (WIDTH_LINE + WIDTH_WALL) * 2 + 1
                if (j - WIDTH_BORDER) % (WIDTH_LINE + WIDTH_WALL) <= WIDTH_LINE:
                    y = (j - WIDTH_BORDER) // (WIDTH_LINE + WIDTH_WALL) * 2
                else:
                    y = (j - WIDTH_BORDER) // (WIDTH_LINE + WIDTH_WALL) * 2 + 1
                if matrix[x][y]:
                    pygame.draw.line(window, COLOR_WAY, [i, j], [i, j], 1)
                else:
                    pygame.draw.line(window, COLOR_WALL, [i, j], [i, j], 1)


def new_game():
    global record_time, start_time, player, matrix, start, finish, matrix_base
    window.fill((0, 0, 0))
    pygame.draw.rect(window, (0, 0, 0), (0, HEIGHT_WINDOW - 70, WIDTH_WINDOW, 70))
    matrix, start, finish = generate_labyrinth(WIDTH, HEIGHT)
    k = 0

    while matrix in matrix_base or start[0] == finish[0] or start[1] == finish[1]:
        matrix, start, finish = generate_labyrinth(WIDTH, HEIGHT)
        k += 1
        if k > 20:
            print('Не найдено лабиринтов без повторения')
            break

    matrix_base.append(matrix)
    draw_labyrinth(matrix, start, finish)


def tick():
    """Cекудномер"""
    global start_time, t
    t = time.time() - start_time


def check(v, g):
    n, m = len(g), len(g[0])
    return 0 <= v[0] < n and 0 <= v[1] < m


def get_path(start, finish, g):
    used = [[False] * len(g[0]) for i in range(len(g))]
    direction = [[0] * len(g[0]) for i in range(len(g))]
    queue = [start]

    while len(queue) != 0:
        v = queue[0]
        queue.remove(queue[0])
        used[v[0]][v[1]] = True
        for i in range(4):
            to = [v[0] + dx[i], v[1] + dy[i]]
            if check(to, g) and not used[to[0]][to[1]] and g[to[0]][to[1]]:
                queue.append(to)
                direction[to[0]][to[1]] = v

    path = [finish]
    v = finish
    while v != start:
        v = direction[v[0]][v[1]]
        path.append(v)
    path.reverse()
    return path


def find_max_way(x, y, g, used):
    used[x][y] = True
    result = 0
    for i in range(4):
        to_x, to_y = x + dx[i], y + dy[i]
        if check([to_x, to_y], g) and g[to_x][to_y] and not used[to_x][to_y]:
            result = max(result, find_max_way(to_x, to_y, g, used))
    if (x + y) % 2 == 0:
        return result + 1
    return result


def max_way_in_labyrinth(g):
    max_way, n, m = 0, len(g), len(g[0])
    for x in range(n):
        for y in range(m):
            if (x + y) % 2 == 0:
                count = 0
                for k in range(4):
                    if check([x + dx[k], y + dy[k]], g) and g[x+dx[k]][y+dy[k]]:
                        count += 1
                if count == 1:
                    used = [[False] * m for i in range(n)]
                    max_way = max(max_way, find_max_way(x, y, g, used))
    return max_way


def get_cords(x, y):
    cord_x = WIDTH_BORDER + x / 2 * (WIDTH_LINE + WIDTH_WALL) + 20
    cord_y = WIDTH_BORDER + y / 2 * (WIDTH_LINE + WIDTH_WALL) + 20
    return [cord_x, cord_y]


def draw_path(surface, matrix, start, finish):
    way = get_path(start, finish, matrix)
    prev = way[0]
    way_length = 1
    for i in range(1, len(way)):
        if i % 2 == 0:
            s = get_cords(prev[0], prev[1])
            f = get_cords(way[i][0], way[i][1])
            prev = way[i]
            pygame.draw.line(surface, BLUE, s, f)
            way_length += 1
    return way_length


def get_text(count):
    if 1 <= count <= 2:
        return "клетка"
    if 3 <= count <= 4:
        return "клетки"
    if 5 <= count:
        return "клеток"


def is_valid(x, y, matrix):
    n = len(matrix)
    m = len(matrix[0])
    return 0 <= 2 * x <= n and 0 <= 2 * y <= m


def to_16(s):
    if type(s) == str:
        s = int(s, 2)
    s16 = hex(s)[2:]
    if len(s16) % 2 == 1:
        s16 = '0' + s16
    res = ""
    for i in range(len(s16)):
        if i != 0 and i % 2 == 0:
            res += ' '
        res += s16[i]
    return res

"""Переменные"""
info = True
t = 0
matrix_base = []
"""Инициализация pygame"""
pygame.init()
window = pygame.display.set_mode((WIDTH_WINDOW, HEIGHT_WINDOW))
pygame.display.set_caption("Лабиринт")
"""Переменные pygame"""
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 30)
# тексты
StartTextArray = ["Всем привет, это просто строитель лабиринтов",
                  "Hello everyone, it is just a labyrinth builder"]
StartText = font.render(StartTextArray[language], True, WHITE)
StartTextRect = StartText.get_rect()
StartTextRect.center = [WIDTH_WINDOW / 2, 50]
AboutTextArray = ["сначала введите значение для width, потом нажмите Enter и введите значение для Height",
                  "first enter a value for width, then press Enter and enter a value for Height"]
AboutText = small_font.render(AboutTextArray[language], True, WHITE)
AboutTextRect = StartText.get_rect()
AboutTextRect.center = [WIDTH_WINDOW / 2 - 50, 450]
# инпуты
InputWidth = Input(100, 500, ["Длинна: ", "Width: "])
InputHeight = Input(100, 600, ["Высота: ", "Height: "])
# кнопки
StartButton = StartButton(1000, 300, window)
SettingsButton = ImageButton(WIDTH_WINDOW, HEIGHT_WINDOW, window, settingsIcon)
OutButton = ImageButton(WIDTH_WINDOW, HEIGHT_WINDOW, window, crossIcon)
ChangeLanguageButton = ImageButton(300, 300, window, changeLanguageIcon)
SafeButton = ImageButton(60, 790, window, safeIcon)
"""Динамичные переменные"""
matrix = []
flag_game = True  # основной цикл игры
game_status = 0  # различные под циклы
status_input = ""
# 0 - меню
# 1 - выбор лабиринта
# 2 - настройки

start = (0, 0)
finish = (0, 0)
position_start = DEFAULT_CORDS
position_finish = DEFAULT_CORDS
start_time = time.time()
max_length = 0
length = -1
image_count=0
"""Основной цикл игры"""
while flag_game:
    window.fill(BLACK)
    while game_status == 0:
        pos = pygame.mouse.get_pos()
        window.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag_game = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pass
                if event.key == pygame.K_1:
                    if status_input == "width":
                        InputWidth.add("1")
                    elif status_input == "height":
                        InputHeight.add("1")
                if event.key == pygame.K_2:
                    if status_input == "width":
                        InputWidth.add("2")
                    elif status_input == "height":
                        InputHeight.add("2")
                if event.key == pygame.K_3:
                    if status_input == "width":
                        InputWidth.add("3")
                    elif status_input == "height":
                        InputHeight.add("3")
                if event.key == pygame.K_4:
                    if status_input == "width":
                        InputWidth.add("4")
                    elif status_input == "height":
                        InputHeight.add("4")
                if event.key == pygame.K_5:
                    if status_input == "width":
                        InputWidth.add("5")
                    elif status_input == "height":
                        InputHeight.add("5")
                if event.key == pygame.K_6:
                    if status_input == "width":
                        InputWidth.add("6")
                    elif status_input == "height":
                        InputHeight.add("6")
                if event.key == pygame.K_7:
                    if status_input == "width":
                        InputWidth.add("7")
                    elif status_input == "height":
                        InputHeight.add("7")
                if event.key == pygame.K_8:
                    if status_input == "width":
                        InputWidth.add("8")
                    elif status_input == "height":
                        InputHeight.add("8")
                if event.key == pygame.K_9:
                    if status_input == "width":
                        InputWidth.add("9")
                    elif status_input == "height":
                        InputHeight.add("9")
                if event.key == pygame.K_0:
                    if status_input == "width":
                        InputWidth.add("0")
                    elif status_input == "height":
                        InputHeight.add("0")
                if event.key == pygame.K_BACKSPACE:
                    if status_input == "width":
                        InputWidth.delete()
                    elif status_input == "height":
                        InputHeight.delete()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if StartButton.on_click(pos):
                    if InputWidth.is_void() or InputHeight.is_void():
                        StartButton.change_color(RED, t)
                    else:
                        WIDTH = InputWidth.get_number()
                        HEIGHT = InputHeight.get_number()
                        recalc_window_size()
                        game_status = 1
                if InputWidth.on_click(pos):
                    status_input = "width"
                if InputHeight.on_click(pos):
                    status_input = "height"
                if SettingsButton.on_click(pos):
                    game_status = 2
        """Рисование отдельных элементов"""
        # Text
        window.blit(StartText, StartTextRect)
        window.blit(AboutText, AboutTextRect)
        # Input
        InputWidth.draw(window)
        InputHeight.draw(window)
        # Buttons
        StartButton.on_hover(pos, t)
        StartButton.draw(window)
        SettingsButton.draw(window)
        """Функции pygame"""
        tick()
        pygame.display.update()

    while game_status == 1:  # основной игровой цикл
        window.fill((0, 0, 0))
        pos = pygame.mouse.get_pos()
        if start == finish:
            pygame.draw.rect(window, (0, 0, 0), (0, HEIGHT_WINDOW - 70, WIDTH_WINDOW, 70))
            matrix, start, finish = generate_labyrinth(WIDTH, HEIGHT)
            k = 0
            while matrix in matrix_base or start[0] == finish[0] or start[1] == finish[1]:
                matrix, start, finish = generate_labyrinth(WIDTH, HEIGHT)
                k += 1
                if k > 20:
                    print('Не найдено лабиринтов без повторения')
                    break
            max_length = max_way_in_labyrinth(matrix)
            matrix_base.append(matrix)
        """Отрисовка"""
        # Лабиринт
        draw_labyrinth(matrix, start, finish)
        # Кнопки
        SafeButton.draw(window)
        # Круги на старте и финише
        pygame.draw.circle(window, PURPLE, radius=10,
                           center=[(WIDTH_BORDER + position_start[0] * (WIDTH_LINE + WIDTH_WALL)) + 20,
                                   (WIDTH_BORDER + position_start[1] * (WIDTH_LINE + WIDTH_WALL)) + 20])
        pygame.draw.circle(window, PURPLE, radius=10,
                           center=[(WIDTH_BORDER + position_finish[0] * (WIDTH_LINE + WIDTH_WALL)) + 20,
                                   (WIDTH_BORDER + position_finish[1] * (WIDTH_LINE + WIDTH_WALL)) + 20])
        if position_finish != DEFAULT_CORDS:
            pos_s = (position_start[0] * 2, position_start[1] * 2)
            pos_f = (position_finish[0] * 2, position_finish[1] * 2)
            length = draw_path(window, matrix, pos_s, pos_f)
            length_text = get_text(length)
            lengthText = font.render("{} {}, хотя самый длинный {}".format(length, length_text, max_length), True,
                                     WHITE)
            lengthTextRect = lengthText.get_rect()
            lengthTextRect.center = [WIDTH_WINDOW / 2 - 50, 750]
            window.blit(lengthText, lengthTextRect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag_game = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_status = 0
                if event.key == pygame.K_r:
                    new_game()
                    max_length = max_way_in_labyrinth(matrix)
                if event.key == pygame.K_ESCAPE:
                    position_finish = DEFAULT_CORDS
                    position_start = DEFAULT_CORDS
                if event.key == pygame.K_KP_ENTER:
                    pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos_x = (pos[0] - WIDTH_BORDER) // (WIDTH_WALL + WIDTH_LINE)
                pos_y = (pos[1] - WIDTH_BORDER) // (WIDTH_WALL + WIDTH_LINE)
                if position_start == DEFAULT_CORDS and is_valid(pos_x, pos_y, matrix):
                    position_start = [pos_x, pos_y]
                elif position_finish == DEFAULT_CORDS and is_valid(pos_x, pos_y, matrix):
                    position_finish = [pos_x, pos_y]
                if SafeButton.on_click(pos):
                    pygame.image.save(window, "myapp\static\screen-images\image{}.png".format(image_count))
                    view = pygame.surfarray.array3d(window)
                    view = view.transpose([1, 0, 2])
                    img_bgr = cv2.cvtColor(view, cv2.COLOR_RGB2BGR)
                    img_bgr = img_bgr[:-85]
                    cv2.imshow("image{}".format(image_count), img_bgr)
                    filename = "myapp\static\mazes\maze{}.kiva".format(image_count)
                    new_maze = open(filename, "w+")
                    format_name = 'kiva'
                    for i in format_name:
                        new_maze.write(hex(ord(i))[2:] + ' ')
                    new_maze.write(to_16(WIDTH*2-1) + ' ' + to_16(HEIGHT*2-1))
                    matrix_string = ""
                    for i in matrix:
                        for j in i:
                            matrix_string = matrix_string + ("0" if j else "1")
                        new_maze.write(' ' + to_16(matrix_string))
                        matrix_string = ""
                    new_maze.write(matrix_string)
                    image_count += 1
        tick()
        pygame.display.update()

    while game_status == 2:
        pos = pygame.mouse.get_pos()
        window.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag_game = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if OutButton.on_click(pos):
                    game_status = 0
                if ChangeLanguageButton.on_click(pos):
                    StartButton.change_language()
                    InputWidth.change_language()
                    InputHeight.change_language()
                    language = (language + 1) % 2
                    StartText = font.render(StartTextArray[language], True, WHITE)
                    AboutText = small_font.render(AboutTextArray[language], True, WHITE)
        """Рисование отдельных элементов"""
        # Text
        # Buttons
        OutButton.draw(window)
        ChangeLanguageButton.draw(window)
        """Функции pygame"""
        tick()
        pygame.display.update()
