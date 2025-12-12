from src.Map import Direction
from pathlib import Path


class Sprite():
    def __init__(self, name: str,
                 x: int = 0,
                 y: int = 0,
                 direction: Direction = Direction.UP,
                 animate: bool = False,
                 animation_idx: int = 0,
                 animation_speed: int = 1,
                 animation_frames: list[Path] = []):
        self.name = name
        self.x = x
        self.y = y
        self.direction = direction
        self.animate = animate
        self.animation_idx = animation_idx
        self.animation_speed = animation_speed
        self.animation_frames = animation_frames

    def update(self):
        pass

    def draw(self):
        pass

    def update_animation(self):
        pass
