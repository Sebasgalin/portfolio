import random
from tkinter import messagebox

import pygame
from pygame.locals import *

import settings
from ball import Ball
from brick import Brick
from paddle import Paddle
from powerup import PowerUp


class Game:
    """Dueño del bucle principal: eventos -> lógica (update) -> dibujo (draw)."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(settings.WINDOW_SIZE, pygame.RESIZABLE)
        pygame.display.set_caption("Brick Breaker")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 30)  # se crea una sola vez, no en cada frame
        self.running = True
        self.restart()

    # ---------- Estado de la partida ----------

    def restart(self):
        width = self.screen.get_width()
        self.paddle = Paddle(width)
        self.ball = Ball(self.paddle.rect.centerx, self.paddle.rect.top - settings.BALL_RADIUS - 10)
        self.bricks = self._create_bricks(width)
        self.powerups = []
        self.lives = settings.START_LIVES
        self.paused = True

    def _create_bricks(self, screen_width):
        offset_x = random.randint(0, max(0, screen_width - settings.BRICK_COLS * settings.BRICK_WIDTH))
        offset_y = random.randint(50, 300)
        return [
            Brick(offset_x + col * settings.BRICK_WIDTH, offset_y + row * settings.BRICK_HEIGHT)
            for row in range(settings.BRICK_ROWS)
            for col in range(settings.BRICK_COLS)
        ]

    # ---------- Bucle principal ----------

    def run(self):
        while self.running:
            delta_time = min(self.clock.tick(settings.FPS) / 1000, settings.MAX_DELTA_TIME)
            self.handle_events()
            if self.running and not self.paused:
                self.update(delta_time)
            if self.running:
                self.draw()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.paused = True
                elif event.key == K_RETURN:
                    self.paused = False
                elif event.key == K_F11:
                    pygame.display.toggle_fullscreen()
                elif event.key == K_BACKSPACE:
                    self.running = False

    def update(self, delta_time):
        width, height = self.screen.get_size()

        self.paddle.update(delta_time, width)

        if self.ball.update(delta_time, width, height):
            self.lose_life()
            return
        self.ball.bounce_off_paddle(self.paddle.rect)

        # Como mucho un ladrillo por frame, igual que antes
        for brick in self.bricks:
            if brick.alive and self.ball.bounce_off_rect(brick.rect):
                brick.alive = False
                self.try_spawn_powerup(brick.rect.center)
                break

        # Los power-ups se actualizan aquí, un paso por frame, sin bloquear el juego
        for powerup in self.powerups[:]:
            powerup.update(delta_time)
            if powerup.rect.colliderect(self.paddle.rect):
                self.apply_powerup(powerup.kind)
                self.powerups.remove(powerup)
            elif powerup.is_off_screen(height):
                self.powerups.remove(powerup)

        if not any(brick.alive for brick in self.bricks):
            self.victory()

    # ---------- Power-ups ----------

    def try_spawn_powerup(self, position):
        kind = random.choices(settings.POWERUP_CHOICES, settings.POWERUP_WEIGHTS, k=1)[0]
        if kind != 0:
            self.powerups.append(PowerUp(kind, *position))

    def apply_powerup(self, kind):
        if kind == 1:
            self.paddle.widen(settings.WIDE_PADDLE_DURATION)
        elif kind == 2:
            self.lives += 1

    # ---------- Vidas / fin de juego ----------

    def lose_life(self):
        self.lives -= 1
        if self.lives == 0:
            if messagebox.askyesno("Game over", "¿Deseas reiniciar el juego?"):
                self.restart()
            else:
                self.running = False
        else:
            messagebox.showinfo("Has perdido una vida", f"Te quedan {self.lives} vidas")
            self.ball.reset(self.paddle.rect.centerx, self.paddle.rect.top - settings.BALL_RADIUS - 10)
            self.powerups.clear()

    def victory(self):
        self.draw()
        messagebox.showinfo("Victory", "Has completado el juego")
        self.running = False

    # ---------- Dibujo ----------

    def draw(self):
        self.screen.fill(settings.BLACK)

        for brick in self.bricks:
            if brick.alive:
                brick.draw(self.screen)
        for powerup in self.powerups:
            powerup.draw(self.screen)
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        self.draw_hud()

        pygame.display.flip()

    def draw_hud(self):
        # Vidas arriba a la derecha
        radius = settings.BALL_RADIUS
        x = self.screen.get_width() - self.lives * radius * 2
        for _ in range(self.lives):
            pygame.draw.circle(self.screen, settings.BALL_COLOR, (x, 30), radius)
            x += radius * 2

        fps_text = self.font.render(f"FPS: {self.clock.get_fps():.2f}", True, settings.WHITE)
        self.screen.blit(fps_text, (10, 10))

        if self.paused:
            text = self.font.render("Pausa - presiona ENTER para jugar", True, settings.WHITE)
            self.screen.blit(text, text.get_rect(center=self.screen.get_rect().center))
