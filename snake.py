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

        if file != "":
            self.load(file)

        self.parts = deque()
        self.lifeSpan = 0
        self.alive = False
        self.lastDir = 0
        self.size = 0
        self.randomize_weights()  # need it to assign random biases

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

    def brain1(self):
        inp = Input((7,))
        d1 = Dense(14, activation='relu')(inp)
        d2 = Dense(9, activation='relu')(d1)
        d3 = Dense(4, activation='softmax')(d2)
        self.model = Sequential(input=inp, output=d3)

    def brain2(self):
        self.model = Sequential()
        self.model.add(Input(shape=(5, 5, 1)))  # 9,9, 1
        self.model.add(Conv2D(5, (3, 3), padding='same', activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2), trainable=False))
        self.model.add(Flatten(trainable=False))
        self.model.add(Dense(6, activation='relu'))
        self.model.add(Dense(4, activation='softmax'))

    # idk if this is required anymore
    def randomize_weights(self):
        w = self.genes()
        v = mat_to_vector(w)

        for i in range(len(v[0])):
            v[0][i] = random.random() * 2 - 1
        nw = vector_to_mat(v, w)
        bias = mat_to_vector(self.biases())
        biases = [random.uniform(-1, 1) for a in bias[0]]
        b = vector_to_mat([biases], self.biases())
        self.setGenes(nw, b)

    # Returns if the snake is still alive.
    def step(self, grid):
        if not self.alive:
            return False
        elif self.lifeSpan <= 0:
            return self.die(grid)

        #### TODO: input tuning
        #### right now:
        #  sitrep = [(item (0, 1, 2) at:) left, up, right, down,
        #           (nearest food loc_x - x, loc_y - y) x, y, (snake length) len]
        # ... total 7 elements
        # NB: also need to reshape it (flip it) to have 7 features, not 7 instances

        # Uncomment the next 2 lines, if u want to use the other snake
        # sitrep = grid.sitrep((self))
        # pred = self.model.predict(np.asarray(sitrep).reshape(1, len(sitrep)))

        # comment these 2 if you uncommented the previous 2 lines
        sitrep = grid.areaAt(self.parts[0][0], self.parts[0][1], 2)  # shape (9,9,1)
        input = grid.getInput(self.parts[0][0], self.parts[0][1])  # shape (3,4,2)
        pred = self.model.predict([[sitrep]])

        self._move(np.argmax(pred), grid)

        return True

    # moves the last part of the snake in front of it in direction dir
    # 0: up
    # 1: right
    # 2: down
    # 3: left
    def _move(self, dir, grid):
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
        for x, y in self.parts:
            grid.grid[x][y] = 0
        return False

    # Makes the snek big
    def _grow(self, grid):
        self.parts.append(self.parts[-1])
        self.lifeSpan += 50
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
