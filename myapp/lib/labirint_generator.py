import random
from parameters import dx, dy


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