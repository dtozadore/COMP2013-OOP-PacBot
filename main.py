from src.window import Window


def main():
    window = Window(current_scene="menu")

    while window.running:
        window.handle_events()
        window.update()
        window.draw()


if __name__ == "__main__":
    main()

    # Map Kernel Testing Code

    # from src.GameLogic import GameLogic
    # from src.Map import Map, StaticMapState
    # import numpy as np

    # l = GameLogic()
    # l.map = Map([5, 5], [], [])
    # l.map.static_map = np.array([[1, 0, 0, 0, 0],
    #                              [0, 1, 0, 0, 0],
    #                              [0, 0, 1, 0, 0],
    #                              [0, 0, 0, 1, 0],
    #                              [0, 0, 0, 0, 1]], dtype=StaticMapState)

    # k = l.build_kernel([1, 3], 0)
    # print(k)
