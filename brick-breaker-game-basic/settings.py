# Configuración general del juego. Cambia valores aquí, no dentro de las clases.

WINDOW_SIZE = (1510, 800)
FPS = 240
# Límite de delta_time: evita que la pelota "salte" después de un messagebox o al mover la ventana
MAX_DELTA_TIME = 1 / 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Raqueta
PADDLE_WIDTH = 200
PADDLE_HEIGHT = 30
PADDLE_Y = 650
PADDLE_SPEED = 1680  # px/s (antes 7 px por frame a 240 fps)
PADDLE_COLOR = WHITE

# Pelota
BALL_RADIUS = 5
BALL_SPEED_X = 700
BALL_SPEED_Y = 500
BALL_SPIN = 200  # cuánto cambia speed_x al golpear los extremos de la raqueta
BALL_COLOR = (250, 255, 0)
START_LIVES = 3

# Ladrillos
BRICK_ROWS = 5
BRICK_COLS = 20
BRICK_WIDTH = 50
BRICK_HEIGHT = 30
BRICK_COLOR = (172, 29, 0)

# Power-ups: tipo 0 = nada. La probabilidad de cada tipo sale de los pesos.
POWERUP_CHOICES = [0, 1, 2]
POWERUP_WEIGHTS = [50, 10, 5]
POWERUP_RADIUS = 20
POWERUP_FALL_SPEED = 500
POWERUP_COLORS = {
    1: (0, 255, 0),    # raqueta más ancha
    2: (0, 150, 255),  # vida extra
}
WIDE_PADDLE_FACTOR = 1.5
WIDE_PADDLE_DURATION = 10  # segundos
