import pygame
import pandas as pd

from map import *
from snake import *
from geneticalgorithm import *
from matrixoperations import *
from userinterface import *

class SnakeGame():

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 420))

        # variables.
        self.number_of_snakes = 20
        self.number_of_food_per_map = 40
        self.parallel_games = 1  # make sure that the number of snakes is divisible by it

        # GA variables
        # make sure that 2 * parent_pairs + children_per_parent_pair * parent_pairs <= number_of_snakes
        # if the sum is less than the number of snakes, then the empty spots will be filled up with new snakes
        self.parent_pairs = 3
        self.children_per_parent_pair = 4
        self.mut_chance = 0.1
        # # tell to use n snakes for recall from previous random game
        # self.recall = 0

        # info about each game
        self.snakes = [Snake(1) for _ in range(self.number_of_snakes)]
        self.maps = [Map(100, 100, 4, self.number_of_food_per_map) for _ in range(self.parallel_games)]
        self.snakes_per_round = len(self.snakes) // self.parallel_games
        self.snake_data = []

        # info about the generations
        self.gen = 0
        self.longest = []
        self.avgs = []

        # general stuff
        self.rec_path = "games/"
        self.model_name = "brain3_1_"
        self.UI = UserInterface(self.maps, self)
        self.GA = GeneticAlgorithm()
        self.DONE = False

    def start(self):
        while not self.DONE:
            print("iteration", self.gen, end='\n')
            # iterate through n parallel games and create them
            for i in range(self.parallel_games):
                self.maps[i].nextRound(self.snakes[i * self.snakes_per_round:(i + 1) * self.snakes_per_round])
            # workhorse
            self.mainloop()

    def mainloop(self):
        view = 0
        gameCounter = 0
        dead_snakes = []
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.DONE = True
                    break
                self.UI.handleEvents(event)
            # resets screen and draws
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(0, 0, 800, 120))
            self.UI.draw(self.screen)

            # makes it show active map
            while self.maps[view].snakesLeft == 0 and view < self.parallel_games:
                view += 1
            self.maps[view].drawGrid(self.screen, 10, 10)
            pygame.display.flip()

            # logic
            for map in self.maps:
                s = None
                # if all dead, returns the list of dead snakes
                # and terminates the game list
                if map.snakesLeft > 0:
                    s = map.update()

                if s is not None:
                    dead_snakes += s
                    gameCounter += 1

                if gameCounter == self.parallel_games:
                    done = True

        self.make_new_snakes(dead_snakes)
        for snek in dead_snakes:
            self.snake_data.append([
                self.gen,
                snek.brain_num,
                snek.size,
                snek.lifeSpan,
                snek.beenAlive,
                snek.size - 3 + round(snek.beenAlive / 1000, 3) - snek.deathPenalty
            ])

    def make_new_snakes(self, dead_snakes):
        self.snakes = dead_snakes
        long, avg = self.GA.mutate_snakes(self.snakes, self.parent_pairs, self.children_per_parent_pair,
                                          self.mut_chance)
        self.longest.append(long)
        self.avgs.append(avg)
        if len(self.longest) == 100:
            self.longest = self.longest[1:]
            self.avgs = self.avgs[1:]

        self.gen += 1
        self.UI.showPlots(self.screen, self.longest, self.avgs, self.gen, avg)

    def save_all_models(self):
        c = 0
        pd.DataFrame(self.snake_data,
                     columns=[
                         'generation',
                         'snake_brain_num',
                         'snake_size',
                         'snake_lifespan_left',
                         'snake_lifespan',
                         'snake_fitness'
                     ]).to_csv(self.rec_path + self.model_name + "stats.csv"),

        for m in self.maps:
            m.saveSnakes(self.rec_path + self.model_name, c)
            c += self.number_of_food_per_map

    def load_all_models(self):
        snakes = []
        path = self.rec_path
        for (dirpath, dirnames, filenames) in os.walk(path):
            for i, file in enumerate(filenames):
                snakes.append(Snake(file=path + file))

        self.snakes = snakes
        self.number_of_snakes = len(self.snakes)
        self.snakes_per_round = self.number_of_snakes // self.parallel_games
        self.gen = 0
        self.longest = []
        self.avgs = []
        print("Models loaded!")
        self.start()
        self.UI.showPlots(self.screen, self.longest, self.avgs, 0, 0)

game = SnakeGame()
game.start()
