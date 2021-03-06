from tensorflow.keras.models import Sequential, load_model, save_model
from tensorflow.keras.layers import Dense, BatchNormalization, Input, Conv2D, MaxPooling2D, Flatten
from collections import deque
import numpy as np
import random
import pygame
from matrixoperations import *


def softmaxer(inp):
    e = np.exp(inp - np.max(inp))
    return e / np.sum(e)


class Snake():

    def __init__(self, brain=2, file=""):
        if brain == 1:
            self.brain1()
        elif brain == 2:
            self.brain2()
        elif brain == 3:
            self.brain3()
        self.brain_num = brain

        if file != "":
            self.load(file)

        self.parts = deque()
        self.lifeSpan = 0
        self.beenAlive = 0
        self.alive = False
        self.lastDir = 0
        self.size = 0
        #self.randomize_weights()  #last time i checked, it wasn't needed anymore
        self.deathPenalty = 0

    def init(self, x, y, initialLen=3, lifeSpan=100):
        # Using a deque to store snake's parts
        # First element is the head.
        self.parts = deque()
        for i in range(initialLen):
            self.parts.append((x, y))

        self.lifeSpan = lifeSpan
        self.alive = True
        self.lastDir = 0
        self.size = initialLen
        self.deathPenalty = 0
        self.beenAlive = 0

    def brain1(self):
        self.model = Sequential()
        self.model.add(Input(shape=(17,)))
        self.model.add(Dense(20, activation='tanh'))
        self.model.add(Dense(10, activation='tanh'))
        self.model.add(Dense(4, activation='softmax'))

    def brain2(self):
        self.model = Sequential()
        self.model.add(Input(shape=(20,)))
        self.model.add(Dense(26, activation='tanh'))
        self.model.add(Dense(13, activation='tanh'))
        self.model.add(Dense(4, activation='softmax'))

    def brain3(self):
        self.model = Sequential()
        self.model.add(Input(shape=(7,)))
        self.model.add(Dense(9, activation='relu'))
        self.model.add(Dense(15, activation='relu'))
        self.model.add(Dense(4, activation='softmax'))

    # idk if this is required anymore
    def randomize_weights(self):
        w = self.genes()
        v = mat_to_vector(w)
        for i in range(len(v)):
            v[i] = random.random() * 2 - 1
        nw = vector_to_mat(v, w)

        bias = self.biases()
        bv = mat_to_vector(bias)
        for i in range(len(bv)):
            bv[i] = random.random() * 2 - 1
        b = vector_to_mat(bv, bias)
        self.setGenes(nw, b)

    # Returns if the snake is still alive.
    def step(self, grid):
        if not self.alive:
            return False
        elif self.lifeSpan <= 0:
            r = self.die(grid)
            self.deathPenalty = 0
            return r
        self.beenAlive += 1
        #### TODO: input tuning

        if self.brain_num == 1:
            head = self.parts[0]
            input = []
            # distance to items and if can be found
            sides = [grid.InRowLeft(head[0], head[1], 1, 10), grid.InRowRight(head[0], head[1], 1, 10),
                     grid.InColumnUp(head[0], head[1], 1, 10), grid.InColumnDown(head[0], head[1], 1, 10),
                     grid.InRowLeft(head[0], head[1], -1, 10), grid.InRowRight(head[0], head[1], -1, 10),
                     grid.InColumnUp(head[0], head[1], -1, 10), grid.InColumnDown(head[0], head[1], -1, 10)]
            for i in sides:
                input.append(i[0])
                input.append(i[1])
            # moving dir
            input.append(self.lastDir)
            pred = self.model.predict([input])

        elif self.brain_num == 2:
            head = self.parts[0]
            input = []
            # distance to items and if can be found
            sides = [grid.InRowLeft(head[0], head[1], 1, 10), grid.InRowRight(head[0], head[1], 1, 10),
                     grid.InColumnUp(head[0], head[1], 1, 10), grid.InColumnDown(head[0], head[1], 1, 10),
                     grid.InRowLeft(head[0], head[1], -1, 10), grid.InRowRight(head[0], head[1], -1, 10),
                     grid.InColumnUp(head[0], head[1], -1, 10), grid.InColumnDown(head[0], head[1], -1, 10)]
            for i in sides:
                input.append(i[0])
                input.append(i[1])
            # moving dir
            for i in range(4):
                if i == self.lastDir:
                    input.append(1)
                else:
                    input.append(0)
            pred = self.model.predict([input])

        elif self.brain_num == 3:
            sitrep = grid.sitrep((self))
            pred = self.model.predict(np.asarray(sitrep).reshape(1, len(sitrep)))

        self._move(np.argmax(pred), grid)

        return True

    # moves the last part of the snake in front of it in direction dir
    # 0: up
    # 1: right
    # 2: down
    # 3: left
    def _move(self, dir, grid):
        self.lastDir = dir
        self.lifeSpan -= 1
        x = self.parts[0][0]
        y = self.parts[0][1]
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

        # removes the tail
        part = self.parts.pop()
        grid.grid[part[0]][part[1]] = 0

        # wall/snake part check
        if not grid.isInGrid(x, y) or grid.at(x, y) == 1:
            return self.die(grid)

        # food check
        if grid.at(x, y) == -1:
            self._grow(grid)

        # adds a new segment in front of the head
        part = (x, y)
        grid.grid[x][y] = 1
        self.parts.appendleft(part)
        return True

    # On death all parts will be replaced by empty tiles.
    # This can be changed to food
    def die(self, grid):
        self.alive = False
        self.deathPenalty = 3
        for x, y in self.parts:
            grid.grid[x][y] = 0
        return False

    # Makes the snek big
    def _grow(self, grid):
        self.parts.append(self.parts[-1])
        self.lifeSpan += 100
        self.size += 1
        grid.addFood(1)

    #  convinience methods for accessing models and weights.
    def swapBrain(self, newBrain):
        self.model = newBrain

    def getBrain(self):
        return self.model

    # It now takes into account only the trainable layers
    def setGenes(self, genes, biases):
        c = 0
        for layer in self.model.layers:
            if not layer.get_config()['trainable']:
                continue
            layer.set_weights([genes[c], biases[c]])
            c += 1

    #  the goto weight getter
    def genes(self):
        return [layer.get_weights()[0] for layer in self.model.layers if layer.get_config()['trainable']]

    def biases(self):
        return [layer.get_weights()[1] for layer in self.model.layers if layer.get_config()['trainable']]

    def configs(self):
        return [layer.get_configs() for layer in self.model.layers]

    def save(self, path):
        self.model.save(path)

    def load(self, path):
        self.model = load_model(path)

    def draw(self, screen, gridX, gridY, cellSize):
        for x, y in self.parts:
            pygame.draw.rect(screen, (50, 10, 255),
                             pygame.Rect(gridX + x * cellSize, gridY + y * cellSize, cellSize, cellSize))

        pygame.draw.rect(screen, (255, 0, 0),
                         pygame.Rect(gridX + self.parts[0][0] * cellSize, gridY + self.parts[0][1] * cellSize, cellSize,
                                     cellSize))
