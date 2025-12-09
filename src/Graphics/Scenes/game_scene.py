import pygame
from src.Graphics.scene_manager import SceneManager

class GameScene():
    def __init__(self, scene_manager: SceneManager):
        self.scene_manager = scene_manager

    def handle_events(self, events:list[pygame.event.Event]):
        pass

    def update(self):
        pass

    def draw(self):
        pass