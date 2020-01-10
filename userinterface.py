from button import *


class UserInterface():

    def __init__(self, map):
        self.map = map
        self.saveButton = Button(430, 20, 80, 20, "Save", map.saveSnakes)
        self.loadButton = Button(430, 60, 80, 20, "Load", map.loadSnakes)

    def handleEvents(self, event):
        self.saveButton.handleEvent(event)
        self.loadButton.handleEvent(event)

    def draw(self, screen):
        self.saveButton.draw(screen)
        self.loadButton.draw(screen)
