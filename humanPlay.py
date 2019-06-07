import time
import pygame
import threading

from imports import findParameter
from imports import GameClass



worldWdth = int(findParameter("settings.txt", "worldWdth", 15))
worldHgth = int(findParameter("settings.txt", "worldHgth", 15))
startLength = int(findParameter("settings.txt", "snakeLength", 3))
stepDelay = int(findParameter("settings.txt", "stepDelay", 125))
worldBorder = int(findParameter("settings.txt", "worldBorder", 24))
squareSize = int(findParameter("settings.txt", "squareSize", 12))



thisGame = GameClass(worldWdth, worldHgth, startLength)


# create pygame window
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Verdana', 18)
textOffset = worldWdth * squareSize + worldBorder * 2
window = pygame.display.set_mode((textOffset + 350, worldHgth * squareSize + worldBorder * 2), pygame.RESIZABLE)
pygame.display.set_caption("Snake with human input")
# ---

class windowThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True  # daemon threads terminates when main thread is terminated

    def run(self):

        timeLeft = 0
        startTime = time.time()

        while True:

            window.fill((80, 80, 80))

            # draw text
            if thisGame.state == 1:
                txt_state = myfont.render(f"You starved to death in step {thisGame.step}", False, (0, 0, 0))
            elif thisGame.state == 2:
                txt_state = myfont.render(f"You hit the wall after {thisGame.step} steps", False, (0, 0, 0))
            elif thisGame.state == 3:
                txt_state = myfont.render(f"You bit yourself after {thisGame.step} steps", False, (0, 0, 0))
            else:
                txt_state = myfont.render(f'Step:{thisGame.step}', False, (0, 0, 0))

            window.blit(txt_state, (textOffset, worldBorder))

            txt_hunger = myfont.render(f'Hunger:{thisGame.hunger}/50', False, (0, 0, 0))
            window.blit(txt_hunger, (textOffset, worldBorder + 20))

            txt_score = myfont.render(f'Score:{thisGame.score}', False, (0, 0, 0))
            window.blit(txt_score, (textOffset, worldBorder + 40))

            txt_delay = myfont.render(f'stepDelay:{stepDelay}ms (+/- to adjust)', False, (0, 0, 0))
            window.blit(txt_delay, (textOffset, worldBorder + 70))

            txt_time = myfont.render(f"stepDelay - execTime = {timeLeft}ms", False, (0, 0, 0))
            window.blit(txt_time, (textOffset, worldBorder + 90))
            # ---

            # draw world
            for x in range(0, thisGame.worldWdth):
                for y in range(0, thisGame.worldHgth):
                    thisvalue = thisGame.world[x][y]

                    if thisvalue == thisGame.score:
                        thisColor = (255, 0, 0)
                    elif thisvalue > 0:
                        thisColor = (255, 255, 255)
                    elif thisvalue == 0:
                        thisColor = (0, 0, 0)
                    else:
                        thisColor = (0, 255, 0)

                    # decrease snakeFelder wenn nicht gameover
                    if thisvalue > 0:
                        thisGame.world[x][y] = thisvalue - 1
                    # ---

                    thisX = worldBorder + squareSize * x
                    thisY = worldBorder + squareSize * y

                    pygame.draw.rect(window, thisColor, (thisX, thisY, squareSize, squareSize))
            # ---

            pygame.display.update()

            if thisGame.state != 0:
                break

            # wait until execTime >= stepDelay
            timeLeft = int(stepDelay - (time.time() - startTime) * 1000)

            if timeLeft > 0:
                pygame.time.delay(timeLeft)
            # ---

            startTime = time.time()

            thisGame.nextstep()
# ---


thisThread = windowThread()
thisThread.name = "windowthread"
thisThread.start()

ugga = 2
while ugga != 0:

    for thisEvent in pygame.event.get():

        if thisEvent.type == pygame.QUIT:
            ugga = 0
            print("Programm ist durch den Benutzer beendet worden.")

        if thisEvent.type == pygame.KEYDOWN:
            if thisEvent.key == pygame.K_KP_PLUS:
                stepDelay += 25
                print(f"stepdelay: {stepDelay}")
            if thisEvent.key == pygame.K_KP_MINUS:
                stepDelay -= 25
                print(f"stepdelay: {stepDelay}")

            if thisEvent.key == pygame.K_RIGHT or thisEvent.key == 100:
                thisGame.headDir = 0
            if thisEvent.key == pygame.K_UP or thisEvent.key == 119:
                thisGame.headDir = 1
            if thisEvent.key == pygame.K_LEFT or thisEvent.key == 97:
                thisGame.headDir = 2
            if thisEvent.key == pygame.K_DOWN or thisEvent.key == 115:
                thisGame.headDir = 3

    stepDelay = max(stepDelay, 0)
