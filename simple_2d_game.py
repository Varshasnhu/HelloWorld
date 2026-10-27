import pygame
import random

# --- Game setup ---
WIDTH = 800
HEIGHT = 600
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (40, 200, 90)
YELLOW = (255, 210, 60)
RED = (220, 60, 60)
BLUE = (80, 140, 255)

pygame.init()
pygame.display.set_caption("Simple 2D Game")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 30, bold=True)
small_font = pygame.font.SysFont("arial", 20)

# --- Player ---
player = pygame.Rect(60, 60, 30, 30)
player_speed = 5

# --- Collectibles ---
coins = []
for _ in range(5):
    coins.append(
        pygame.Rect(
            random.randint(50, WIDTH - 50),
            random.randint(50, HEIGHT - 50),
            18,
            18,
        )
    )

# --- Enemies ---
 enemies = []
for _ in range(3):
    enemies.append(
        pygame.Rect(
            random.randint(50, WIDTH - 50),
            random.randint(50, HEIGHT - 50),
            25,
            25,
        )
    )

# --- Score / game state ---
score = 0
game_over = False
message = "Collect all coins!"


def draw_text(text, x, y, color=WHITE, size=30):
    rendered = pygame.font.SysFont("arial", size, bold=True).render(text, True, color)
    screen.blit(rendered, (x, y))


running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.x += player_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.y -= player_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.y += player_speed

        # Keep player on screen
        player.x = max(0, min(player.x, WIDTH - player.width))
        player.y = max(0, min(player.y, HEIGHT - player.height))

        # Collect coins
        for coin in coins[:]:
            if player.colliderect(coin):
                coins.remove(coin)
                score += 1

        # Move enemies slowly and end the game if touched
        for enemy in enemies:
            enemy.x += random.choice([-1, 1])
            enemy.y += random.choice([-1, 1])
            enemy.x = max(0, min(enemy.x, WIDTH - enemy.width))
            enemy.y = max(0, min(enemy.y, HEIGHT - enemy.height))

            if player.colliderect(enemy):
                game_over = True
                message = "Game Over!"

        # Win condition
        if score >= 5:
            game_over = True
            message = "You Win!"

    # --- Drawing ---
    screen.fill(BLUE)

    # Draw player
    pygame.draw.rect(screen, GREEN, player)

    # Draw coins
    for coin in coins:
        pygame.draw.circle(screen, YELLOW, coin.center, coin.width // 2)

    # Draw enemies
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)

    # Draw score and message
    draw_text(f"Score: {score}", 20, 20, WHITE, 24)
    draw_text(message, 250, 20, WHITE, 24)

    if game_over:
        draw_text("Press R to restart", 250, 540, WHITE, 22)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            player.x = 60
            player.y = 60
            score = 0
            game_over = False
            message = "Collect all coins!"
            coins.clear()
            for _ in range(5):
                coins.append(
                    pygame.Rect(
                        random.randint(50, WIDTH - 50),
                        random.randint(50, HEIGHT - 50),
                        18,
                        18,
                    )
                )

    pygame.display.flip()

pygame.quit()
