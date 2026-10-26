import pygame
import random

# Screen settings
WIDTH = 720
HEIGHT = 720
GRID_SIZE = 24
GRID_COUNT = WIDTH // GRID_SIZE

# Colors
BLACK = (15, 15, 15)
DARK = (30, 30, 30)
GREEN = (76, 175, 80)
GREEN_DARK = (32, 120, 44)
GREEN_LIGHT = (144, 238, 144)
RED = (220, 60, 60)
RED_DARK = (160, 25, 25)
WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)

# Game settings
SPEED = 6

# Snake setup
snake = [(9, 10), (8, 10), (7, 10)]
direction = (1, 0)
next_direction = (1, 0)
food = (15, 10)
score = 0

pygame.init()
pygame.display.set_caption("Realistic Snake")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)


def place_food():
    global food
    while True:
        x = random.randint(0, GRID_COUNT - 1)
        y = random.randint(0, GRID_COUNT - 1)
        if (x, y) not in snake:
            food = (x, y)
            return


def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, (45, 45, 45), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, (45, 45, 45), (0, y), (WIDTH, y))


def draw_apple(cell_x, cell_y):
    x = cell_x * GRID_SIZE + 2
    y = cell_y * GRID_SIZE + 2
    radius = GRID_SIZE // 2 - 4

    pygame.draw.circle(screen, RED, (x + radius + 2, y + radius + 2), radius)
    pygame.draw.circle(screen, RED_DARK, (x + radius + 2, y + radius + 2), radius - 6)

    stem_x = x + radius + 2
    stem_y = y + 4
    pygame.draw.rect(screen, (120, 80, 40), (stem_x - 2, stem_y, 5, 12))

    leaf_x = stem_x + 6
    leaf_y = stem_y + 4
    pygame.draw.ellipse(screen, (40, 180, 80), (leaf_x - 8, leaf_y - 12, 14, 18))


def draw_snake_segment(segment, is_head=False):
    x, y = segment
    px = x * GRID_SIZE
    py = y * GRID_SIZE

    rect = pygame.Rect(px + 2, py + 2, GRID_SIZE - 4, GRID_SIZE - 4)
    color = GREEN if not is_head else GREEN_DARK
    pygame.draw.rect(screen, color, rect, border_radius=10)

    if is_head:
        eye_offset = 6
        eye_size = 3

        left_eye = (px + 7, py + 8)
        right_eye = (px + GRID_SIZE - 10, py + 8)
        pygame.draw.circle(screen, WHITE, left_eye, eye_size)
        pygame.draw.circle(screen, WHITE, right_eye, eye_size)
        pygame.draw.circle(screen, BLACK, left_eye, 1)
        pygame.draw.circle(screen, BLACK, right_eye, 1)


def draw_snake():
    for idx, segment in enumerate(snake):
        draw_snake_segment(segment, idx == 0)


def draw_food():
    x, y = food
    draw_apple(x, y)


def draw_score():
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (18, 14))


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, 1):
                next_direction = (0, -1)
            elif event.key == pygame.K_DOWN and direction != (0, -1):
                next_direction = (0, 1)
            elif event.key == pygame.K_LEFT and direction != (1, 0):
                next_direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                next_direction = (1, 0)

    direction = next_direction

    head_x, head_y = snake[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)

    if new_head[0] < 0 or new_head[0] >= GRID_COUNT or new_head[1] < 0 or new_head[1] >= GRID_COUNT:
        running = False

    if new_head in snake[:-1]:
        running = False

    snake.insert(0, new_head)

    if new_head == food:
        score += 1
        place_food()
    else:
        snake.pop()

    screen.fill(BLACK)
    draw_grid()
    draw_food()
    draw_snake()
    draw_score()
    pygame.display.flip()
    clock.tick(SPEED)

if not running:
    game_over = font.render("Game Over!", True, WHITE)
    screen.blit(game_over, (260, 330))
    score_text = small_font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(score_text, (290, 370))
    pygame.display.flip()
    pygame.time.delay(1500)

pygame.quit()
