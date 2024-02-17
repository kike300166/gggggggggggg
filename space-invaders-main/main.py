import pygame
import random
import math

#Initialize pygame
pygame.init()

#create screen
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('background.png')

#caption and icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('rocket.png')
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 490
playerX_change = 0

#enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(32, 100))
    enemyX_change.append(2)
    enemyY_change.append(40)

#bullet
#bulletstate: ready - you can't see the bullet
#              fire - bullet is moving

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = 'ready'

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
font1 = pygame.font.Font('freesansbold.ttf', 70)
font2 = pygame.font.Font('freesansbold.ttf', 28)

textX = 10
textY = 10

def show_score(x, y):
    score = font.render("SCORE: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(a1, a2, b1, b2):
    distance = math.sqrt(math.pow(a1 - b1, 2) + math.pow(a2 - b2, 2))
    if distance <= 27:
        return True

def game_over_text(x, y):
    text = font1.render("GAME OVER", True, (255, 0, 0))
    screen.blit(text, (x, y))

def final_score(x,y):
    final_text = font2.render("YOUR SCORE WAS: " + str(score_value), True, (255, 0, 0))
    screen.blit(final_text, (x, y))


#game loop
running = True
while running:

    #Red Green Blue colour of screen (from 0 to 255)
    screen.fill((60, 60, 80))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736

    for i in range(num_of_enemies):

        #Game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text(180, 200)
            final_score(245, 280)
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        if enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        if isCollision(bulletX, bulletY, enemyX[i], enemyY[i]):
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(32, 100)
            bullet_state = 'ready'
            bulletY = 480
            score_value += 1


        enemy(enemyX[i], enemyY[i], i)



    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if bulletY <= 0:
        bullet_state = 'ready'
        bulletY = 480


    show_score(textX, textY)
    player(playerX, playerY)
    pygame.display.update()