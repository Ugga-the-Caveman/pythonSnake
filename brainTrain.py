import threading
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
    lines = []
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



class TrainThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.keeprunning = True

    def run(self):

        bestBrain = protoBrain
        generation = 0

        while True:

            if not self.keeprunning:
                print(f"Training thread stopped in generation {generation}")

                print(f"best avgScore: {bestBrain.avgScore}")

                print("Enter filename to save best Brain. Enter empty string if you don't want to save.")
                ble = False
                while not ble:
                    filename = input("Enter filename: ")

                    if filename.replace(" ", "") != "":
                        ble = bestBrain.save(filename)
                    else:
                        ble = True
                break
            else:
                generation += 1
            # ---

            population = [bestBrain]

            for popIndex in range(popSize - 1):

                if not self.keeprunning:
                    print(f"stopped @ popIndex {popIndex}/{popSize}")
                    break

                thisBrain = copy.deepcopy(bestBrain)
                thisBrain.mutate(0.01, 0.0042)

                for gameIndex in range(gameCount):

                    if not self.keeprunning:
                        print(f"stopped @ gameIndex {gameIndex}/{gameCount}")
                        break

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
                # ---

                population.append(thisBrain)

            # ---

            if self.keeprunning:
                for thisBrain in population:
                    if bestBrain.avgScore < thisBrain.avgScore:
                        bestBrain = thisBrain

                print(f"Generation {generation} completed. Highscore: {bestBrain.bestScore} avg: {bestBrain.avgScore}")
    # ---




thisThread = TrainThread()
thisThread.start()

input("Training started. Hit enter to stop.\n")
thisThread.keeprunning = False
