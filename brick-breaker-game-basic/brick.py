import pygame

import settings


class Brick:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, settings.BRICK_WIDTH, settings.BRICK_HEIGHT)
        self.alive = True

    def draw(self, surface):
        pygame.draw.rect(surface, settings.BRICK_COLOR, self.rect.inflate(-3, -2))
        pygame.draw.rect(surface, settings.BLACK, self.rect, 1)
