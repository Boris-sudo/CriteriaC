import pygame


def recalc_window_size():
    WIDTH_WINDOW = max(1000,
                       ((WIDTH * 2 - 1) // 2 + 1) * WIDTH_LINE + ((WIDTH * 2 - 1) // 2) * WIDTH_WALL + WIDTH_BORDER * 2)
    HEIGHT_WINDOW = max(800, ((HEIGHT * 2 - 1) // 2 + 1) * WIDTH_LINE + (
                (HEIGHT * 2 - 1) // 2) * WIDTH_WALL + WIDTH_BORDER * 2)

################## СТАТИЧНЫЕ ПЕРЕМЕННЫЕ
dx, dy = [1, 0, -1, 0], [0, -1, 0, 1]
language = 0
DEFAULT_CORDS = (-100, -100)
"""Длины"""
WIDTH_BORDER = 5
WIDTH_LINE = 40
WIDTH_WALL = 5
"""Пути к спрайтам"""
changeLanguageIcon = "static\change-language-icon.png"
safeIcon = "static\safe-icon.png"
crossIcon = "static\cross.png"
settingsIcon = "static\settings-image.png"
"""Определенные цвета"""
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

PURPLE = (196, 0, 255)
"""Цвета объектов"""
COLOR_WAY = (255, 255, 255)
COLOR_WALL = (0, 0, 0)
COLOR_PLAYER = (0, 0, 255)
COLOR_START = (0, 255, 0)
COLOR_FINISH = (255, 0, 0)
COLOR_TRACE = COLOR_PLAYER
TRACE = False

WIDTH = 3
HEIGHT = 3
WIDTH_WINDOW = max(1000, ((WIDTH * 2 - 1) // 2 + 1) * WIDTH_LINE + ((WIDTH * 2 - 1) // 2) * WIDTH_WALL + WIDTH_BORDER * 2)
HEIGHT_WINDOW = max(800, ((HEIGHT * 2 - 1) // 2 + 1) * WIDTH_LINE + ((HEIGHT * 2 - 1) // 2) * WIDTH_WALL + WIDTH_BORDER * 2)