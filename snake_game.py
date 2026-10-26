import math
import random
import pygame

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
YELLOW = (255, 215, 0)
BLUE = (92, 167, 255)
GREEN = (60, 180, 90)
PURPLE = (149, 93, 255)
PURPLE_DARK = (102, 58, 199)
ORANGE = (255, 140, 40)
ORANGE_DARK = (180, 90, 0)
BERRY = (180, 80, 200)
GOLD = (255, 200, 50)
GOLD_DARK = (180, 140, 0)

# Game settings
LEVEL_SPEEDS = {1: 8, 2: 6, 3: 4}
LEVEL_FOODS = {
    1: ["apple", "berry"],
    2: ["apple", "orange", "grape"],
    3: ["golden_apple", "star_fruit", "grape"],
}
current_level = 1
SPEED = LEVEL_SPEEDS[current_level]

# Snake setup
snake = []
direction = (1, 0)
next_direction = (1, 0)
food = (15, 10)
food_type = "apple"
score = 0
game_over = False
start_screen = True

# Snake color selection
snake_colors = {
    "purple": (PURPLE, PURPLE_DARK),
    "blue": (BLUE, (57, 99, 180)),
    "green": (GREEN, (34, 120, 60)),
    "red": (RED, RED_DARK),
}
snake_color_name = "purple"
SNAKE_BODY, SNAKE_HEAD = snake_colors[snake_color_name]

pygame.init()
pygame.display.set_caption("Ready, Set, Go!")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("verdana", 30, bold=True)
header_font = pygame.font.SysFont("arialblack", 58, bold=True)
subtitle_font = pygame.font.SysFont("verdana", 26, bold=True)
small_font = pygame.font.SysFont("verdana", 22)


def reset_game():
    global snake, direction, next_direction, food, score, game_over, SPEED, SNAKE_BODY, SNAKE_HEAD, food_type
    snake = [(9, 10), (8, 10), (7, 10)]
    direction = (1, 0)
    next_direction = (1, 0)
    score = 0
    game_over = False
    SPEED = LEVEL_SPEEDS[current_level]
    SNAKE_BODY, SNAKE_HEAD = snake_colors[snake_color_name]
    place_food()


def place_food():
    global food, food_type
    while True:
        x = random.randint(0, GRID_COUNT - 1)
        y = random.randint(0, GRID_COUNT - 1)
        if (x, y) not in snake:
            food = (x, y)
            food_type = random.choice(LEVEL_FOODS[current_level])
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


def draw_berry(cell_x, cell_y):
    x = cell_x * GRID_SIZE + 8
    y = cell_y * GRID_SIZE + 8
    pygame.draw.circle(screen, BERRY, (x + 8, y + 8), 8)
    pygame.draw.circle(screen, (120, 40, 150), (x + 11, y + 4), 3)
    pygame.draw.line(screen, (90, 50, 100), (x + 8, y + 2), (x + 8, y - 4), 2)


def draw_orange(cell_x, cell_y):
    x = cell_x * GRID_SIZE + 4
    y = cell_y * GRID_SIZE + 4
    pygame.draw.circle(screen, ORANGE, (x + 10, y + 10), 10)
    pygame.draw.circle(screen, ORANGE_DARK, (x + 10, y + 10), 6)
    pygame.draw.circle(screen, (255, 220, 160), (x + 14, y + 6), 2)


def draw_grape(cell_x, cell_y):
    x = cell_x * GRID_SIZE + 5
    y = cell_y * GRID_SIZE + 5
    colors = [(160, 90, 220), (180, 110, 240), (120, 70, 180)]
    for dx, dy, color in [(0, 0, colors[0]), (8, 0, colors[1]), (4, 8, colors[2]), (12, 8, colors[1]), (0, 12, colors[0]), (8, 12, colors[2])]:
        pygame.draw.circle(screen, color, (x + dx + 6, y + dy + 6), 5)


def draw_golden_apple(cell_x, cell_y):
    x = cell_x * GRID_SIZE + 2
    y = cell_y * GRID_SIZE + 2
    radius = GRID_SIZE // 2 - 4

    pygame.draw.circle(screen, GOLD, (x + radius + 2, y + radius + 2), radius)
    pygame.draw.circle(screen, GOLD_DARK, (x + radius + 2, y + radius + 2), radius - 7)

    stem_x = x + radius + 2
    stem_y = y + 4
    pygame.draw.rect(screen, (120, 80, 40), (stem_x - 2, stem_y, 5, 12))

    leaf_x = stem_x + 6
    leaf_y = stem_y + 2
    pygame.draw.ellipse(screen, (60, 160, 90), (leaf_x - 8, leaf_y - 12, 14, 18))


def draw_star_fruit(cell_x, cell_y):
    x = cell_x * GRID_SIZE + 12
    y = cell_y * GRID_SIZE + 12
    points = []
    for i in range(10):
        angle = math.radians(i * 36 - 90)
        radius = 10 if i % 2 == 0 else 5
        px = x + radius * math.cos(angle)
        py = y + radius * math.sin(angle)
        points.append((px, py))
    pygame.draw.polygon(screen, (255, 220, 90), points)
    pygame.draw.polygon(screen, (200, 150, 30), points, 2)


def draw_food():
    x, y = food
    if food_type == "apple":
        draw_apple(x, y)
    elif food_type == "berry":
        draw_berry(x, y)
    elif food_type == "orange":
        draw_orange(x, y)
    elif food_type == "grape":
        draw_grape(x, y)
    elif food_type == "golden_apple":
        draw_golden_apple(x, y)
    elif food_type == "star_fruit":
        draw_star_fruit(x, y)


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


def draw_score():
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (18, 14))


def draw_level_info():
    level_text = small_font.render(f"Level {current_level}", True, WHITE)
    screen.blit(level_text, (620, 18))


def draw_intro_animation():
    time_ms = pygame.time.get_ticks()
    for i in range(18):
        x = (i * 42 + time_ms * 0.03) % (WIDTH + 150) - 50
        y = 120 + (i % 6) * 45 + math.sin(time_ms / 500 + i) * 18
        radius = 7 + (i % 4) * 3
        pygame.draw.circle(screen, (50 + i * 6, 80 + i * 5, 120 + i * 4), (int(x), int(y)), radius)

    glow = 100 + int(40 * math.sin(time_ms / 250))
    title_color = (glow, glow + 30, 255)
    title = header_font.render("READY, SET, GO!", True, title_color)
    screen.blit(title, (120, 110))


def draw_start_screen():
    screen.fill(BLACK)
    draw_intro_animation()

    info = subtitle_font.render("Move with the arrow keys: ↑ ↓ ← →", True, WHITE)
    screen.blit(info, (140, 220))

    subtitle = subtitle_font.render("Choose Level 1, 2 or 3", True, YELLOW)
    screen.blit(subtitle, (200, 280))

    level_box = pygame.Rect(200, 330, 320, 90)
    pygame.draw.rect(screen, DARK, level_box, border_radius=12)
    pygame.draw.rect(screen, BLUE, level_box, 3, border_radius=12)

    level_text = header_font.render(f"Level {current_level}", True, WHITE)
    text_rect = level_text.get_rect(center=level_box.center)
    screen.blit(level_text, text_rect)

    info_line = small_font.render("Color: P purple  |  B blue  |  G green  |  R red", True, WHITE)
    screen.blit(info_line, (110, 440))

    current_color_line = small_font.render(f"Current snake color: {snake_color_name.title()}", True, WHITE)
    screen.blit(current_color_line, (220, 470))

    help_text = small_font.render("Press 1 / 2 / 3 for level, P/B/G/R for color, then Enter or click to start", True, WHITE)
    screen.blit(help_text, (40, 520))

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
                elif event.key == pygame.K_p:
                    snake_color_name = "purple"
                elif event.key == pygame.K_b:
                    snake_color_name = "blue"
                elif event.key == pygame.K_g:
                    snake_color_name = "green"
                elif event.key == pygame.K_r:
                    snake_color_name = "red"
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
