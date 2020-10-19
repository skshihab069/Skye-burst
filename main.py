import pygame
import random
import math
from pygame import mixer

# initializing pygame
pygame.init()

# making screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('1876.jpg').convert()

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Game tittle & icon
pygame.display.set_caption("ALIEN HUNTER")
icon = pygame.image.load('rocket-ship.png')
pygame.display.set_icon(icon)

# player info
player_img = pygame.image.load('jet.png').convert_alpha()
playerX = 370
playerY = 480
playerX_change = 0

# enemy info
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
number_of_enemies = 6
for i in range(number_of_enemies):
    enemy_img.append(pygame.image.load('alien.png').convert_alpha())
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet info
# ready state means bullet the bullet is not moving
# Fire state means the bullet is moving
bullet_img = pygame.image.load('ammunition.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 20
bullet_state = 'ready'

# displaying the score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game over fonts
over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    game_over = over_font.render('GAME OVER', True, (255, 0, 255))
    screen.blit(game_over, (200, 250))


def show_score(x, y):
    score = font.render('Score :' + str(score_value), True, (255, 0, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_img, (x + 16, y + 10))


def is_collusion(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:

    # R G B = red, green, blue
    screen.fill((153, 51, 255))
    # background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -12
            if event.key == pygame.K_RIGHT:
                playerX_change = 12
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    # Creating a border for player
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Creating a border for game over text and enemy movement
    for i in range(number_of_enemies):

        # Game over text
        if enemyY[i] > 440:
            for j in range(number_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
          # Enemy movement
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collution
        collution = is_collusion(enemyX[i], enemyY[i], bulletX, bulletY)
        if collution:
            collution_sound = mixer.Sound('explosion.wav')
            collution_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1

            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'
    if bullet_state is 'fire':
        bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
