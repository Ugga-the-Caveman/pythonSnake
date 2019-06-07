import threading
import ctypes
import copy

from imports import findParameter
from imports import GameClass
from imports import BrainClass



brainFile = input("Enter brain file: ")

# try to open file
try:
    thisFile = open(brainFile, "r")
    lines = thisFile.readlines()
    thisFile.close()
except FileNotFoundError:
    exit("File not Found")
# ---

worldWdth = int(findParameter(brainFile, "inputWdth", 10))
worldHgth = int(findParameter(brainFile, "inputHgth", 10))
startLength = int(findParameter(brainFile, "startLength", 1))

protoBrain = BrainClass(worldWdth, worldHgth, startLength)

protoBrain.games = int(findParameter(brainFile, "gamesPlayed", 0))
protoBrain.bestScore = int(findParameter(brainFile, "bestScore", startLength))
protoBrain.avgScore = float(findParameter(brainFile, "avgScore", startLength))

firstLyrLine = 0
for thisLine in lines:
    if thisLine.find("layers:") == -1:
        firstLyrLine += 1
    else:
        break

inc = 0
for thisLine in lines[firstLyrLine + 1:]:
    thisString = f"lyr{inc}:"
    inc += 1

    start = thisLine.find(thisString)
    end = thisLine.find(";")
    arrayString = thisLine[start + len(thisString):end]

    thisLyr = [[float(i) for i in x.strip(" []").split(",")] for x in arrayString.strip('[]').split("],")]
    protoBrain.lyrs.append(thisLyr)


if len(protoBrain.lyrs) == 0:
    exit("Brain has no layers.")

popSize = int(input("population Size: "))
gameCount = int(input("Nr. of Games: "))


population = []

for inc in range(popSize):

    thisBrain = copy.deepcopy(protoBrain)
    thisBrain.randomize()
    population.append(thisBrain)

    for y in range(gameCount):

        thisGame = GameClass(worldWdth, worldHgth, startLength)

        while True:
            # decrease snakeFelder
            for x in range(0, thisGame.worldWdth):
                for y in range(0, thisGame.worldHgth):
                    thisvalue = thisGame.world[x][y]
                    if thisvalue > 0:
                        thisGame.world[x][y] = thisvalue - 1
            # ---

            if thisGame.state != 0:

                thisBrain.evaluateGame(thisGame)

                break

            else:

                thisBrain.think(thisGame)

                thisGame.nextstep()






bestBrain = population[0]
for thisBrain in population:
    if bestBrain.avgScore < thisBrain.avgScore:
        bestBrain = thisBrain
print(f"best avgScore: {bestBrain.avgScore}")

antwort = ctypes.windll.user32.MessageBoxW(0, f"save best brain into {brainFile}?", "Save Brain?", 4)
if antwort == 6:
    bestBrain.save(brainFile)
