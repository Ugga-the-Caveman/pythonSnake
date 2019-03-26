import random
import time
import numpy
import pygame

#try to import settings from file
try:
    thisFile = open("settings.txt", "r")
    stringFromFile = thisFile.read()
    stringSize = len(stringFromFile)-1
except:
    print("cannot open settings.txt")
    stringFromFile = ""
finally:
    thisFile.close()
#---


start = stringFromFile.find("worldWdth:", 0, stringSize)
if start != -1:
    start += len("worldWdth:")
    end = stringFromFile.find(";", start, stringSize)
else:
    end = -1
if end != -1:
    try:
        worldWdth = int(stringFromFile[start:end])
    except:
        worldWdth = 20
else:
    worldWdth = 20
    print("worldWdth not defined")


start = stringFromFile.find("worldHgth:", 0, stringSize)
if start != -1:
    start += len("worldHgth:")
    end = stringFromFile.find(";", start, stringSize)
else:
    end = -1
if end != -1:
    try:
        worldHgth = int(stringFromFile[start:end])
    except:
        worldHgth = 20
else:
    worldHgth = 20
    print("worldHgth not defined")


start = stringFromFile.find("snakeLength:", 0, stringSize)
if start != -1:
    start += len("snakeLength:")
    end = stringFromFile.find(";", start, stringSize)
else:
    end = -1
if end != -1:
    try:
        score = int(stringFromFile[start:end])
    except:
        score = 1
else:
    score = 1
    print("snakeLength not defined")


start = stringFromFile.find("stepDelay:", 0, stringSize)
if start != -1:
    start += len("stepDelay:")
    end = stringFromFile.find(";", start, stringSize)
else:
    end = -1
if end != -1:
    try:
        stepDelay = int(stringFromFile[start:end])
    except:
        stepDelay = 100
else:
    stepDelay = 100
    print("stepDelay not defined")


start = stringFromFile.find("seed:", 0, stringSize)
if start != -1:
    start += len("seed:")
    end = stringFromFile.find(";", start, stringSize)
else:
    end = -1
if end != -1:
    try:
        thisSeed = int(stringFromFile[start:end])
    except:
        thisSeed = 9001
else:
    thisSeed = 9001
    print("seed not defined")



start = stringFromFile.find("windowBorder:", 0, stringSize)
if start != -1:
    start += len("windowBorder:")
    end = stringFromFile.find(";", start, stringSize)
else:
    end = -1
if end != -1:
    try:
        windowBorder = int(stringFromFile[start:end])
    except:
        windowBorder = 24
else:
    windowBorder = 24
    print("windowBorder not defined")


start = stringFromFile.find("squareSize:", 0, stringSize)
if start != -1:
    start += len("squareSize:")
    end = stringFromFile.find(";", start, stringSize)
else:
    end = -1
if end != -1:
    try:
        squareSize = int(stringFromFile[start:end])
    except:
        squareSize = 12
else:
    squareSize = 12
    print("squareSize not defined")


step = 0

print(f"spiel gestartet. worldSize:{worldWdth}x{worldHgth}={worldWdth*worldHgth} startingScore:{score} seed:{thisSeed}")



random.seed(thisSeed)

#create empty world
world = numpy.full((worldWdth, worldHgth), 0)
#---


#place snake headPos in the middle of the world
headX = round(worldWdth / 2)
headY = round(worldHgth / 2)
headDir = 0
#---

#create first apple
appleX = random.randint(0, worldWdth - 1)
appleY = random.randint(0, worldHgth - 1)
world[appleX][appleY] = -1
#---


#create window
pygame.init()
boardsize = worldWdth * squareSize + windowBorder * 2
window = pygame.display.set_mode((boardsize + 300, worldHgth * squareSize + windowBorder * 2))
pygame.display.set_caption("Snake")
#---



#prepare text
pygame.font.init()
myfont = pygame.font.SysFont('Verdana', 18)
#---


run = 2
while run == 2:
    startTime = time.time()

    step += 1

    #stop loop on exit button
    for thisEvent in pygame.event.get():
        if thisEvent.type == pygame.QUIT:
            run = 0
    #---

    # register keypress
    keys = pygame.key.get_pressed()

    if keys[pygame.K_KP_PLUS]:
        stepDelay += 50
    if keys[pygame.K_KP_MINUS]:
        stepDelay -= 50
    stepDelay = max(stepDelay, 0)

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        headDir = 0

    if keys[pygame.K_UP] or keys[pygame.K_w]:
        headDir = 1

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        headDir = 2

    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        headDir = 3
    # ---

    # move snakeHeadPos in headDir
    if headDir == 0:
        headX += 1
    elif headDir == 1:
        headY -= 1
    elif headDir == 2:
        headX -= 1
    else:
        headY += 1
    # ---

    window.fill((80, 80, 80))

    if (headX < 0) or (headX >= worldWdth) or (headY < 0) or (headY >= worldHgth):

        textGamestate = myfont.render(f"You hit the wall after {step} steps", False, (0, 0, 0))
        run = 1

    elif world[headX][headY] > 0:

        textGamestate = myfont.render(f"You bit yourself after {step} steps", False, (0, 0, 0))
        run = 1

    else:

        textGamestate = myfont.render(f'Step:{step}', False, (0, 0, 0))

        # if new snakeHead is on an apple increment score and spawn new apple
        if world[headX][headY] == -1:
            score += 1
            appleX = random.randint(0, worldWdth - 1)
            appleY = random.randint(0, worldHgth - 1)
            world[appleX][appleY] = -1
        # ---

        #add snake element at new snakeHeadPos
        world[headX][headY] = score
    # ---


    # draw world
    for x in range(0, worldWdth):
        for y in range(0, worldHgth):
            thisvalue = world[x][y]

            if thisvalue == score:
                thisColor = (255, 0, 0)
            elif thisvalue > 0:
                thisColor = (255, 255, 255)
            elif thisvalue == 0:
                thisColor = (0, 0, 0)
            else:
                thisColor = (0, 255, 0)

            if thisvalue > 0 and run == 2:
                world[x][y] = thisvalue - 1

            thisX = windowBorder + squareSize * x
            thisY = windowBorder + squareSize * y

            pygame.draw.rect(window, thisColor, (thisX, thisY, squareSize, squareSize))
    # ---

    # update text
    window.blit(textGamestate, (boardsize, windowBorder))

    textstep = myfont.render(f'Score:{score}', False, (0, 0, 0))
    window.blit(textstep, (boardsize, windowBorder + 20))

    textscore = myfont.render(f'stepDelay:{stepDelay}ms (+/- to adjust)', False, (0, 0, 0))
    window.blit(textscore, (boardsize, windowBorder + 50))
    # ---

    #wait until execTime >= stepDelay
    timeLeft = int(stepDelay - (time.time() - startTime) * 1000)

    if timeLeft > 0:
        pygame.time.delay(timeLeft)

    textDelay = myfont.render(f"stepDelay - execTime = {timeLeft}ms", False, (0, 0, 0))
    window.blit(textDelay, (boardsize, windowBorder + 70))
    #---

    pygame.display.update()




if run == 1:
    exitReason = "Spiel verloren."

    # stop loop on exit button
    while run == 1:
        for thisEvent in pygame.event.get():
            if thisEvent.type == pygame.QUIT:
                run = 0
    # ---

else:
    exitReason = "Spiel ist durch den Benutzer beendet worden."


print(exitReason)
for y in range(0, worldHgth):
    string = ""
    for x in range(0, worldWdth):
        string += f" {world[x][y]}"
    print(string)

print(f'length:{score} Steps:{step}')
