import random


def start_point_generate(n, m):
    """Функция выбора точки начала лабиринта"""
    if random.choice([True, False]):
        if random.choice([True, False]):
            start = (0, random.randint(0, m - 1))
        else:
            start = (n - 1, random.randint(0, m - 1))
    else:
        if random.choice([True, False]):
            start = (random.randint(0, n - 1), 0)
        else:
            start = (random.randint(0, n - 1), m - 1)
    return start


def finish_point_generate(start, n, m):
    """Выбор точки конца лабиринта"""
    return n - 1 - start[0], m - 1 - start[1]


def vertical_choise(x, y, g):
    """Функция выбора дальнейшего пути в генерации лабиринта"""
    choice_list = []
    if x > 0:
        if not g[x - 1][y]:
            choice_list.append((x - 1, y))
    if x < len(g) - 1:
        if not g[x + 1][y]:
            choice_list.append((x + 1, y))
    if y > 0:
        if not g[x][y - 1]:
            choice_list.append((x, y - 1))
    if y < len(g[0]) - 1:
        if not g[x][y + 1]:
            choice_list.append((x, y + 1))

    if choice_list:
        nx, ny = random.choice(choice_list)
        if x == nx:
            if ny > y:
                tx, ty = x * 2, ny * 2 - 1
            else:
                tx, ty = x * 2, ny * 2 + 1
        else:
            if nx > x:
                tx, ty = nx * 2 - 1, y * 2
            else:
                tx, ty = nx * 2 + 1, y * 2
        return nx, ny, tx, ty
    else:
        return -1, -1, -1, -1


def generate_labyrinth(n=20, m=20):
    """Генерация лабиринта"""
    used = [[False] * m for i in range(n)]
    g = []
    for i in range(n * 2 - 1):  # заполнение матрицы переходов
        g.append([])
        for j in range(m * 2 - 1):
            if i % 2 == 0 and j % 2 == 0:
                g[i].append(True)
            else:
                g[i].append(False)

    start = start_point_generate(n, m)
    finish = finish_point_generate(start, n, m)
    queue = [start]
    x, y = start
    used[x][y] = True
    x, y, tx, ty = vertical_choise(x, y, used)

    for i in range(1, m * n):
        while not (x >= 0 and y >= 0):
            x, y = queue[-1]
            queue.pop()
            x, y, tx, ty = vertical_choise(x, y, used)
        used[x][y] = True
        queue.append((x, y))
        g[tx][ty] = True
        x, y, tx, ty = vertical_choise(x, y, used)
    return g, start, finish