import pygame

import settings


class Ball:
    def __init__(self, x, y):
        self.radius = settings.BALL_RADIUS
        self.reset(x, y)

    def reset(self, x, y):
        """Coloca la pelota en (x, y) moviéndose hacia arriba."""
        self.x = float(x)
        self.y = float(y)
        self.speed_x = settings.BALL_SPEED_X
        self.speed_y = -settings.BALL_SPEED_Y

    @property
    def rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def update(self, delta_time, screen_width, screen_height):
        """Mueve la pelota y rebota en las paredes. Devuelve True si cayó por debajo de la pantalla."""
        self.x += self.speed_x * delta_time
        self.y += self.speed_y * delta_time

        if self.y - self.radius <= 0:
            self.y = self.radius
            self.speed_y = abs(self.speed_y)
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.speed_x = abs(self.speed_x)
        if self.x + self.radius >= screen_width:
            self.x = screen_width - self.radius
            self.speed_x = -abs(self.speed_x)

        return self.y - self.radius > screen_height

    def bounce_off_paddle(self, paddle_rect):
        # Solo rebota si va bajando, así no se queda "pegada" dentro de la raqueta
        if self.speed_y <= 0 or not self.rect.colliderect(paddle_rect):
            return

        self.y = paddle_rect.top - self.radius
        self.speed_y = -self.speed_y

        # La raqueta se divide en tercios: los extremos dan efecto, el centro lo quita
        third = paddle_rect.width / 3
        if self.x < paddle_rect.left + third:
            self.speed_x -= settings.BALL_SPIN
        elif self.x > paddle_rect.left + third * 2:
            self.speed_x += settings.BALL_SPIN
        else:
            self.speed_x = settings.BALL_SPEED_X if self.speed_x >= 0 else -settings.BALL_SPEED_X

    def bounce_off_rect(self, rect):
        """Rebota contra un rectángulo (ladrillo). Devuelve True si hubo choque."""
        ball_rect = self.rect
        if not ball_rect.colliderect(rect):
            return False

        # El lado con menos solapamiento es el lado por el que entró la pelota
        overlap_left = ball_rect.right - rect.left
        overlap_right = rect.right - ball_rect.left
        overlap_top = ball_rect.bottom - rect.top
        overlap_bottom = rect.bottom - ball_rect.top

        if min(overlap_left, overlap_right) < min(overlap_top, overlap_bottom):
            if overlap_left < overlap_right:
                self.x -= overlap_left
                self.speed_x = -abs(self.speed_x)
            else:
                self.x += overlap_right
                self.speed_x = abs(self.speed_x)
        else:
            if overlap_top < overlap_bottom:
                self.y -= overlap_top
                self.speed_y = -abs(self.speed_y)
            else:
                self.y += overlap_bottom
                self.speed_y = abs(self.speed_y)
        return True

    def draw(self, surface):
        pygame.draw.circle(surface, settings.BALL_COLOR, (round(self.x), round(self.y)), self.radius)
