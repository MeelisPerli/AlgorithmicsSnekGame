from button import *
import matplotlib

matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg


class UserInterface():

    def __init__(self, map, screen):
        self.clickedToggle = False
        self.map = map
        self.saveButton = Button(430, 20, 80, 20, "Save", map.saveSnakes)
        self.loadButton = Button(430, 60, 80, 20, "Load", map.loadSnakes)

    def handleEvents(self, event):
        self.saveButton.handleEvent(event)
        self.loadButton.handleEvent(event)

    def draw(self, screen):
        self.saveButton.draw(screen)
        self.loadButton.draw(screen)

    def showPlots(self, screen, longest, fig, gen, avg, font, textRect, lines):
        ax = fig.gca()

        if lines:
            ax.lines.pop()

        line = ax.plot(longest)
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()

        surf = pygame.image.fromstring(raw_data, size, "RGB")
        screen.blit(surf, (430, 140))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(430, 350, 220, 20))
        text = font.render('Gen: ' + str(gen)
                           + "Avg: " + str(round(avg, 2))
                           + "Best: " + str(longest[-1]), True, (255, 255, 255), (255, 255))
        screen.blit(text, textRect)

        return line
        # pygame.display.flip()
