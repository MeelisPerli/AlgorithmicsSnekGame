from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from collections import deque
import random
import pygame


class Snake():

    def __init__(self, brain=None):
        if brain is None:
            self.brain = None  # self._createNewBrain()
        else:
            self.brain = brain

        self.parts = deque()
        self.lifeSpan = 0
        self.alive = False
        self.lastDir = 0
        self.size = 0

    def init(self, x, y, initialLen=3, lifeSpan=300):
        # Using a deque to store snake's parts
        # First element is the head.
        self.parts = deque()
        for i in range(initialLen):
            self.parts.append((x, y))

        self.lifeSpan = lifeSpan
        self.alive = True
        self.lastDir = 0
        self.size = initialLen

    def swapBrain(self, newBrain):
        self.brain = newBrain

    def getBrain(self):
        return self.brain

    # TODO: improve the neural network
    def _createNewBrain(self):
        model = Sequential()
        model.add(Dense(12, input_dim=8, activation='relu'))
        model.add(Dense(8, activation='relu'))
        model.add(Dense(4, activation='sigmoid'))
        model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
        return model

    # Returns if the snake is still alive.
    # TODO replace the random movement with outputs from the model
    def step(self, grid):
        if not self.alive:
            return False
        elif self.lifeSpan <= 0:
            return False

        direction = random.randint(0, 3)
        self._move(direction, grid)

        return True

    # moves the last part of the snake in front of it in direction dir
    # 0: up
    # 1: right
    # 2: down
    # 3: left
    def _move(self, dir, grid):
        x = self.parts[0][0]
        y = self.parts[0][1]
        self.lastDir = dir
        if dir == 0:
            y -= 1
        elif dir == 1:
            x += 1
        elif dir == 2:
            y += 1
        else:
            x -= 1

        # If the snake tries to go back, then it goes forward
        if (x, y) == self.parts[1]:
            return self._move((dir + 2) % 4, grid)

        # wall/snake part check
        if not grid.isInGrid(x, y) or grid.at(x, y) == 1:
            return self.die(grid)

        # food check
        if grid.at(x, y) == 2:
            self._grow(grid)

        # moves the snake's tail in front
        part = self.parts.pop()
        grid.grid[part[0]][part[1]] = 0
        part = (x, y)
        grid.grid[x][y] = 1
        self.parts.appendleft(part)
        return True

    # On death all parts will be replaced by empty tiles.
    # This can be changed to food
    def die(self, grid):
        self.alive = False
        for x, y in self.parts:
            grid.grid[x][y] = 0
        return False

    # Makes the snek big
    def _grow(self, grid):
        self.parts.append(self.parts[-1])
        self.lifeSpan += 50
        self.size += 1
        grid.addFood(1)

    def draw(self, screen, gridX, gridY, cellSize):
        for x, y in self.parts:
            pygame.draw.rect(screen, (50, 10, 255),
                             pygame.Rect(gridX + x * cellSize, gridY + y * cellSize, cellSize, cellSize))
