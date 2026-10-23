import pygame

import settings


class PowerUp:
    """Un power-up que cae desde un ladrillo. Cada uno guarda su propia posición."""

    def __init__(self, kind, x, y):
        self.kind = kind
        self.x = float(x)
        self.y = float(y)
        self.radius = settings.POWERUP_RADIUS
        self.color = settings.POWERUP_COLORS[kind]

    @property
    def rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def update(self, delta_time):
        self.y += settings.POWERUP_FALL_SPEED * delta_time

    def is_off_screen(self, screen_height):
        return self.y - self.radius > screen_height

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (round(self.x), round(self.y)), self.radius)
