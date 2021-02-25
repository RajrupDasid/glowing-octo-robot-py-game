import pygame
import random
import math
from pygame import mixer
# initalize the py game
pygame.init()
# creat the screen with resoluation in the brackets
screen = pygame.display.set_mode((800, 600))  # vector value x,y axis
# background image
background = pygame.image.load('galactic.png')

# background sound
mixer.music.load('hermit.wav')
mixer.music.play(-1)


## Title and icons
pygame.display.set_caption("Galactic Warriors")
icon = pygame.image.load('galaxy.png')
pygame.display.set_icon(icon)

# Player Image
playerimg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480  # giving the half vector value to appear the image exact in the middle
playerX_change = 0

# Enemy
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 7
for i in range(num_of_enemies):

    enemyimg.append(pygame.image.load('ufo.png'))
    # random used to randomized the appearance the player
    # giving the half vector value to appear the image exact in the middle
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.4)  # vector coordinate speed values
    enemyY_change.append(40)

# bullet
bulletimg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 3
# ready state means you can't see the bullet on the screen and fire on current screen
bullet_state = "ready"
# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
testY = 10

over_font = pygame.font.Font('freesansbold.ttf', 35)


def game_over_text(x, y):
    over_text = over_font.render('Game Over Your Score is : '+ str(score_value), True, (255, 255, 255))
    screen.blit(over_text, (150, 250))


def show_score(x, y):
    score = font.render('score :' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerimg, (x, y))  # drawing a player image // bilt == draw


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x+16, y+10))


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX, 2) + (math.pow(enemyY-bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# gameloop // making sure that screen doesnot close automatically
running = True
while running:
    screen.fill((0, 0, 0))  # RGB values are written here // for background
    screen.blit(background, (0, 0))  # adding background image
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if a keystroke has pressed wether it's right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('sound.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # its value have to be 0  because it's controlling the coordinate position
                playerX_change = 0
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    for i in range(num_of_enemies):
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text(200, 250)
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # bullet fire
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # x += 5 - 0.1  -> 5 = 5- 0.1
    playerX += playerX_change
    player(playerX, playerY)
    # to appear all the times the player put it in the loop
    show_score(textX, testY)
    pygame.display.update()
