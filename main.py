import pygame
import random
import sys

# Game variables
screenWidth = 480
screenHeight = 800
healthBarHeight = 20

bullets = []
player_health = 100
boss_health = 200

fontSize = 36

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

if __name__ == "__main__":
    # Initialize
    pygame.init()
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    clock = pygame.time.Clock()

    # Load images
    load_player_img = pygame.image.load('assets/plantson.png').convert_alpha()
    load_boss_img = pygame.image.load('assets/Castle_Pibby.png').convert_alpha()

    # Scale them to fit
    player_img = pygame.transform.smoothscale(load_player_img, (80, 80))
    boss_img = pygame.transform.smoothscale(load_boss_img, (80, 80))

    player_pos = [
        screenWidth / 2 - player_img.get_width() / 2,
        screenHeight * 0.75 - player_img.get_height() / 2
    ]

    boss_pos = [
        screenWidth / 2 - boss_img.get_width() / 2,
        screenHeight * 0.25 - boss_img.get_height() / 2
    ]

    font = pygame.font.SysFont(None, fontSize)

def draw_health_bars(surface, x, y, bossHealth, playerHealth):
    # boss health bar
    pygame.draw.rect(surface, RED, (x, y, 200, healthBarHeight))
    pygame.draw.rect(surface, BLUE, (x, y, bossHealth, healthBarHeight))

    # player health bar
    pygame.draw.rect(surface, RED, (x, screenHeight - healthBarHeight - y, 200, healthBarHeight))
    pygame.draw.rect(surface, GREEN, (x, screenHeight - healthBarHeight - y, 2 * playerHealth, healthBarHeight))

class Bullet:
    def __init__(self, x, y, speed, state):
        if (state == "super"):
            self.x = x
            self.y = y
            self.radius = 10
            self.color = (255, 255, 0)
            self.speed = speed * 2
            self.alive = True
        elif (state == "random"): 
            self.x = random.randint(-255, 255)
            self.y = random.randint(-255, 255)
            self.radius = random.randint(1, 10)
            self.color = (0, 255, 255)
            self.speed = random.randint(-100, 100)
            self.alive = True
        else: 
            self.x = x
            self.y = y
            self.radius = 5
            self.color = (255, 0, 255)
            self.speed = speed
            self.alive = True


    def update(self):
        self.y -= self.speed
        if (self.y < 0) or (self.y > screenHeight):
            self.alive = False

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)


# finite state machine
running = True
gameOver = False
tutorial = True
levelOne = False
levelTwo = False

# attack cool down
last_shot_time = 0 
shoot_cooldown = 700  # milliseconds, 0.3 seconds

# Game loop
while running:
    screen.fill((255, 255, 255))
    current_time = pygame.time.get_ticks()

    # click x to exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not gameOver and tutorial:
        # player control
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_pos[0] -= 2
        if keys[pygame.K_RIGHT]:
            player_pos[0] += 2
        if keys[pygame.K_UP]:
            player_pos[1] -= 2
        if keys[pygame.K_DOWN]:
            player_pos[1] += 2
        if keys[pygame.K_SPACE] and current_time - last_shot_time > shoot_cooldown:
            bullet = Bullet(player_pos[0] + player_img.get_width() // 2, player_pos[1], 2, "")
            bullets.append(bullet)
            last_shot_time = current_time

        # Clamp position
        player_pos[0] = max(0, min(player_pos[0], screenWidth - player_img.get_width()))
        player_pos[1] = max(healthBarHeight, min(player_pos[1], screenHeight - player_img.get_height() - healthBarHeight))

        # boss shooting
        # if random.randint(0, 20) == 0:
        #     bullets.append([boss_pos[0] + boss_img.get_width() // 2, boss_pos[1] + boss_img.get_height()])

        # Update bullets
        # for bullet in bullets[:]:
        #     bullet[1] += 3
        #     elif player_img.get_rect(topleft=player_pos).collidepoint(bullet):
        #         bullets.remove(bullet)
        #         player_health -= 5

        for bullet in bullets[:]:  # iterate over a copy to allow safe removal
            bullet.update()
            bullet.draw(screen)
            if not bullet.alive:
                bullets.remove(bullet)

        # Draw
        screen.blit(player_img, player_pos)
        screen.blit(boss_img, boss_pos)
        draw_health_bars(screen, 10, 10, boss_health, player_health)

        if player_health <= 0:
            gameOver = True
        elif boss_health <= 0:
            tutorial = False
            levelOne = True

        pygame.display.flip()
        clock.tick(60)
    
    elif gameOver:
        gameOverText = font.render('Game Over', True, RED)
        screen.blit(gameOverText, gameOverText.get_rect(center=(screenWidth / 2, screenHeight / 2)))
        retryText = font.render('Retry? [Y] [N]', True, (0, 0, 0))
        screen.blit(retryText, retryText.get_rect(center=(screenWidth / 2, (screenHeight / 2) + fontSize)))
        pygame.display.flip()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_y]:
            player_pos = [
                screenWidth / 2 - player_img.get_width() / 2,
                screenHeight * 0.75 - player_img.get_height() / 2
            ]

            boss_pos = [
                screenWidth / 2 - boss_img.get_width() / 2,
                screenHeight * 0.25 - boss_img.get_height() / 2
            ]
            bullets = []
            player_health = 100
            boss_health = 200
            gameOver = False
        elif keys[pygame.K_n]:
            running = False
