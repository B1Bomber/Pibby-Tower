import pygame
import random
import sys

# Initialize
pygame.init()
screen = pygame.display.set_mode((1600, 1200))
clock = pygame.time.Clock()

# Load images
load_player_img = pygame.image.load('assets/plantson.png').convert_alpha()
load_enemy_img = pygame.image.load('assets/PIBBY_snail.png').convert_alpha()

# Scale them to fit
player_img = pygame.transform.smoothscale(load_player_img, (50, 50))
enemy_img = pygame.transform.smoothscale(load_enemy_img, (60, 60))

# Game variables
player_pos = [400, 500]
enemy_pos = [400, 100]
bullets = []
health = 100

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)

font = pygame.font.SysFont(None, 36)

def draw_health_bar(surface, x, y, health):
    pygame.draw.rect(surface, RED, (x, y, 200, 20))
    pygame.draw.rect(surface, GREEN, (x, y, 2 * health, 20))

# Game loop
running = True
while running:
    screen.fill((255, 255, 255))

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= 5
    if keys[pygame.K_RIGHT]:
        player_pos[0] += 5
    if keys[pygame.K_UP]:
        player_pos[1] -= 5
    if keys[pygame.K_DOWN]:
        player_pos[1] += 5

    # Clamp position
    player_pos[0] = max(0, min(player_pos[0], 800 - player_img.get_width()))
    player_pos[1] = max(0, min(player_pos[1], 600 - player_img.get_height()))

    # Enemy shooting
    if random.randint(0, 20) == 0:
        bullets.append([enemy_pos[0] + enemy_img.get_width() // 2, enemy_pos[1] + enemy_img.get_height()])

    # Update bullets
    for bullet in bullets[:]:
        bullet[1] += 7
        if bullet[1] > 600:
            bullets.remove(bullet)
        elif player_img.get_rect(topleft=player_pos).collidepoint(bullet):
            bullets.remove(bullet)
            health -= 5

    # Draw
    screen.blit(player_img, player_pos)
    screen.blit(enemy_img, enemy_pos)
    for bullet in bullets:
        pygame.draw.circle(screen, RED, bullet, 5)

    draw_health_bar(screen, 10, 10, max(0, health))

    if health <= 0:
        text = font.render('Game Over', True, RED)
        screen.blit(text, (300, 250))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    pygame.display.flip()
    clock.tick(60)
