import pygame

# --- Constants ---
WIDTH = 900
HEIGHT = 600
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (80, 200, 120)
BLUE = (90, 140, 255)
SKY = (120, 180, 255)
GROUND = (60, 110, 70)
PLATFORM = (120, 80, 40)
COIN = (255, 215, 60)
ENEMY = (220, 80, 80)
FLAG = (255, 255, 255)
FLAG_POLE = (220, 220, 220)

pygame.init()
pygame.display.set_caption("Mini Platformer")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 28, bold=True)
small_font = pygame.font.SysFont("arial", 20)

# --- Player ---
player = pygame.Rect(60, 420, 34, 48)
player_vel_x = 0
player_vel_y = 0
move_speed = 5
jump_strength = 15
gravity = 0.7
on_ground = False

# --- Platforms ---
platforms = [
    pygame.Rect(0, HEIGHT - 60, WIDTH, 60),
    pygame.Rect(150, 500, 180, 20),
    pygame.Rect(420, 440, 180, 20),
    pygame.Rect(660, 360, 170, 20),
    pygame.Rect(250, 300, 160, 20),
    pygame.Rect(540, 250, 160, 20),
]

# --- Coins ---
coins = [
    pygame.Rect(190, 470, 18, 18),
    pygame.Rect(500, 410, 18, 18),
    pygame.Rect(740, 330, 18, 18),
    pygame.Rect(310, 270, 18, 18),
    pygame.Rect(610, 220, 18, 18),
]

# --- Enemy ---
enemy = pygame.Rect(320, 470, 28, 28)
enemy_dir = 1
enemy_speed = 2

# --- Goal flag ---
flag = pygame.Rect(840, 150, 18, 120)

# --- HUD ---
score = 0
state = "playing"


def reset_game():
    global player, player_vel_x, player_vel_y, on_ground, score, state
    player = pygame.Rect(60, 420, 34, 48)
    player_vel_x = 0
    player_vel_y = 0
    on_ground = False
    score = 0
    for i in range(len(coins)):
        coins[i].width = 18
        coins[i].height = 18
    state = "playing"


def draw_background():
    screen.fill(SKY)
    pygame.draw.rect(screen, GREEN, (0, HEIGHT - 60, WIDTH, 60))
    for i in range(0, WIDTH, 80):
        pygame.draw.rect(screen, (110, 200, 120), (i, HEIGHT - 60, 40, 15))


def draw_platforms():
    for p in platforms:
        pygame.draw.rect(screen, PLATFORM, p)


def draw_coins():
    for coin in coins:
        if coin.width > 0:
            pygame.draw.circle(screen, COIN, coin.center, 9)
            pygame.draw.circle(screen, (255, 240, 150), coin.center, 5)


def draw_enemy():
    pygame.draw.rect(screen, ENEMY, enemy)
    pygame.draw.circle(screen, (40, 40, 40), (enemy.x + 7, enemy.y + 9), 3)
    pygame.draw.circle(screen, (40, 40, 40), (enemy.x + 19, enemy.y + 9), 3)


def draw_flag():
    pygame.draw.rect(screen, FLAG_POLE, (flag.x, flag.y, 6, flag.height))
    pygame.draw.polygon(screen, FLAG, [(flag.x + 6, flag.y + 10), (flag.x + 70, flag.y + 30), (flag.x + 6, flag.y + 50)])


def draw_player():
    pygame.draw.rect(screen, BLUE, player)
    pygame.draw.circle(screen, (240, 240, 240), (player.x + 10, player.y + 15), 4)
    pygame.draw.circle(screen, (240, 240, 240), (player.x + 24, player.y + 15), 4)


def draw_hud():
    text = font.render(f"Coins: {score}", True, WHITE)
    screen.blit(text, (20, 18))

    if state == "won":
        message = font.render("You Win! Press R to play again", True, WHITE)
        screen.blit(message, (260, 20))
    elif state == "lost":
        message = font.render("Game Over! Press R to retry", True, WHITE)
        screen.blit(message, (260, 20))


def handle_input():
    global player_vel_x, player_vel_y, on_ground
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_vel_x = -move_speed
    elif keys[pygame.K_RIGHT]:
        player_vel_x = move_speed
    else:
        player_vel_x = 0

    if keys[pygame.K_SPACE] and on_ground:
        player_vel_y = -jump_strength
        on_ground = False


def move_player():
    global on_ground, player_vel_y

    on_ground = False

    # Horizontal collision
    player.x += player_vel_x
    for plat in platforms:
        if player.colliderect(plat):
            if player_vel_x > 0:
                player.right = plat.left
            elif player_vel_x < 0:
                player.left = plat.right

    # Vertical movement and collision
    player_vel_y += gravity
    player.y += player_vel_y
    for plat in platforms:
        if player.colliderect(plat):
            if player_vel_y > 0:
                player.bottom = plat.top
                player_vel_y = 0
                on_ground = True
            elif player_vel_y < 0:
                player.top = plat.bottom
                player_vel_y = 0

    # fail if player falls below screen
    if player.y > HEIGHT + 100:
        return "lost"

    # collect coins
    for coin in coins:
        if coin.width > 0 and player.colliderect(coin):
            coin.width = 0
            coin.height = 0
            coin.x = -100
            coin.y = -100
            return "coin"

    # touch flag
    if player.colliderect(flag):
        return "won"

    # touch enemy
    if player.colliderect(enemy):
        return "lost"

    return "playing"


def move_enemy():
    global enemy_dir
    enemy.x += enemy_speed * enemy_dir
    if enemy.x <= 260 or enemy.x >= 660:
        enemy_dir *= -1


def update_game():
    global state
    if state != "playing":
        return

    handle_input()
    result = move_player()
    move_enemy()

    if result == "lost":
        state = "lost"
    elif result == "won":
        state = "won"
    elif result == "coin":
        global score
        score += 1


# --- Main loop ---
reset_game()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and state != "playing":
                reset_game()

    if state == "playing":
        update_game()

    draw_background()
    draw_platforms()
    draw_coins()
    draw_enemy()
    draw_flag()
    draw_player()
    draw_hud()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
