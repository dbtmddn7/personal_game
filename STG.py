import pygame
import sys
import random
from time import sleep

rockImage = ['resource\\rock01.png', 'resource\\rock02.png', 'resource\\rock03.png', 'resource\\rock04.png', \
             'resource\\rock05.png', 'resource\\rock06.png', 'resource\\rock07.png', 'resource\\rock08.png', \
             'resource\\rock09.png', 'resource\\rock10.png']
explosionSound = ['resource\\explosion01.wav','resource\\explosion02.wav','resource\\explosion03.wav', \
                  'resource\\explosion04.wav']

BLACK = (0, 255, 0)
padWidth = 480
padHeight = 640

def writeMessage(text):
    global gamePad, gameoverSound
    textfont = pygame.font.Font('resource\\NanumGothic.ttf', 40)
    text = textfont.render(text, True, (255,0,0))
    textpos = text.get_rect()
    textpos.center = (padWidth/2, padHeight/2)
    gamePad.blit(text, textpos)
    pygame.display.update()
    pygame.mixer.music.stop()
    gameOverSound.play()
    sleep(2)
    pygame.mixer.music.play(-1)
    runGame()

def crash():
    global gamePad
    writeMessage("Destroyed Flight!!")

def gameOver():
    global gamePad
    writeMessage("Game Over!!")

def writeScore(count):
    global gamePad
    font = pygame.font.Font('resource\\NanumGothic.ttf', 20)
    text = font.render('Destroyed No. : ' + str(count), True, (255, 255, 255))
    gamePad.blit(text, (10, 10))


def writePassed(count):
    global gamePad
    font = pygame.font.Font('resource\\NanumGothic.ttf', 20)
    text = font.render('Failed No. : ' + str(count), True, (255, 0, 0))
    gamePad.blit(text, (350, 10))


def drawOject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))


def initGame():
    global gamePad, clock, background, fighter, missile, explosion, missileSound, gameOverSound
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('STG testing')
    background = pygame.image.load('resource\\background.png')
    fighter = pygame.image.load('resource\\fighter.png')
    missile = pygame.image.load('resource\\missile.png')
    explosion = pygame.image.load('resource\\explosion.png')
    pygame.mixer.music.load('resource\\music.wav')
    pygame.mixer.music.play(-1)
    missileSound = pygame.mixer.Sound('resource\\missile.wav')
    gameOverSound = pygame.mixer.Sound('resource\\gameover.wav')
    clock = pygame.time.Clock()


def runGame():
    global gamePad, clock, background, fighter, missile, explosion, missileSound

    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]
    x = padWidth * 0.45
    y = padHeight * 0.9
    fighterX = 0
    missileXY = []

    rock = pygame.image.load(random.choice(rockImage))
    rockSize = rock.get_rect().size
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]
    rockX = random.randrange(0, padWidth - rockWidth)
    # print('rockX = ', rockX)
    rockY = 0
    rockSpeed = 2
    destroySound = pygame.mixer.Sound(random.choice(explosionSound))

    isShot = False
    shotCount = 0
    rockPassed = 0

    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                pygame.quit()
                sys.exit()
            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT:
                    fighterX -= 5
                elif event.key == pygame.K_RIGHT:
                    fighterX += 5
                elif event.key == pygame.K_SPACE:
                    missileSound.play()
                    missileX = x + fighterWidth / 2
                    missileY = y - fighterHeight
                    missileXY.append([missileX, missileY])
            if event.type in [pygame.KEYUP]:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighterX = 0

        drawOject(background, 0, 0)

        x += fighterX
        if x < 0: x = 0
        if x > padWidth - fighterWidth: x = padWidth - fighterWidth

        if y < rockY + rockHeight:
            #print(str(rockX), '>', str(x), ' and ',str(rockX), '<', str(x + fighterWidth))
            #print('or ', str(rockX + rockWidth), '>', str(x), ' and ', str(rockX + rockWidth), ' < ', str(x + fighterWidth))
            #sleep(1)
            if (rockX > x and rockX < x + fighterWidth) or (rockX + rockWidth > x and rockX < x + fighterWidth):
                crash()

        drawOject(fighter, x, y)

        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY):
                bxy[1] -= 10
                missileXY[i][1] = bxy[1]
                if bxy[1] < rockY:
                    if bxy[0] > rockX and bxy[0] < rockX + rockWidth:
                        missileXY.remove(bxy)
                        isShot = True
                        shotCount += 1

                if bxy[1] <= 0:
                    try:
                        missileXY.remove(bxy)
                    except:
                        pass
        if len(missileXY) != 0:
            for bx, by in missileXY:
                drawOject(missile, bx, by)

        writeScore(shotCount)
        # font = pygame.font.Font('resource\\NanumGothic.ttf', 20)
        # text = font.render('Destroyed No. : ' + str(shotCount), True, (255, 255, 255))
        # gamePad.blit(text, (10, 10))

        rockY += rockSpeed
        if rockY > padHeight:
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            rockPassed += 1
        if rockPassed == 3: gameOver()

        writePassed(rockPassed)

        if isShot:
            drawOject(explosion, rockX, rockY)
            destroySound.play()
            # sleep(0.3)
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            destroySound = pygame.mixer.Sound(random.choice(explosionSound))
            isShot = False
            rockSpeed += 0.02
            if rockSpeed>10: rockSpeed=10
            # shotCount += 1
        else:
            drawOject(rock, rockX, rockY)

        pygame.display.update()
        clock.tick(60)
    pygame.quit()


initGame()
runGame()
