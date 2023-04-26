import time
from myapp.lib.parameters import *


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


def get_cords(x, y):
    cord_x = WIDTH_BORDER + x / 2 * (WIDTH_LINE + WIDTH_WALL) + 20
    cord_y = WIDTH_BORDER + y / 2 * (WIDTH_LINE + WIDTH_WALL) + 20
    return [cord_x, cord_y]