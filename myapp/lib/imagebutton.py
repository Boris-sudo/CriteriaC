import pygame


class StartButton:
    text = ["Начать игру", "Start the game"]
    font_name = "Arial"
    font_size = 30
    width = 500
    width_above = 510
    height = 90
    height_above = 100
    language = 0

    def __init__(self, WIDTH, margin_top, surface):
        pygame.init()
        self.surface = surface
        self.button_rect = pygame.Rect((WIDTH - self.width) / 2, margin_top, self.width, self.height)
        self.button_rect_above = pygame.Rect((WIDTH - self.width_above) / 2, margin_top - 5, self.width_above, self.height_above)
        self.WIDTH = WIDTH
        self.margin_top = margin_top
        self.where = self.button_rect.center
        self.color = (243, 239, 224)
        self.font = None
        self.last_time_red = -100

    def on_click(self, pos):
        return self.button_rect.collidepoint(pos)

    def on_hover(self, pos, time):
        if abs(self.last_time_red - time) > 1:
            if self.button_rect.collidepoint(pos):
                self.color = (67, 66, 66)
            else:
                self.color = (243, 239, 224)

    def draw(self, surface):
        button_above = pygame.draw.rect(self.surface, pygame.Color(255, 255, 255, 127), self.button_rect_above, 20)
        button = pygame.draw.rect(self.surface, self.color, self.button_rect, 10)
        font = pygame.font.SysFont(self.font_name, self.font_size)
        text = font.render(self.text[self.language], True, self.color)
        text_rect = text.get_rect(center=self.where)
        surface.blit(text, text_rect)

    def change_color(self, color, time):
        self.color = color
        self.last_time_red = time

    def change_language(self):
        self.language = (self.language + 1) % 2


class ImageButton:
    def __init__(self, WIDTH, HEIGHT, surface, file_path):
        pygame.init()
        # Image
        self.image = pygame.image.load(file_path).convert_alpha()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        # Window
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        # Rect
        self.rect = pygame.Rect((self.WIDTH - self.width - 10, self.HEIGHT - self.height - 10, self.width, self.height))
        # Stuff
        self.surface = surface

    def on_click(self, pos):
        return self.rect.collidepoint(pos)

    def draw(self, surface):
        surface.blit(self.image, self.rect)