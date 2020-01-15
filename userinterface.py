from button import *
import matplotlib
import pylab
import pygame

matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg


class UserInterface():

    def __init__(self, maps, main):
        self.clickedToggle = False
        self.maps = maps
        self.saveButton = Button(430, 20, 80, 20, "Save", maps[0].saveSnakes)
        self.loadButton = Button(430, 60, 80, 20, "Load", maps[0].loadSnakes)
        self.font = pygame.font.SysFont("Arial", 20)
        self.fig = pylab.figure(figsize=[2, 2],  # Inches
                                dpi=100,  # 100 dots per inch, so the resulting buffer is 400x400 pixels
                                )

    def handleEvents(self, event):
        self.saveButton.handleEvent(event)
        self.loadButton.handleEvent(event)

    def draw(self, screen):
        self.saveButton.draw(screen)
        self.loadButton.draw(screen)
        self.displaySnakeCount(screen)


    def showPlots(self, screen, longest, avgs, gen, avg):
        ax = self.fig.gca()
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(430, 200, 400, 200))
        ax.plot(longest)
        ax.plot(avgs)
        canvas = agg.FigureCanvasAgg(self.fig)
        canvas.draw()

        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()

        surf = pygame.image.fromstring(raw_data, size, "RGB")
        screen.blit(surf, (430, 140))

        s = 'Gen: ' + str(gen) + " Avg: " + str(round(avg, 2)) + " Best: " + str(longest[-1])
        text = self.font.render(s, True, (255, 255, 255), (255, 255))
        screen.blit(text, (430, 340))

    def displaySnakeCount(self, screen):
        c = 0
        for map in self.maps:
            c += map.snakesLeft
        self.text("Snakes left: " + str(c), screen, 430, 100)

    def text(self, text, screen, x, y):
        t = self.font.render(text, True, (255, 255, 255))
        screen.blit(t, (x, y))


    def save_all_models(self):
        path = "games/model"
        c = 0
        for m in self.maps:
            m.saveSnakes(path + str(c) + ".h5")