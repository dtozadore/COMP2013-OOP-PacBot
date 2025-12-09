from enum import Enum
import numpy as np


def clamp(n, lo, hi):
    return max(lo, min(n, hi))


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Map:
    pass


class Entity:
    def update_view(self):
        pass

    def get_movement(self) -> Direction:
        return Direction.UP


class Window:
    pass


class GameLogic:
    def __init__(self, teleoperation_mode=False):
        self.map: Map
        self.pacbots: list[Entity] = []
        self.aliens: list[Entity] = []
        self.window: Window

        self.retrieved_survivors = 0
        self.remaining_pacbots = 3

        self.teleoperation_mode = teleoperation_mode
        pass

    def init_game(self):
        self.entities = []
        pass

    def update_game(self):
        # Update views of the entities (and allow communication)
        #  Also prevents desync where entites updated later on in the
        #  sequence see the new positions of those updated before them
        for entity in [*self.pacbots, *self.aliens]:
            entity.update_view()

        # Get desired movement for the aliens
        for i, entity in enumerate(self.aliens):
            desired_dir = entity.get_movement()

            # Check desired direction for wall collision
            new_pos = self.map.get_entity(len(self.pacbots) + i)
            if desired_dir == Direction.UP:
                new_pos[1] -= 1
            elif desired_dir == Direction.RIGHT:
                new_pos[0] += 1
            elif desired_dir == Direction.DOWN:
                new_pos[1] += 1
            elif desired_dir == Direction.LEFT:
                new_pos[0] -= 1

            new_pos[0] = clamp(new_pos[0], 0, self.map.width)
            new_pos[1] = clamp(new_pos[0], 0, self.map.height)

            if self.map.get(new_pos) > 1:
                # Is a wall -> invalid move
                continue

            self.map.set_entity(len(self.pacbots) + i, new_pos)

        # Check for custom collisions
        dead_pacbots = []
        for i, pacbot in enumerate(self.pacbots):
            # Picked up a survivor
            self_pos = self.map.get_entity(i)
            if self.map.get(self_pos) == MapTile.Survivor:
                pacbot.pickup_survivor()
                self.map.set(self_pos, MapTile.Survivor)

            for i in range(len(self.aliens)):
                # Overlap with an alien
                if self_pos == self.map.get(len(self.pacbots) + i):
                    # Remove the pacbot
                    dead_pacbots.append(i)
                    self.remaining_pacbots -= 1

                    # Replace the survivor on the map

        # Iterate backward to prevent indexing error
        for i in dead_pacbots[::-1]:
            self.pacbots[i] = []
            self.map.remove_pacbot(i)

    def convert_to_render_data(self):
        entity_data = [(*self.map.get_entity(i), e.get_sprite())
                       for i, e in enumerate([*self.pacbots, *self.aliens])]
        return self.map, entity_data
