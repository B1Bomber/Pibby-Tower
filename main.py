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
    load_boss_img2 = pygame.image.load('assets/PIBBY_mushy.png').convert_alpha()
    # Scale them to fit
    player_img = pygame.transform.smoothscale(load_player_img, (80, 80))
    boss_img = pygame.transform.smoothscale(load_boss_img, (80, 80))
    boss_img2 = pygame.transform.smoothscale(load_boss_img2, (80, 80))

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

def boss_actions(bossImg, x, y, minX, maxX, minY, maxY, speed, bullets):
    moveRight = x + (bossImg.get_width() // 2) + speed
    moveLeft = x - (bossImg.get_width() // 2) - speed
    moveUp = y + (bossImg.get_height() // 2) - speed
    moveDown = y - (bossImg.get_height() // 2) + speed

    dangerMap = {}
    dangerMap["rightDanger"] = 0
    dangerMap["leftDanger"] = 0
    dangerMap["upDanger"] = 0
    dangerMap["downDanger"] = 0
    
    # make sure it does not go out of bounds
    if moveRight > maxX:
        dangerMap["rightDanger"] = float('inf')
    if moveLeft < minX:
        dangerMap["leftDanger"] = float('inf')
    if moveUp < minY:
        dangerMap["upDanger"] = float('inf')
    if moveDown > maxY:
        dangerMap["downDanger"] = float('inf')

    # make sure it avoids bullets
    for bullet in bullets[:]:
        if bullet.origin == "boss":
            continue
        if (x <= bullet.x <= moveRight):
            dangerMap["rightDanger"] += 1
        if (moveLeft <= bullet.x <= x):
            dangerMap["leftDanger"] += 1
        if (moveUp <= bullet.y <= y):
            dangerMap["upDanger"] += 1
        if (y <= bullet.y <= moveDown):
            dangerMap["downDanger"] += 1

    # if all(c == 0 for c in dangerMap.values()) or all (d == float('inf') for d in dangerMap.values()):
    #     # dangerMap["rightDanger"] = 0
    #     # dangerMap["leftDanger"] = 0
    #     # dangerMap["upDanger"] = 0
    #     # dangerMap["downDanger"] = 0
    #     return "stay"

    #print(dangerMap)

    min_danger = min(dangerMap.values())
    candidates = [direction for direction, danger in dangerMap.items() if danger == min_danger]
    safestMove = random.choice(candidates)
    
    #print(safestMove)
    #print("ping")

    # dangerMap["rightDanger"] = 0
    # dangerMap["leftDanger"] = 0
    # dangerMap["upDanger"] = 0
    # dangerMap["downDanger"] = 0

    return safestMove
    

class Bullet:
    def __init__(self, x, y, origin, speed, state):
        self.state = state
        self.origin = origin
        # self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        if (state == "super"):
            self.x = x
            self.y = y
            self.radius = 10
            self.color = (255, 255, 0)
            self.speed = speed * 2
            self.alive = True
            self.damage = 15
        elif (state == "random"): 
            self.x = x
            self.y = y
            self.radius = random.randint(1, 10)
            self.color = (0, 255, 255)
            self.speed = 0
            self.alive = True
            self.damage = random.randint(0, 25)
        else: 
            self.x = x
            self.y = y
            self.radius = 5
            self.color = (255, 0, 255)
            self.speed = speed
            self.alive = True
            self.damage = 5 


    def update(self):
        if (self.state == "random") and (self.origin == "player"):
            self.y += random.randint(-10, 10)
            self.x += random.randint(-10, 10)
        elif (self.state == "random") and (self.origin == "boss"):
            self.y += random.randint(0, 10)
            self.x += random.randint(-10, 10)
        else:
            if (self.origin == "player"):
                self.y -= self.speed
            elif (self.origin == "boss"):
                self.y += self.speed
            
        if (self.y < 0) or (self.y > screenHeight) or (self.x < 0) or (self.x > screenWidth):
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
boss_shot_time = 0
super_boss_shot_time = 0
random_boss_shot_time = 0
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
        if keys[pygame.K_SPACE] and (current_time - last_shot_time > shoot_cooldown):
            bullet = Bullet(player_pos[0] + player_img.get_width() // 2, player_pos[1], "player", 2, "")
            bullets.append(bullet)
            last_shot_time = current_time
        if keys[pygame.K_c] and (current_time - last_shot_time > (shoot_cooldown * 2)):
            superBullet = Bullet(player_pos[0] + player_img.get_width() // 2, player_pos[1], "player", 2, "super")
            bullets.append(superBullet)
            last_shot_time = current_time
        if keys[pygame.K_c] and (current_time - last_shot_time > (shoot_cooldown * 3)):
            randomBullet = Bullet(player_pos[0] + player_img.get_width() // 2, player_pos[1], "player", 2, "random")
            bullets.append(randomBullet)
            last_shot_time = current_time

        # Clamp position
        player_pos[0] = max(0, min(player_pos[0], screenWidth - player_img.get_width()))
        player_pos[1] = max(healthBarHeight, min(player_pos[1], screenHeight - player_img.get_height() - healthBarHeight))

        # boss shooting
        if random.randint(0, 100) == 0:
            bossBullet = Bullet(boss_pos[0] + boss_img.get_width() // 2, boss_pos[1] + boss_img.get_height(), "boss", 2, "")
            bullets.append(bossBullet)

        # Update bullets
        for bullet in bullets[:]:
            bullet.update()
            bullet.draw(screen)
            if player_img.get_rect(topleft=player_pos).collidepoint(bullet.x, bullet.y):
                bullet.alive = False
                player_health -= bullet.damage
            if boss_img.get_rect(topleft=boss_pos).collidepoint(bullet.x, bullet.y):
                bullet.alive = False
                boss_health -= bullet.damage
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
    
    elif not gameOver and levelOne:
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
        if keys[pygame.K_SPACE] and (current_time - last_shot_time > shoot_cooldown):
            bullet = Bullet(player_pos[0] + player_img.get_width() // 2, player_pos[1], "player", 2, "")
            bullets.append(bullet)
            last_shot_time = current_time
        if keys[pygame.K_c] and (current_time - last_shot_time > (shoot_cooldown * 2)):
            superBullet = Bullet(player_pos[0] + player_img.get_width() // 2, player_pos[1], "player", 2, "super")
            bullets.append(superBullet)
            last_shot_time = current_time
        
        # Clamp position
        player_pos[0] = max(0, min(player_pos[0], screenWidth - player_img.get_width()))
        player_pos[1] = max(healthBarHeight, min(player_pos[1], screenHeight - player_img.get_height() - healthBarHeight))

        # boss shooting
        if current_time - boss_shot_time >= shoot_cooldown:
            bossBullet = Bullet(boss_pos[0] + boss_img.get_width() // 2, boss_pos[1] + boss_img.get_height(), "boss", 2, "")
            bullets.append(bossBullet)
            boss_shot_time = current_time
        if current_time - super_boss_shot_time >= (shoot_cooldown * 2):
            superBossBullet = Bullet(boss_pos[0] + boss_img.get_width() // 2, boss_pos[1] + boss_img.get_height(), "boss", 2, "super")
            bullets.append(superBossBullet)
            super_boss_shot_time = current_time
        if current_time - random_boss_shot_time >= (shoot_cooldown * 3):
            randomBossBullet = Bullet(boss_pos[0] + boss_img.get_width() // 2, boss_pos[1] + boss_img.get_height(), "boss", 2, "random")
            bullets.append(randomBossBullet)
            random_boss_shot_time = current_time

        # boss move
        bossMovement = boss_actions(boss_img2, boss_pos[0], boss_pos[1], 0, screenWidth, healthBarHeight, screenHeight - healthBarHeight, 4, bullets)
        if (bossMovement == "leftDanger"):
            boss_pos[0] -= 4
        elif (bossMovement == "rightDanger"):
            boss_pos[0] += 4
        elif (bossMovement == "upDanger"):
            boss_pos[1] -= 4
        elif (bossMovement == "downDanger"):
            boss_pos[1] += 4

        # Update bullets
        for bullet in bullets[:]:
            bullet.update()
            bullet.draw(screen)
            if player_img.get_rect(topleft=player_pos).collidepoint(bullet.x, bullet.y):
                bullet.alive = False
                player_health -= bullet.damage
            if boss_img.get_rect(topleft=boss_pos).collidepoint(bullet.x, bullet.y):
                bullet.alive = False
                boss_health -= bullet.damage
            if not bullet.alive:
                bullets.remove(bullet)

        # Draw
        screen.blit(player_img, player_pos)
        screen.blit(boss_img2, boss_pos)
        draw_health_bars(screen, 10, 10, boss_health, player_health)

        if player_health <= 0:
            gameOver = True
        elif boss_health <= 0:
            player_pos = [
                screenWidth / 2 - player_img.get_width() / 2,
                screenHeight * 0.75 - player_img.get_height() / 2
            ]

            boss_pos = [
                screenWidth / 2 - boss_img2.get_width() / 2,
                screenHeight * 0.25 - boss_img2.get_height() / 2
            ]
            bullets = []
            player_health = 100
            boss_health = 200
            levelOne = False
            levelTwo = True

        pygame.display.flip()
        clock.tick(60)

    elif not gameOver and levelTwo:
        gameOver = True

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
