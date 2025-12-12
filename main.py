import pygame
from src.window import Window

FPS = 60

def main():
    window = Window(current_scene="menu")

    while window.running:
        window.handle_events()
        window.update()
        window.draw()
        pygame.time.Clock().tick(FPS)


if __name__ == "__main__":
    main()

    # Map Kernel Testing Code

    # from src.GameLogic import GameLogic
    # from src.Map import Map, StaticMapState
    # import numpy as np

    # l = GameLogic()
    # l.scenario.map = Map([5, 5], [
    #       {"id": 0, "pos": [0,0]},
    #       {"id": 1, "pos": [0,0]},
    #       {"id": 2, "pos": [0,0]}], [{"id": 3, "pos": [0,0]},
    #       {"id": 4, "pos": [0,0]},
    #       {"id": 5, "pos": [0,0]}])
    # l.scenario.map.static_map = np.array([[1, 0, 0, 0, 0],
    #                                       [0, 1, 0, 0, 0],
    #                                       [0, 0, 1, 0, 0],
    #                                       [0, 0, 0, 1, 0],
    #                                       [0, 0, 0, 0, 1]], dtype=StaticMapState)

    # k = l.build_kernel([1, 2], 0)
    # print(k)
