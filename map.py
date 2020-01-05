import pygame
import random
from snake import *


# tile info:
# 0: empty tile
# 1: snake
# 2: food

# A grid based map.
class Map():

    def __init__(self, x, y, cellSize):
        self.x = x
        self.y = y
        self.cellSize = cellSize
        self._initialize_grid()

    def nextRound(self, snakes):
        self.aliveSnakes = snakes

        # letting the snakes loose
        for snake in self.aliveSnakes:
            # no do-while loop in python :(
            while True:
                x = random.randint(1, self.x-1)
                y = random.randint(1, self.y-1)
                if self.at(x, y) == 0:
                    break
            snake.init(x, y)

        self.deadSnakes = []

    def _initialize_grid(self):
        self.grid = [[0] * self.x for i in range(self.y)]

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

    def drawGrid(self, screen, xOnScreen=0, yOnScreen=0):
        for y in range(self.y):
            for x in range(self.x):
                pygame.draw.rect(screen, (255, 255, 255),
                                 pygame.Rect(xOnScreen + x * self.cellSize, yOnScreen + y * self.cellSize,
                                             self.cellSize, self.cellSize))

        for snake in self.aliveSnakes:
            snake.draw(screen, xOnScreen, yOnScreen, self.cellSize)

    def isInGrid(self, x, y):
        return 0 <= x < self.x and 0 <= y < self.y

    def at(self, x, y):
        return self.grid[x][y]
