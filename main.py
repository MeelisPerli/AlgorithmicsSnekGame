from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import pygame
from map import *
from snake import *

# The idea is to have m games and n snakes in every game to run at the same time.
# Once all snakes are dead (across all the games), they are improved with a Generic algorithm
# map. Update method returns all the dead snakes from a game once that game finishes (None otherwise)
# The dead snakes need to be evaluated. Maybe use their size or lifetime as a metric. Use the best to
# get new weights for the neural network. DO NOT CREATE NEW SNAKES during/after the Genetic algorithm.
# New snakes should only be created at the beginning (this reduces the amount of garbage). Just swap out
# their brains.

pygame.init()
screen = pygame.display.set_mode((420, 420))
done = False
m = Map(100, 100, 4)

# you can change the input model here,
# or define new standard in Snake._createNewBrain()
# extra params for Snake in compilation:
#  - loss_fun
#  - opt
#  - metrics
model = [
    Dense(12, input_dim = 1, activation = 'relu'),
    Dense(8, input_dim = 12, activation = 'relu'),
    Dense(1, activation = 'sigmoid')
]

testSnakes = [Snake(brain = model) for _ in range(1)]
m.nextRound(testSnakes, 50)
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pygame.display.flip()
    deadSnakes = m.update()
    m.drawGrid(screen, 10, 10)
