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
WHITE = (255, 255, 255)
RED = (220, 60, 60)
RED_DARK = (160, 25, 25)
SNAKE_BODY = (149, 93, 255)
SNAKE_HEAD = (102, 58, 199)
BLUE = (92, 167, 255)
GREEN = (60, 180, 90)

# Game settings
LEVEL_SPEEDS = {1: 8, 2: 6, 3: 4}
current_level = 1
SPEED = LEVEL_SPEEDS[current_level]

# Snake setup
snake = []
direction = (1, 0)
next_direction = (1, 0)
food = (15, 10)
score = 0
game_over = False
start_screen = True

pygame.init()
pygame.display.set_caption("Ready, Set, Go!")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 42)
header_font = pygame.font.SysFont(None, 72)
small_font = pygame.font.SysFont(None, 24)


def reset_game():
    global snake, direction, next_direction, food, score, game_over, SPEED
    snake = [(9, 10), (8, 10), (7, 10)]
    direction = (1, 0)
    next_direction = (1, 0)
    score = 0
    game_over = False
    SPEED = LEVEL_SPEEDS[current_level]
    place_food()


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
    color = SNAKE_HEAD if is_head else SNAKE_BODY
    pygame.draw.rect(screen, color, rect, border_radius=10)

    if is_head:
        left_eye = (px + 7, py + 8)
        right_eye = (px + GRID_SIZE - 10, py + 8)
        pygame.draw.circle(screen, WHITE, left_eye, 3)
        pygame.draw.circle(screen, WHITE, right_eye, 3)
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


def draw_level_info():
    level_text = small_font.render(f"Level {current_level}", True, WHITE)
    screen.blit(level_text, (620, 18))


def draw_start_screen():
    screen.fill(BLACK)
    title = header_font.render("Ready, Set, Go!", True, BLUE)
    screen.blit(title, (190, 160))

    subtitle = font.render("Choose a level: 1 = slow, 2 = medium, 3 = fast", True, WHITE)
    screen.blit(subtitle, (60, 250))

    level_box = pygame.Rect(200, 330, 320, 90)
    pygame.draw.rect(screen, DARK, level_box, border_radius=12)
    pygame.draw.rect(screen, BLUE, level_box, 3, border_radius=12)

    level_text = header_font.render(f"Level {current_level}", True, WHITE)
    screen.blit(level_text, (285, 350))

    help_text = small_font.render("Press 1 / 2 / 3, then click mouse or press Enter to start", True, WHITE)
    screen.blit(help_text, (120, 460))

    pygame.display.flip()


def draw_game_over_prompt():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))

    game_over_text = header_font.render("Game Over", True, WHITE)
    screen.blit(game_over_text, (215, 250))

    prompt = small_font.render("Play again? (Y/N)", True, WHITE)
    screen.blit(prompt, (285, 345))

    score_text = small_font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(score_text, (295, 380))


reset_game()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if start_screen:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    current_level = 1
                elif event.key == pygame.K_2:
                    current_level = 2
                elif event.key == pygame.K_3:
                    current_level = 3
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    start_screen = False
                    reset_game()
                elif event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                start_screen = False
                reset_game()

            draw_start_screen()
            continue

        if event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_y:
                    reset_game()
                elif event.key == pygame.K_n:
                    running = False
            else:
                if event.key == pygame.K_UP and direction != (0, 1):
                    next_direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    next_direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    next_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    next_direction = (1, 0)

    if not start_screen and not game_over:
        direction = next_direction

        head_x, head_y = snake[0]
        dx, dy = direction
        new_head = (head_x + dx, head_y + dy)

        if new_head[0] < 0 or new_head[0] >= GRID_COUNT or new_head[1] < 0 or new_head[1] >= GRID_COUNT:
            game_over = True
        elif new_head in snake[:-1]:
            game_over = True
        else:
            snake.insert(0, new_head)

            if new_head == food:
                score += 1
                place_food()
            else:
                snake.pop()

    if not start_screen:
        screen.fill(BLACK)
        draw_grid()
        draw_food()
        draw_snake()
        draw_score()
        draw_level_info()

        if game_over:
            draw_game_over_prompt()

        pygame.display.flip()
        clock.tick(SPEED)

pygame.quit()
