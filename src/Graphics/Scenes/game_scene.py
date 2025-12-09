import pygame
from src.Graphics.Scenes.scene import Scene
from src.Graphics.scene_manager import SceneManager

class GameScene(Scene):
    def __init__(self, scene_manager: SceneManager):
        super().__init__(scene_manager)

    def handle_events(self, events:list[pygame.event.Event]):
        pass

    def update(self):
        pass

    def draw(self):
        pass