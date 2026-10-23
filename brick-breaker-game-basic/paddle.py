import pygame

import settings


class Paddle:
    def __init__(self, screen_width):
        self.base_width = settings.PADDLE_WIDTH
        self.rect = pygame.Rect(0, settings.PADDLE_Y, self.base_width, settings.PADDLE_HEIGHT)
        self.rect.centerx = screen_width // 2
        self.x = float(self.rect.x)
        self.wide_timer = 0.0

    def widen(self, duration):
        center = self.rect.centerx
        self.rect.width = int(self.base_width * settings.WIDE_PADDLE_FACTOR)
        self.rect.centerx = center
        self.x = float(self.rect.x)
        self.wide_timer = duration

    def update(self, delta_time, screen_width):
        keys = pygame.key.get_pressed()
        direction = keys[pygame.K_d] - keys[pygame.K_a]
        self.x += direction * settings.PADDLE_SPEED * delta_time

        # Cuenta regresiva del power-up de raqueta ancha
        if self.wide_timer > 0:
            self.wide_timer -= delta_time
            if self.wide_timer <= 0:
                center = self.rect.centerx
                self.rect.width = self.base_width
                self.x = center - self.base_width / 2

        self.x = max(0, min(self.x, screen_width - self.rect.width))
        self.rect.x = round(self.x)

    def draw(self, surface):
        pygame.draw.rect(surface, settings.PADDLE_COLOR, self.rect)
