from snake import *
import os


# tile info:
# 0: empty tile
# 1: snake
# -1: food

# A grid based map.
class Map():

    def __init__(self, x, y, cellSize, nOfFood):
        self.x = x
        self.y = y
        self.cellSize = cellSize
        self._initialize_grid()
        self.nOfFood = nOfFood
        self.snakesLeft = 0

    def nextRound(self, snakes):
        self.aliveSnakes = snakes
        # clearing the map
        self._initialize_grid()

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
        self.addFood(self.nOfFood)
        self.snakesLeft = len(self.aliveSnakes)
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
                self.snakesLeft -= 1
                self.deadSnakes.append(snake)

        self.aliveSnakes = alive
        if self.snakesLeft > 0:
            return None

        return self.deadSnakes

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
        for X in range(r * 2 + 1):
            for Y in range(r * 2 + 1):
                area[X][Y][0] = self.safeAt(x - r + X, y - r + Y)

        return area

    def getInput(self, x, y):
        i = np.ones((3, 4, 2))
        i[0, 0, 0], i[0, 0, 1] = self.InRowRight(x, y, -1)
        i[0, 1, 0], i[0, 1, 1] = self.InRowLeft(x, y, -1)

        i[0, 2, 0], i[0, 2, 1] = self.InColumnUp(x, y, -1)
        i[0, 3, 0], i[0, 3, 1] = self.InColumnDown(x, y, -1)

        i[1, 0, 0], i[1, 0, 1] = self.InRowLeft(x, y, 1)
        i[1, 1, 0], i[1, 1, 1] = self.InRowRight(x, y, 1)

        i[1, 2, 0], i[1, 2, 1] = self.InColumnUp(x, y, 1)
        i[1, 3, 0], i[1, 3, 1] = self.InColumnDown(x, y, 1)

        i[2, 0, 0], i[2, 0, 1] = self.x - x, x
        i[2, 1, 0], i[2, 1, 1] = x, self.x

        i[2, 2, 0], i[2, 2, 1] = y, self.y
        i[2, 3, 0], i[2, 3, 1] = self.y - y, y
        # print(i)

        return i

    def InRowLeft(self, x, y, val, lim=-1):
        if lim == -1:
            lim = 0
        else:
            lim = x - lim
        for i in range(x - 1, lim, -1):
            if self.safeAt(i, y) == val:
                return 1, x - i
        return -1, -1

    def InRowRight(self, x, y, val, lim=-1):
        if lim == -1:
            lim = self.x
        else:
            lim = x + lim
        for i in range(x + 1, lim):
            if self.safeAt(i, y) == val:
                return 1, i - x
        return -1, -1

    def InColumnUp(self, x, y, val, lim=-1):
        if lim == -1:
            lim = 0
        else:
            lim = y - lim
        for i in range(y - 1, lim, -1):
            if self.safeAt(x, i) == val:
                return 1, y - i
        return -1, -1

    def InColumnDown(self, x, y, val, lim=-1):
        if lim == -1:
            lim = self.y
        else:
            lim = y + lim
        for i in range(y + 1, lim):
            if self.safeAt(x, i) == val:
                return 1, i - y
        return -1, -1

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

    def addFood(self, n):
        while n > 0:
            x = random.randint(1, self.x - 1)
            y = random.randint(1, self.y - 1)
            self.grid[x][y] = -1
            n -= 1

    def drawGrid(self, screen, xOnScreen=0, yOnScreen=0):
        pygame.draw.rect(screen, (255, 255, 255),
                         pygame.Rect(xOnScreen, yOnScreen, self.cellSize * self.x, self.cellSize * self.y))
        for y in range(self.y):
            for x in range(self.x):
                if self.at(x, y) == -1:
                    pygame.draw.rect(screen, (0, 255, 0),
                                     pygame.Rect(xOnScreen + x * self.cellSize, yOnScreen + y * self.cellSize,
                                                 self.cellSize, self.cellSize))

        for snake in self.aliveSnakes:
            snake.draw(screen, xOnScreen, yOnScreen, self.cellSize)

    def isInGrid(self, x, y):
        return 0 <= x < self.x and 0 <= y < self.y

    def at(self, x, y):
        return self.grid[x][y]

    #  edit: added safer query for inputs
    def safeAt(self, x, y):
        if self.isInGrid(x, y):
            return self.grid[x][y]
        else:
            return 1

    def saveSnakes(self, path, game):
        i = 0
        for s in self.aliveSnakes:
            s.save(path + str(int(game + i)) + ".h5")
            i += 1
        for s in self.deadSnakes:
            s.save(path + str(int(game + i)) + ".h5")
            i += 1
        print("Models saved!")
