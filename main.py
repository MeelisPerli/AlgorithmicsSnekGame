import pygame
from map import *
from snake import *
from geneticalgorithm import *
from matrixoperations import *
from userinterface import *
import pylab

# The idea is to have m games and n snakes in every game to run at the same time.
# Once all snakes are dead (across all the games), they are improved with a Generic algorithm
# map. Update method returns all the dead snakes from a game once that game finishes (None otherwise)
# The dead snakes need to be evaluated. Maybe use their size or lifetime as a metric. Use the best to
# get new weights for the neural network. DO NOT CREATE NEW SNAKES during/after the Genetic algorithm.
# New snakes should only be created at the beginning (this reduces the amount of garbage). Just swap out
# their brains.

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

i = 0
longest = []
reallydone = False
testSnakes = [Snake(1) for _ in range(40)]
m = Map(200, 200, 2, 300)
UI = UserInterface(m, screen)
ga = GeneticAlgorithm()

for snake in testSnakes:
    snake.randomize_weights()

while not reallydone:
    print("iteration", i, end='\n')
    m.nextRound(testSnakes)
    testSnakes = None
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done, reallydone = True, True
            UI.handleEvents(event)
        UI.draw(screen)
        pygame.display.flip()
        #  if all dead, returns the list of dead snakes
        # and terminates the game list
        testSnakes = m.update()
        if testSnakes is not None:
            done = True
        m.drawGrid(screen, 10, 10)

    long, avg = ga.mutate_snakes(testSnakes, 6, 10, 0.1)
    longest.append(long)
    if len(longest) == 30:
        longest = longest[1:]
    lines.append(UI.showPlots(screen, longest, fig, i, avg, font, textRect, lines))

    i += 1
    if i > 1000:
        reallydone = True
