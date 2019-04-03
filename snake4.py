import random
import time
import pygame
import threading


def findParameter(stringFromFile, name, default):
    ble = f"{name}:"
    stringSize = len(stringFromFile)
    start = stringFromFile.find(ble, 0, stringSize)
    if start != -1:
        start += len(ble)
        end = stringFromFile.find(";", start, stringSize)
    else:
        end = -1
    if end != -1:
        try:
            value = stringFromFile[start:end]
        except:
            value = default
    else:
        value = default
        print(name + " not defined. using Default value.")

    return value


def createApple(thisWorld):
    appleX = random.randint(0, worldWdth - 1)
    appleY = random.randint(0, worldHgth - 1)
    thisWorld[appleX][appleY] = -1


# try to import settings from file
try:
    thisFile = open("settings.txt", "r")
    stringFromFile = thisFile.read()
    thisFile.close()
except:
    stringFromFile = ""

if stringFromFile == "":
    print("loading settings.txt failed.")
else:
    print("loading settings.txt succesfull.")
# ---


worldWdth = int(findParameter(stringFromFile, "worldWdth", 15))
worldHgth = int(findParameter(stringFromFile, "worldHgth", 15))
startLength = int(findParameter(stringFromFile, "snakeLength", 1))
stepDelay = int(findParameter(stringFromFile, "stepDelay", 100))
thisSeed = int(findParameter(stringFromFile, "seed", 9001))
worldBorder = int(findParameter(stringFromFile, "worldBorder", 24))
squareSize = int(findParameter(stringFromFile, "squareSize", 12))
mode = int(findParameter(stringFromFile, "mode", 0))

random.seed(thisSeed)

print(f"mode:{mode} worldSize:{worldWdth}x{worldHgth}={worldWdth * worldHgth} startingScore:{startLength} randomSeed:{thisSeed}")

# create window
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Verdana', 18)
textOffset = worldWdth * squareSize + worldBorder * 2
window = pygame.display.set_mode((textOffset + 300, worldHgth * squareSize + worldBorder * 2))
pygame.display.set_caption("Snake")


class windowThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True  # daemon threads terminates when main thread is terminated

    def run(self):

        global headDir, headX, headY, score, step, hunger

        def createworld():

            global world, headX, headY, headDir, score, step, hunger

            world = []
            for x in range(0, worldWdth):
                thisRow = [0] * worldHgth
                world.append(thisRow)

            createApple(world)

            headX = round(worldWdth / 2)
            headY = round(worldHgth / 2)
            headDir = 0
            step = 0
            score = startLength
            hunger = 0

        createworld()

        timeLeft = 0

        gameover = False
        while True:

            if mode == 0:
                if gameover:
                    exit()
            else:
                thisBrain.checkScore(score)

                if gameover:

                    print(f"gameover. step:{step} score:{score}")
                    gameover = False
                    createworld()
                    thisBrain.mutate(0.025)
            # ---

            startTime = time.time()
            step += 1
            hunger += 1

            if hunger >= 100:
                textGamestate = myfont.render(f"You starved to death after {step} steps", False, (0, 0, 0))
                gameover = True

            elif (headX < 0) or (headX >= worldWdth) or (headY < 0) or (headY >= worldHgth):

                textGamestate = myfont.render(f"You hit the wall after {step} steps", False, (0, 0, 0))
                gameover = True

            elif world[headX][headY] > 0:

                textGamestate = myfont.render(f"You bit yourself after {step} steps", False, (0, 0, 0))
                gameover = True

            else:

                textGamestate = myfont.render(f'Step:{step}', False, (0, 0, 0))

                # if new snakeHead is on an apple increment score and spawn new apple
                if world[headX][headY] == -1:
                    score += 1
                    hunger = 0
                    createApple(world)
                # ---

                # add snake element at snakeHeadPos
                world[headX][headY] = score
            # ---

            window.fill((80, 80, 80))

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

                    # decrease snakeFelder wenn nicht gameover
                    if thisvalue > 0 and not gameover:
                        world[x][y] = thisvalue - 1
                    # ---

                    thisX = worldBorder + squareSize * x
                    thisY = worldBorder + squareSize * y

                    pygame.draw.rect(window, thisColor, (thisX, thisY, squareSize, squareSize))
            # ---


            # update text
            window.blit(textGamestate, (textOffset, worldBorder))

            txt_hunger = myfont.render(f'Hunger:{hunger}/100', False, (0, 0, 0))
            window.blit(txt_hunger, (textOffset, worldBorder + 20))

            txt_score = myfont.render(f'Score:{score}', False, (0, 0, 0))
            window.blit(txt_score, (textOffset, worldBorder + 40))

            txt_delay = myfont.render(f'stepDelay:{stepDelay}ms (+/- to adjust)', False, (0, 0, 0))
            window.blit(txt_delay, (textOffset, worldBorder + 70))

            txt_time = myfont.render(f"stepDelay - execTime = {timeLeft}ms", False, (0, 0, 0))
            window.blit(txt_time, (textOffset, worldBorder + 90))
            # ---


            pygame.display.update()

            # get brain input
            if mode >= 1:
                headDir = thisBrain.think(world)
            # ---

            # move snakeHeadPos in headDir
            if headDir == 0:
                headX += 1
                # print("right")
            elif headDir == 1:
                headY -= 1
                # print("up")
            elif headDir == 2:
                headX -= 1
                # print("left")
            else:
                headY += 1
                # print("down")
            # ---

            # wait until execTime >= stepDelay
            timeLeft = int(stepDelay - (time.time() - startTime) * 1000)

            if timeLeft > 0:
                pygame.time.delay(timeLeft)
            # ---
# ---


class BrainClass:

    def __init__(self, filename):

        self.lyrs = []
        self.file = filename

        # try to open brain.txt
        try:
            brainFile = open(self.file, "r")
            lines = brainFile.readlines()

            brainFile.close()
            print(f"loading {self.file} succesfull.")

        except:
            lines = ["", "", ""]
            print(f"loading {self.file} failed.")
        # ---



        self.inputWdth = int(findParameter(lines[0], "inputWdth", -1))
        self.inputHgth = int(findParameter(lines[1], "inputHgth", -1))
        self.bestScore = int(findParameter(lines[2], "bestScore", -1))




        inc = 0
        for thisstring in lines[3:]:

            thisLine = findParameter(thisstring, f"lyr{inc}", -1)
            inc += 1
            thisLyr = [[float(i) for i in x.strip(" []").split(",")] for x in thisLine.strip('[]').split("],")]

            self.lyrs.append(thisLyr)


    def think(self, thisWorld):

        outputs = []

        for x in range(worldWdth):
            for y in range(worldHgth):
                inputValue = thisWorld[x][y]
                outputs.append(inputValue)
        # ---

        for thisLyr in self.lyrs:

            inputs = outputs.copy()
            outputs = []

            for thisNode in thisLyr:

                inc = 0
                outPutValue = 0

                for thisWeigth in range(len(thisNode)):
                    inputValue = inputs[inc]
                    inc += 1
                    weigth = thisNode[thisWeigth]
                    outPutValue += inputValue * weigth

                outputs.append(outPutValue)
        # ---

        index_max = max(range(len(outputs)), key=outputs.__getitem__)

        return index_max

    def addLayer(self, nodes, inputs):
        newLayer = []
        for n in range(nodes):
            newNode = []
            for i in range(inputs):
                newNode.append(0)
            newLayer.append(newNode)
        self.lyrs.append(newLayer)

    def savetofile(self):

        # try to create brain.txt
        try:
            brainFile = open(self.file, "w+")
            inputWdth = worldWdth
            inputHgth = worldHgth

            brainFile.write(f"inputWdth:{inputWdth};\n")
            brainFile.write(f"inputHgth:{inputHgth};\n")
            brainFile.write(f"bestScore:{self.bestScore};\n")


            for inc in range(len(self.lyrs)):
                brainFile.write(f"lyr{inc}:{self.lyrs[inc]};\n")

            brainFile.close()

            print(f"brain saved in {self.file}")

        except:
            exit(f"writing to {self.file} failed.")
        # ---

    def randomize(self):
        for x in range(len(self.lyrs)):
            for y in range(len(self.lyrs[x])):
                for z in range(len(self.lyrs[x][y])):
                    self.lyrs[x][y][z] = random.uniform(-1, 1)
        # ---
        print("brain randomized")


    def mutate(self, power):
        for x in range(len(self.lyrs)):
            for y in range(len(self.lyrs[x])):
                for z in range(len(self.lyrs[x][y])):
                    self.lyrs[x][y][z] += random.uniform(-power, power)


    def checkScore(self, newScore):

        if self.bestScore < newScore:
            print(f"new bestScore: {newScore}")
            self.bestScore = newScore
            self.savetofile()
# ---


ugga = 0

if mode == 0:
    ugga = 2
elif mode == 1:
    thisBrain = BrainClass("brain.txt")

    if len(thisBrain.lyrs) == 0:
        thisBrain.addLayer(200, worldWdth * worldHgth)
        thisBrain.addLayer(100, 200)
        thisBrain.addLayer(90, 100)
        thisBrain.addLayer(80, 90)
        thisBrain.addLayer(70, 80)
        thisBrain.addLayer(60, 70)
        thisBrain.addLayer(50, 60)
        thisBrain.addLayer(40, 50)
        thisBrain.addLayer(30, 40)
        thisBrain.addLayer(20, 30)
        thisBrain.addLayer(10, 20)
        thisBrain.addLayer(4, 10)
        thisBrain.randomize()

    ugga = 2
# ---


thread1 = windowThread()
thread1.start()

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

            if mode == 0:
                if thisEvent.key == pygame.K_RIGHT or thisEvent.key == 100:
                    headDir = 0
                if thisEvent.key == pygame.K_UP or thisEvent.key == 119:
                    headDir = 1
                if thisEvent.key == pygame.K_LEFT or thisEvent.key == 97:
                    headDir = 2
                if thisEvent.key == pygame.K_DOWN or thisEvent.key == 115:
                    headDir = 3
            else:
                if thisEvent.key == pygame.K_1:
                    thisBrain.savetofile()

    stepDelay = max(stepDelay, 0)
