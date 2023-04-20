import pygame

def delete_player():
    """Функция удаления игрока при движении и оставления следов"""
    if (player[0], player[1]) == start:
        pygame.draw.circle(window, color_start, (border + player[0] * (width_line + width_walls) + width_line // 2,
                                                 border + player[1] * (width_line + width_walls) + width_line // 2),
                           width_line // 2 - 3)
    else:
        pygame.draw.circle(window, color_way, (border + player[0] * (width_line + width_walls) + width_line // 2,
                                               border + player[1] * (width_line + width_walls) + width_line // 2),
                           width_line // 2 - 3)
    if trace:
        pygame.draw.circle(window, color_trace, (border + player[0] * (width_line + width_walls) + width_line // 2,
                                                 border + player[1] * (width_line + width_walls) + width_line // 2),
                           width_line // 3 - 3)


def draw_player():
    """Отрисовка игрока на экране"""
    pygame.draw.circle(window, color_player, (border + player[0] * (width_line + width_walls) + width_line // 2,
                                              border + player[1] * (width_line + width_walls) + width_line // 2),
                       width_line // 2 - 3)