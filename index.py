
import pygame
import random
import math

pygame.init()

# ---------- GAME SETTINGS ----------
WIDTH, HEIGHT = 900, 650
CELL = 25
COLS, ROWS = WIDTH // CELL, HEIGHT // CELL
FPS = 12

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NEON SNAKE // CYBERPUNK")
clock = pygame.time.Clock()

# Futuristic colors
BG = (5, 8, 22)
GRID = (15, 28, 48)
CYAN = (0, 255, 230)
PINK = (255, 40, 180)
PURPLE = (130, 60, 255)
WHITE = (230, 250, 255)
GREEN = (70, 255, 130)

font = pygame.font.SysFont("consolas", 24, bold=True)
big_font = pygame.font.SysFont("consolas", 48, bold=True)
small_font = pygame.font.SysFont("consolas", 17)

# ---------- HELPERS ----------
def draw_text(text, font_obj, color, x, y, center=False):
    surface = font_obj.render(text, True, color)
    rect = surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surface, rect)


def glow_circle(surface, color, pos, radius):
    # Soft outer glow
    for r in range(radius + 10, radius, -3):
        alpha = max(5, 30 - (r - radius) * 3)
        layer = pygame.Surface((r * 2 + 4, r * 2 + 4),
                               pygame.SRCALPHA)
        pygame.draw.circle(
            layer, (*color, alpha),
            (r + 2, r + 2), r
        )
        surface.blit(layer, (pos[0] - r - 2, pos[1] - r - 2))

    pygame.draw.circle(surface, color, pos, radius)


def new_food(snake):
    while True:
        pos = (random.randrange(COLS), random.randrange(ROWS))
        if pos not in snake:
            return pos


def reset_game():
    snake = [(COLS // 2, ROWS // 2),
             (COLS // 2 - 1, ROWS // 2),
             (COLS // 2 - 2, ROWS // 2)]
    return snake, (1, 0), (1, 0), new_food(snake), 0


# ---------- BACKGROUND ----------
def draw_background():
    screen.fill(BG)

    # Neon grid
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, GRID, (x, 0), (x, HEIGHT), 1)

    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, GRID, (0, y), (WIDTH, y), 1)

    # Futuristic header
    pygame.draw.line(screen, PURPLE, (0, 65), (WIDTH, 65), 2)
    pygame.draw.line(screen, CYAN, (0, HEIGHT - 35),
                     (WIDTH, HEIGHT - 35), 2)

    draw_text("N E O N   S N A K E", font, CYAN, 20, 20)
    draw_text("CYBER SYSTEM // ONLINE", small_font,
              PURPLE, WIDTH - 280, 25)


def draw_food(food):
    x = food[0] * CELL + CELL // 2
    y = food[1] * CELL + CELL // 2

    glow_circle(screen, PINK, (x, y), 8)

    # Small animated-style core
    pygame.draw.circle(screen, WHITE, (x, y), 3)


def draw_snake(snake):
    for i, (x, y) in enumerate(snake):
        rect = pygame.Rect(
            x * CELL + 3, y * CELL + 3,
            CELL - 6, CELL - 6
        )

        color = CYAN if i == 0 else (
            0, max(80, 230 - i * 5), max(100, 210 - i * 3)
        )

        pygame.draw.rect(screen, color, rect, border_radius=7)

        if i == 0:
            # Futuristic head
            cx = x * CELL + CELL // 2
            cy = y * CELL + CELL // 2
            pygame.draw.circle(screen, WHITE, (cx, cy), 3)


def draw_hud(score, snake):
    draw_text(f"SCORE  {score:04d}", font, GREEN, 20, HEIGHT - 29)
    draw_text(f"LENGTH  {len(snake)}", small_font,
              CYAN, 250, HEIGHT - 27)
    draw_text("WASD / ARROWS  |  ESC TO QUIT",
              small_font, PURPLE, WIDTH - 365, HEIGHT - 27)


# ---------- MAIN GAME ----------
def main():
    snake, direction, next_direction, food, score = reset_game()
    game_over = False
    paused = False
    running = True

    while running:
        clock.tick(min(FPS + score // 5, 24))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_r and game_over:
                    snake, direction, next_direction, food, score = reset_game()
                    game_over = False
                    paused = False

                if event.key == pygame.K_p and not game_over:
                    paused = not paused

                if not game_over and not paused:
                    # Prevent reversing directly into yourself
                    if event.key in (pygame.K_UP, pygame.K_w):
                        if direction != (0, 1):
                            next_direction = (0, -1)

                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        if direction != (0, -1):
                            next_direction = (0, 1)

                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        if direction != (1, 0):
                            next_direction = (-1, 0)

                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        if direction != (-1, 0):
                            next_direction = (1, 0)

        if not game_over and not paused:
            direction = next_direction
            hx, hy = snake[0]

            new_head = (hx + direction[0], hy + direction[1])

            # Wall collision
            if (new_head[0] < 0 or new_head[0] >= COLS or
                    new_head[1] < 0 or new_head[1] >= ROWS):
                game_over = True

            # Allow moving into the old tail cell if the tail moves
            elif new_head in (snake if new_head == food else snake[:-1]):
                game_over = True

            else:
                snake.insert(0, new_head)

                if new_head == food:
                    score += 1
                    food = new_food(snake)
                else:
                    snake.pop()

        draw_background()
        draw_food(food)
        draw_snake(snake)
        draw_hud(score, snake)

        if paused:
            draw_text("SYSTEM PAUSED", big_font, CYAN,
                      WIDTH // 2, HEIGHT // 2 - 20, True)
            draw_text("PRESS P TO RESUME", font, WHITE,
                      WIDTH // 2, HEIGHT // 2 + 35, True)

        if game_over:
            # Dark overlay
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 10, 200))
            screen.blit(overlay, (0, 0))

            draw_text("GAME OVER", big_font, PINK,
                      WIDTH // 2, HEIGHT // 2 - 75, True)
            draw_text(f"FINAL SCORE: {score}", font, CYAN,
                      WIDTH // 2, HEIGHT // 2 - 15, True)
            draw_text("PRESS R TO RESTART", font, WHITE,
                      WIDTH // 2, HEIGHT // 2 + 40, True)
            draw_text("ESC TO EXIT", small_font, PURPLE,
                      WIDTH // 2, HEIGHT // 2 + 80, True)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
