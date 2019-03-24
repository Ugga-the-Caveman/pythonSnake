import pygame
import numpy
import random


worldWdth = 80
worldHgth = 60
squareSize = 12
windowBorder = 24
score = 1
step = 0
stepDelay = 100

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
window = pygame.display.set_mode((worldWdth * squareSize + windowBorder * 2, worldHgth * squareSize + windowBorder * 2))
pygame.display.set_caption("Snake")
#---



#prepare text
pygame.font.init()
myfont = pygame.font.SysFont('Verdana', 18)
#---



run = 2
while run == 2:

    pygame.time.delay(stepDelay)
    step += 1

    #stop loop on exit button
    for thisEvent in pygame.event.get():
        if thisEvent.type == pygame.QUIT:
            run = 0
    #---


    #register keypress
    keys = pygame.key.get_pressed()

    if keys[pygame.K_KP_PLUS]:
        stepDelay += 25
    if keys[pygame.K_KP_MINUS]:
        stepDelay -= 25
    stepDelay = max(stepDelay, 0)


    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        headDir = 0

    if keys[pygame.K_UP] or keys[pygame.K_w]:
        headDir = 1

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        headDir = 2

    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        headDir = 3
    #---


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

    #if snake is inside worldArea and has not biten itself
    if (headX >= 0) and (headX < worldWdth) and (headY >= 0) and (headY < worldHgth) and world[headX][headY] <= 0:

        # if new snakeHead is on an apple increment score and spawn new apple
        if world[headX][headY] == -1:
            score += 1
            appleX = random.randint(0, worldWdth - 1)
            appleY = random.randint(0, worldHgth - 1)
            world[appleX][appleY] = -1
        # ---

        #add snake element at new snakeHeadPos
        world[headX][headY] = score



        # update score
        textsurface = myfont.render(f'stepDelay:{stepDelay}ms length:{score} Step:{step}', False, (0, 0, 0))
        window.blit(textsurface, (windowBorder, 0))
        # ---

    else:

        run = 1

        # show final score
        textsurface = myfont.render(f'Game Over. length:{score} Steps:{step}', False, (0, 0, 0))
        window.blit(textsurface, (windowBorder, 0))
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

    pygame.display.update()

if run == 0:
    exitReason = "Spiel verloren."
else:
    exitReason = "Spiel ist durch den Benutzer beendet worden."

    # stop loop on exit button
    while run == 1:
        for thisEvent in pygame.event.get():
            if thisEvent.type == pygame.QUIT:
                run = 0
    # ---


print(exitReason)

for x in world:
    print(*x, sep=" ")

print(f'length:{score} Steps:{step}')