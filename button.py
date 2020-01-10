import pygame


class Button():

    def __init__(self, x, y, sideX, sideY, text, funct):
        self.x = x
        self.y = y
        self.sideX = sideX
        self.sideY = sideY
        font = pygame.font.SysFont("Arial", 20)
        self.text = font.render(text, True, (0, 0, 0))
        self.functionToCall = funct

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.x <= mouse_pos[0] <= self.x + self.sideX and self.y <= mouse_pos[1] <= self.y + self.sideY:
                self.functionToCall()

    def draw(self, screen):
        pygame.draw.rect(screen, (120, 120, 120), pygame.Rect(self.x, self.y, self.sideX, self.sideY))
        pygame.draw.rect(screen, (90, 90, 90), pygame.Rect(self.x + 2, self.y + 2, self.sideX - 4, self.sideY - 4))
        screen.blit(self.text, ((self.x + self.sideX // 4), self.y - 2))