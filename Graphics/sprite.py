from direction import Direction
from pathlib import Path

class Sprite():
    def __init__(self, x:int=0, y:int=0, direction:Direction=Direction.UP, animate:bool=False, animation_speed:int=1, frame_path:Path=Path("pixel_art/na.png")):
        self.x = x
        self.y = y
        self.direction = direction
        self.animate = animate
        self.animation_idx = 0
        self.animation_speed = animation_speed
        self.animation_frames = {}

    def updateAnimation(self):
        pass
