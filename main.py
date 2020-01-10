from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, BatchNormalization, Input, Conv2D, MaxPooling2D, Flatten
import pygame
from map import *
from snake import *
from geneticalgorithm import *

# The idea is to have m games and n snakes in every game to run at the same time.
# Once all snakes are dead (across all the games), they are improved with a Generic algorithm
# map. Update method returns all the dead snakes from a game once that game finishes (None otherwise)
# The dead snakes need to be evaluated. Maybe use their size or lifetime as a metric. Use the best to
# get new weights for the neural network. DO NOT CREATE NEW SNAKES during/after the Genetic algorithm.
# New snakes should only be created at the beginning (this reduces the amount of garbage). Just swap out
# their brains.

pygame.init()
screen = pygame.display.set_mode((420, 420))

#  you can change the input model here, but keep the input_shape as (7,)
# and final layer output as 4 or whatever you have as dimensions.
# extra params for Snake in compilation:
#  - loss_fun
#  - opt
#  - metrics
model = [
    Dense(14, input_shape=(7,), activation='relu'),
    Dense(9, activation='relu'),
    Dense(4, activation='softmax')
]

model2 = [
    Input(shape=(5, 5, 1)),
    Conv2D(5, (3, 3), padding='same', activation='relu'),
    MaxPooling2D(pool_size=(2, 2), trainable=False),
    Flatten(trainable=False),
    Dense(6, activation='relu'),
    Dense(4, activation='softmax')
]

i = 0
reallydone = False
testSnakes = [Snake(brain=model2) for _ in range(50)]
ga = GeneticAlgorithm(testSnakes)
while not reallydone:
    print("iteration", i, end='\n')

    m = Map(200, 200, 2)
    m.nextRound(testSnakes, 100)
    testSnakes = None
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done, reallydone = True, True

        pygame.display.flip()
        #  if all dead, returns the list of dead snakes
        # and terminates the game list
        testSnakes = m.update()
        if testSnakes is not None:
            done = True
        m.drawGrid(screen, 10, 10)

    #  TODO:
    #  play with dead snakes

    ga.mutate_snakes(3, 2, 1, 0.2)

    i += 1
    if i > 100:
        reallydone = True
