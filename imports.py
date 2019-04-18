import random
import sys


def findParameter(fileName, thisString, defaultValue):

    # try to open file
    try:
        thisFile = open(fileName, "r")
        lines = thisFile.readlines()
        thisFile.close()
    except:
        print(f"this exception occured while opening {fileName}: ", sys.exc_info())
        lines = []
    # ---


    thisValue = ""

    for thisLine in lines:
        start = thisLine.find(f"{thisString}:")
        end = thisLine.find(";")

        if start >= 0 and end != -1:
            thisValue = thisLine[start+len(f"{thisString}:"):end]
            print(f"reading  {thisString}:{thisValue}  from  {fileName}")
            break

    if thisValue.replace(" ", "") == "":
        print(f"can not find {thisString} in {fileName}. using defaultValue:{defaultValue}")
        thisValue = defaultValue

    return thisValue
# ---


class GameClass:
    def __init__(self, worldWdth, worldHgth, startLength):

        self.worldWdth = worldWdth
        self.worldHgth = worldHgth
        self.startLength = startLength

        self.world = []
        self.headX = 0
        self.headY = 0
        self.headDir = 0
        self.hunger = 0
        self.step = 0
        self.score = 0
        self.state = 0

        self.restart()

    def createApple(self):
        appleX = random.randint(0, self.worldWdth - 1)
        appleY = random.randint(0, self.worldHgth - 1)
        self.world[appleX][appleY] = -1

    def restart(self):

        self.world = []
        for x in range(0, self.worldWdth):
            thisRow = [0] * self.worldHgth
            self.world.append(thisRow)

        self.headX = (self.worldWdth // 2)
        self.headY = (self.worldHgth // 2)
        self.headDir = 0
        self.step = 0
        self.score = self.startLength
        self.hunger = 0
        self.state = 0

        self.world[self.headX][self.headY] = self.score

        self.createApple()

    def nextstep(self):

        self.step += 1

        # move snakeHeadPos in headDir
        if self.headDir == 0:
            self.headX += 1
        elif self.headDir == 1:
            self.headY -= 1
        elif self.headDir == 2:
            self.headX -= 1
        else:
            self.headY += 1
        # ---

        if self.hunger > 50:
            self.state = 1

        elif (self.headX < 0) or (self.headX >= self.worldWdth) or (self.headY < 0) or (self.headY >= self.worldHgth):
            self.state = 2

        elif self.world[self.headX][self.headY] > 0:
            self.state = 3

        else:

            # if new snakeHead is on an apple increment score and spawn new apple
            if self.world[self.headX][self.headY] == -1:
                self.score += 1
                self.hunger = 0
                self.createApple()
            else:
                self.hunger += 1
            # ---

            # add snake element at snakeHeadPos
            self.world[self.headX][self.headY] = self.score
        # ---
# ---


class BrainClass:

    def __init__(self):

        self.inputWdth = 13
        self.inputHgth = 13
        self.startLength = 1
        self.lyrs = []
        self.bestScore = 1
        self.games = 0
        self.avgScore = 1

    def evaluateGame(self, thisGame):

        if self.bestScore < thisGame.score:
            print(f"new highScore in game {self.games}!")
            self.bestScore = thisGame.score

        s = self.avgScore * self.games
        y = ((s / (self.games + 1)) + (thisGame.score / (self.games + 1))) - self.avgScore

        self.avgScore += y
        self.games += 1


    def think(self, thisGame):

        outputs = []

        for x in range(thisGame.worldWdth):
            for y in range(thisGame.worldHgth):
                inputValue = thisGame.world[x][y]
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
        thisGame.headDir = index_max

    def addLayer(self, nodes):
        newLayer = []

        if len(self.lyrs) == 0:
            inputSize = self.inputHgth * self.inputWdth
        else:
            inputSize = len(self.lyrs[-1])

        for n in range(nodes):
            newNode = []
            for i in range(inputSize):
                newNode.append(0)
            newLayer.append(newNode)
        self.lyrs.append(newLayer)

    def load(self, fileName):

        # try to open file
        try:
            thisFile = open(fileName, "r")
            lines = thisFile.readlines()
            thisFile.close()
        except:
            print(f"this exception occured while opening {fileName}: ", sys.exc_info())
            lines = []
        # ---

        self.inputWdth = int(findParameter(fileName, "inputWdth", 13))
        self.inputHgth = int(findParameter(fileName, "inputHgth", 13))
        self.startLength = int(findParameter(fileName, "startLength", 1))

        self.games = int(findParameter(fileName, "gamesPlayed", 0))
        self.bestScore = int(findParameter(fileName, "bestScore", self.startLength))
        self.avgScore = float(findParameter(fileName, "avgScore", self.startLength))

        firstLyrLine = 0
        for thisLine in lines:
            if thisLine.find("layers:") == -1:
                firstLyrLine += 1
            else:
                break

        inc = 0
        for thisLine in lines[firstLyrLine+1:]:

            thisString = f"lyr{inc}:"
            inc += 1

            start = thisLine.find(thisString)
            end = thisLine.find(";")
            arrayString = thisLine[start + len(thisString):end]

            thisLyr = [[float(i) for i in x.strip(" []").split(",")] for x in arrayString.strip('[]').split("],")]
            self.lyrs.append(thisLyr)


    def save(self, fileName):

        # try to create brain.txt
        try:
            thisFile = open(fileName, "w+")

            thisFile.write(f"inputWdth:{self.inputWdth};\n")
            thisFile.write(f"inputHgth:{self.inputHgth};\n")
            thisFile.write(f"startLength:{self.startLength};\n")
            thisFile.write(f"gamesPlayed:{self.games};\n")
            thisFile.write(f"bestScore:{self.bestScore};\n")
            thisFile.write(f"avgScore:{self.avgScore};\n")

            layercount = len(self.lyrs)
            thisFile.write(f"layers:{layercount};\n")
            for inc in range(layercount):
                thisFile.write(f"lyr{inc}:{self.lyrs[inc]};\n")

            thisFile.close()

            print(f"brain saved in {fileName}")

        except:

            exit(f"writing to {fileName} failed.", sys.exc_info())
        # ---


    def randomize(self):
        for x in range(len(self.lyrs)):
            for y in range(len(self.lyrs[x])):
                for z in range(len(self.lyrs[x][y])):
                    self.lyrs[x][y][z] = random.uniform(-1, 1)
        # ---
        print("brain randomized")


