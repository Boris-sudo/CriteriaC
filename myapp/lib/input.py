"""Imports"""
import pygame
from .parameters import *


class Input:
    language = 0

    def __init__(self, x, y, text):
        self.pre_text = text
        self.font = pygame.font.Font(None, 25)
        self.x = x
        self.y = y
        self.string = ""
        self.text = self.font.render(self.pre_text[self.language] + self.string, True, WHITE)

    def add(self, char):
        self.string += char
        if int(self.string) > 16 or (char == "0" and len(self.string) == 1):
            self.string = self.string[:-1]
        self.text = self.font.render(self.pre_text[self.language] + self.string, True, WHITE)

    def delete(self):
        self.string = self.string[:-1]
        self.text = self.font.render(self.pre_text[self.language] + self.string, True, WHITE)

    def on_click(self, pos):
        cord_x = pos[0] - self.x
        cord_y = pos[1] - self.y
        self.rect = self.text.get_rect()
        return self.rect.collidepoint([cord_x, cord_y])

    def draw(self, screen):
        screen.blit(self.text, [self.x, self.y])

    def get_number(self):
        return int(self.string)

    def is_void(self):
        return len(self.string) == 0

    def change_language(self):
        self.language = (self.language + 1) % 2
        self.text = self.font.render(self.pre_text[self.language] + self.string, True, WHITE)