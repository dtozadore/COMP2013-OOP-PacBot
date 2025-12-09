import pygame
import sys

class Window():
    def __init__(self, width:int=800, height:int=600, title:str="Game"):
        pygame.init()
        self.width = width
        self.height = height
        self.title = title
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.running = True

    def update(self):
        pygame.display.update()

    def draw(self):
        pass

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()