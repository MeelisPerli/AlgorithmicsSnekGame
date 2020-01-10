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

# you can change the input model here, but keep the input_shape as (7,)
# and final layer output as 4 or whatever you have as dimensions.
# extra params for Snake in compilation:
#  - loss_fun
#  - opt
#  - metrics
model = [
    Dense(14, input_shape = (7,), activation = 'relu'),
    Dense(9, input_dim = 7, activation = 'relu'),
    Dense(4, activation = 'softmax')
]

i = 0
reallydone = False
testSnakes = [Snake(brain = model) for _ in range(5)]
while not reallydone:
    print("iteration", i, end = '\n')

    m = Map(100, 100, 4)
    m.nextRound(testSnakes, 10)
    testSnakes = None
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done, reallydone = True, True

        pygame.display.flip()
        # if all dead, returns the list of dead snakes
        # and terminates the game list
        testSnakes = m.update()
        if testSnakes != None:
            done = True
        m.drawGrid(screen, 10, 10)

    # TODO:
    # play with dead snakes
    sizetable, maxsize, minsize = [], 0, np.inf
    n = 0
    for snake in testSnakes:
        sizetable.append([snake.size, snake])
        if snake.size > maxsize:
            maxsize = snake.size
        if snake.size < minsize:
            minsize = snake.size

        n += 1
        print(n, "-th snake had size: ", snake.size)

    testSnakes = [Snake(brain = model) if snake.size == minsize else snake for snake in testSnakes ]

    i += 1
    if i > 100:
        reallydone = True
