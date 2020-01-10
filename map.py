import pygame
import random
import numpy as np
from snake import *


# tile info:
# 0: empty tile
# 1: snake
# -1: food

# A grid based map.
class Map():

    def __init__(self, x, y, cellSize):
        self.x = x
        self.y = y
        self.cellSize = cellSize
        self._initialize_grid()

    def nextRound(self, snakes, nOfFood):
        self.aliveSnakes = snakes

        # letting the snakes loose
        for snake in self.aliveSnakes:
            # no do-while loop in python :(
            while True:
                x = random.randint(1, self.x - 1)
                y = random.randint(1, self.y - 1)
                if self.at(x, y) == 0:
                    break
            snake.init(x, y)

        # adding food to the map
        self.addFood(nOfFood)

        self.deadSnakes = []

    def _initialize_grid(self):
        self.grid = [[0] * self.x for i in range(self.y)]

    def sitrep(self, snake):
        #  access head
        head = snake.parts[0]
        return [self.safeAt(head[0] - 1, head[1]),
                self.safeAt(head[0] + 1, head[1]),
                self.safeAt(head[0], head[1] - 1),
                self.safeAt(head[0], head[1] + 1),
                *self.closestFood(*head),
                snake.size]

    def areaAt(self, x, y, r):
        area = np.ones((r * 2 + 1, r * 2 + 1, 1))
        for X in range(r*2 + 1):
            for Y in range(r*2 + 1):
                area[X][Y][0] = self.safeAt(x-r+X, y-r+Y)
        return area


    #  spiraling out algorithm (sorta) for finding closest food tile to x, y
    def closestFood(self, x, y):
        for i in range(1, np.max((self.x, self.y))):
            #  interweave horizontal sides
            spiral = np.empty((i * 2 - 1,), dtype=int)
            spiral[0::2] = np.arange(y, y - i, -1)
            spiral[1::2] = np.arange(y + 1, y + i)

            # look at horizontal sides (and check if both points are still in grid)
            if self.isInGrid(x - i, y - i) or self.isInGrid(x - i, y + i):
                for nx, ny in zip([x - i] * len(spiral), spiral):
                    if self.safeAt(nx, ny) == -1:
                        return x - nx, y - ny

            if self.isInGrid(x + i, y - i) or self.isInGrid(x + i, y + i):
                for nx, ny in zip([x + i] * len(spiral), spiral):
                    if self.safeAt(nx, ny) == -1:
                        return x - nx, y - ny

            #  interweave vertical sides
            spiral[0::2] = np.arange(x, x - i, -1)
            spiral[1::2] = np.arange(x + 1, x + i)

            #  look at vertical sides
            if self.isInGrid(x - i, y - i) or self.isInGrid(x + i, y - i):
                for nx, ny in zip(spiral, [y - i] * len(spiral)):
                    if self.safeAt(nx, ny) == -1:
                        return x - nx, y - ny

            if self.isInGrid(x - i, y + i) or self.isInGrid(x + i, y + i):
                for nx, ny in zip(spiral, [y + i] * len(spiral)):
                    if self.safeAt(nx, ny) == -1:
                        return x - nx, y - ny
        return np.inf, np.inf

    # If all snakes are dead, then returns them. Otherwise None
    def update(self):
        alive = []
        for snake in self.aliveSnakes:
            if snake.step(self):
                alive.append(snake)
            else:
                self.deadSnakes.append(snake)

        self.aliveSnakes = alive
        if len(alive) > 0:
            return None

        return self.deadSnakes

    def addFood(self, n):
        while n > 0:
            x = random.randint(1, self.x - 1)
            y = random.randint(1, self.y - 1)
            self.grid[x][y] = -1
            n -= 1

    def drawGrid(self, screen, xOnScreen=0, yOnScreen=0):
        for y in range(self.y):
            for x in range(self.x):
                if self.at(x, y) == 0:
                    pygame.draw.rect(screen, (255, 255, 255),
                                     pygame.Rect(xOnScreen + x * self.cellSize, yOnScreen + y * self.cellSize,
                                                 self.cellSize, self.cellSize))
                if self.at(x, y) == -1:
                    pygame.draw.rect(screen, (0, 255, 0),
                                     pygame.Rect(xOnScreen + x * self.cellSize, yOnScreen + y * self.cellSize,
                                                 self.cellSize, self.cellSize))

        for snake in self.aliveSnakes:
            snake.draw(screen, xOnScreen, yOnScreen, self.cellSize)

    def isInGrid(self, x, y):
        return -1 <= x < self.x and -1 <= y < self.y

    def at(self, x, y):
        return self.grid[x][y]

    #  edit: added safer query for inputs
    def safeAt(self, x, y):
        if self.isInGrid(x, y):
            return self.grid[x][y]
        else:
            return 1
