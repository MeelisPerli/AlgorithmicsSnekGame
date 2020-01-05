import pygame
from map import *

# The idea is to have m games and n snakes in every game to run at the same time.
# Once all snakes are dead (across all the games), they are improved with a Generic algorithm
# map.Update method returns all the dead snakes from a game once that game finishes (None otherwise)
# The dead snakes need to be evaluated. Maybe use their size or lifetime as a metric. Use the best to
# get new weights for the neural network. DO NOT CREATE NEW SNAKES during/after the Genetic algorithm.
# New snakes should only be created at the beginning (this reduces the amount of garbage). Just swap out
# their brains.



pygame.init()
screen = pygame.display.set_mode((800, 600))
done = False
m = Map(200, 200, 2)
testSnakes = [Snake() for _ in range(200)]
m.nextRound(testSnakes, 100)
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pygame.display.flip()
    m.update()
    m.drawGrid(screen, 10, 10)
