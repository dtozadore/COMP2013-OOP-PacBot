from enum import Enum
import numpy as np
from pathlib import Path

from Map import StaticMapState, Map
from Graphics.sprite import Sprite


def clamp(n, lo, hi):
    return max(lo, min(n, hi))


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Entity:
    def update_view(self):
        pass

    def get_movement(self) -> Direction:
        return Direction.UP


class GameLogic:
    def __init__(self, teleoperation_mode=False):
        self.map: Map
        self.pacbots: list[Entity] = []
        self.aliens: list[Entity] = []

        self.retrieved_survivors = 0
        self.remaining_pacbots = 3

        self.teleoperation_mode = teleoperation_mode
        pass

    def init_game(self):
        self.entities = []
        pass

    def update(self) -> tuple[np.ndarray, list[Sprite]]:
        # Update views of the entities (and allow communication)
        #  Also prevents desync where entites updated later on in the
        #  sequence see the new positions of those updated before them
        for entity in [*self.pacbots, *self.aliens]:
            entity.update_view()

        # Get desired movement for the aliens
        for i, entity in enumerate(self.aliens):
            desired_dir = entity.get_movement()

            # Check desired direction for wall collision
            new_pos = self.__move_coord(
                self.map.get_dynamic(len(self.pacbots) + i), desired_dir)

            check = self.map.get_static(new_pos)
            if check is None or check > 1:
                # Is a wall -> invalid move
                continue

            self.map.set_entity(len(self.pacbots) + i, new_pos)

        # Check for custom collisions
        dead_pacbots = []
        for i, pacbot in enumerate(self.pacbots):
            # Picked up a survivor
            self_pos = self.map.get_dynamic(i)
            if self.map.get_static(self_pos) == StaticMapState.SURVIVOR:
                pacbot.pickup()
                self.map.set(self_pos, StaticMapState.SURVIVOR)

            for i in range(len(self.aliens)):
                # Overlap with an alien
                if self_pos == self.map.get_dynamic(len(self.pacbots) + i):
                    # Remove the pacbot
                    dead_pacbots.append(i)
                    self.remaining_pacbots -= 1

                    # Replace the survivor on the map

        # Iterate backward to prevent indexing error
        for i in dead_pacbots[::-1]:
            self.pacbots[i] = []
            self.map.remove(i)

        # Render update

        # Game end logic
        if self.remaining_pacbots <= 0:
            pass
        if self.retrieved_survivors >= 7:
            pass

        return self.convert_to_render_data()

    def convert_to_render_data(self):
        if not hasattr(self, "last_entity_data"):
            self.last_entity_data = None

        entity_data = [(*self.map.get_dynamic(i), e.get_sprite())
                       for i, e in enumerate([*self.pacbots, *self.aliens])]

        if self.last_entity_data is not None:
            sprites = [
                Sprite("", e[0], e[1], self.__check_direction(e[0:2], last_e[0:2]), False, 0, 0, [e[2]])
                for e, last_e in zip(entity_data, self.last_entity_data)]
        else:
            sprites = [
                Sprite("", e[0], e[1], Direction.DOWN, False, 0, 0, [e[2]])
                for e in entity_data]
        self.last_entity_data = entity_data.copy()

        return self.map.static_map, sprites

    def __check_direction(self, current, last) -> Direction:
        dx = current[0] - last[0]
        dy = current[1] - last[1]

        if dx < 0:
            return Direction.LEFT
        elif dx > 0:
            return Direction.RIGHT
        elif dy < 0:
            return Direction.UP
        elif dy > 0:
            return Direction.DOWN
        else:
            return Direction.DOWN

    def replace_survivor(self, initial_attempt):
        if self.map.get_static(initial_attempt) == 0:
            self.map.set(initial_attempt, 1)
            return

        checked_list = [initial_attempt]
        check_queue = []
        for new_pos in self.__generate_adjacent(initial_attempt):
            if new_pos not in checked_list:
                check_queue.append(new_pos)

        while len(check_queue) != 0:
            check_pos = check_queue[0]
            check_queue[0] = []
            checked_list.append(check_pos)

            if self.map.get(check_pos) == 0:
                self.map.set(initial_attempt, 1)
                return

            for new_pos in self.__generate_adjacent(check_pos):
                if new_pos not in checked_list:
                    check_queue.append(new_pos)

    def __move_coord(self, coord, direction: Direction):
        new_coord = coord.copy()
        if direction == Direction.UP:
            new_coord[1] -= 1
        elif direction == Direction.RIGHT:
            new_coord[0] += 1
        elif direction == Direction.DOWN:
            new_coord[1] += 1
        elif direction == Direction.LEFT:
            new_coord[0] -= 1

        new_coord[0] = clamp(new_coord[0], 0, self.map.rows)
        new_coord[1] = clamp(new_coord[0], 0, self.map.cols)

        return new_coord

    def __generate_adjacent(self, coord):
        return [self.__move_coord(coord, Direction.UP),
                self.__move_coord(coord, Direction.DOWN),
                self.__move_coord(coord, Direction.LEFT),
                self.__move_coord(coord, Direction.RIGHT)]
