import pygame
import random

# Screen settings
WIDTH = 600
HEIGHT = 600
GRID_SIZE = 20
GRID_COUNT = WIDTH // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Game settings
SPEED = 5

# Snake setup
snake = [(10, 10), (9, 10), (8, 10)]
direction = (1, 0)
next_direction = (1, 0)
food = (15, 10)
score = 0

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)


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
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (0, y), (WIDTH, y))


def draw_snake():
    for segment in snake:
        x, y = segment
        pygame.draw.rect(screen, GREEN, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))


def draw_food():
    x, y = food
    pygame.draw.rect(screen, RED, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))


def draw_score():
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))


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

    # Move snake
    head_x, head_y = snake[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)

    # Collision with walls
    if new_head[0] < 0 or new_head[0] >= GRID_COUNT or new_head[1] < 0 or new_head[1] >= GRID_COUNT:
        running = False

    # Collision with itself (ignore tail if moving into it)
    if new_head in snake[:-1]:
        running = False

    snake.insert(0, new_head)

    # Eat food
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

# Game over message
if not running:
    game_over = font.render("Game Over!", True, WHITE)
    screen.blit(game_over, (200, 250))
    pygame.display.flip()
    pygame.time.delay(1500)

pygame.quit()
