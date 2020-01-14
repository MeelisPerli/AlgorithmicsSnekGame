import pygame
from map import *
from snake import *
from geneticalgorithm import *
from matrixoperations import *
from userinterface import *
import pylab

pygame.init()
screen = pygame.display.set_mode((800, 420))
lines = []
#  you can change the input model here, but keep the input_shape as (7,)
# and final layer output as 4 or whatever you have as dimensions.
# extra params for Snake in compilation:
#  - loss_fun
#  - opt
#  - metrics


fig = pylab.figure(figsize=[2, 2],  # Inches
                   dpi=100,  # 100 dots per inch, so the resulting buffer is 400x400 pixels
                   )

font = pygame.font.Font('freesansbold.ttf', 14)
text = font.render('Generation: ' + str(0)
                   + " \nAverage fitness: " + str(0)
                   + "\n Best fitness: " + str(0), True, (255, 255, 255), (255, 255))
textRect = text.get_rect()
textRect.center = (620, 360)

gen = 0
longest = []
avgs = []
reallydone = False
testSnakes = [Snake(1) for _ in range(20)]
games = 1
gameCounter = 0
snakesPerRound = len(testSnakes) // games
m = [Map(200, 200, 2, 100) for _ in range(games)]
UI = UserInterface(m, screen)
ga = GeneticAlgorithm()

while not reallydone:
    print("iteration", gen, end='\n')
    for i in range(games):
        m[i].nextRound(testSnakes[i * snakesPerRound:(i + 1) * snakesPerRound])
    testSnakes = []

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done, reallydone = True, True
            UI.handleEvents(event)
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, 800, 120))
        UI.draw(screen)
        m[0].drawGrid(screen, 10, 10)
        pygame.display.flip()
        for map in m:
            s = None
            # if all dead, returns the list of dead snakes
            # and terminates the game list
            if map.snakesLeft > 0:
                s = map.update()

            if s is not None:
                testSnakes += s
                gameCounter += 1
            if gameCounter == games:
                gameCounter = 0
                done = True

    long, avg = ga.mutate_snakes(testSnakes, 4, 7, 0.1)
    longest.append(long)
    avgs.append(avg)
    if len(longest) == 100:
        longest = longest[1:]
        avgs = avgs[1:]
    lines.append(UI.showPlots(screen, longest, avgs, fig, i, avg, font, textRect, lines))

    gen += 1
    if gen > 1000:
        reallydone = True
