# Brick Breaker Game basic

A classic brick breaker game made with Python and pygame. Move the paddle, keep the ball in play and break every brick to win.

## Features

- Randomly positioned wall of 100 bricks (5 rows × 20 columns)
- Ball spin: hitting the ends of the paddle changes the ball's angle
- Power-ups that drop from broken bricks:
  - **Green:** wider paddle for 10 seconds
  - **Blue:** extra life
- 3 starting lives, shown in the top-right corner
- Frame-rate independent movement, resizable window and fullscreen mode
- All tuning values (speeds, sizes, colors, power-up odds) live in `settings.py`

## Controls

| Key | Action |
| --- | --- |
| `A` / `D` | Move the paddle left / right |
| `Enter` | Start or resume |
| `Esc` | Pause |
| `F11` | Toggle fullscreen |
| `Backspace` | Quit |

## Running the game

Requires Python 3 and pygame.

```bash
pip install -r requirements.txt
python pruebitas.py
```

## Project structure

| File | Purpose |
| --- | --- |
| `pruebitas.py` | Entry point |
| `game.py` | Main loop, collisions, lives and power-up logic |
| `ball.py` | Ball movement and bouncing |
| `paddle.py` | Paddle movement and the wide-paddle power-up |
| `brick.py` | Brick drawing |
| `powerup.py` | Falling power-ups |
| `settings.py` | Game configuration |
