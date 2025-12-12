from abc import ABC, abstractmethod
import numpy as np
from collections import deque
from src.Map import Direction, StaticMapState

# =========================
# Constants
# =========================
PACBOT = 13
ALIEN = 14
SURVIVOR = 15
UNEXPLORED = -1
WALL = 0
EMPTY = 1


# =========================
# BFS Utility
# =========================
def bfs_next_step(grid, start, is_target, passable):
    rows, cols = grid.shape
    visited = list()
    queue = deque()

    queue.append((start[0], start[1], None))
    visited.append(start)

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        x, y, first_step = queue.popleft()

        if is_target(grid[x, y]) and (x, y) != start:
            return first_step

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < rows and
                0 <= ny < cols and
                (nx, ny) not in visited and
                passable(grid[nx, ny])
            ):
                visited.append((nx, ny))
                queue.append((nx, ny, first_step or (nx, ny)))

    return None


# =========================
# Entity Base Class
# =========================
class Entity(ABC):
    def __init__(self, speed, id, icon, name, team=None, pos=None):
        self.alive = True
        self.speed = speed
        self.id = id
        self.icon = icon
        self.name = name
        self.team = team
        self.pos = pos

    @abstractmethod
    def move(self) -> Direction:
        raise NotImplementedError()

    def give_ui(self):
        return [self.id, self.icon, self.name]

    def assign_id(self, new_id):
        self.id = new_id

    def update_view(self, kernel, pos):
        assert self.team is not None
        self.team.update(kernel, pos)
        
    def get_sprite(self) -> str:
        return self.icon


# =========================
# Pacbot
# =========================
class Pacbot(Entity):
    def __init__(self, speed, id, name, icon = "", team=None, pos=None):
        super().__init__(speed, id, "resources/art/pacbot/pacbot_down.png", name, team, pos)
        self.carry_survivor = False

    def pickup(self):
        self.carry_survivor = True

    def dropoff(self):
        self.carry_survivor = False

    def has_survivor(self):
        return self.carry_survivor

    def move(self) -> Direction:
        return Direction.DOWN


# =========================
# Alien
# =========================
class Alien(Entity):
    def __init__(self, speed, id, name, team=None, pos=None):
        super().__init__(speed, id, "resources/art/pacbot/pacbot_down.png", name, team, pos)

    def move(self, pos=None) -> Direction:
        # Use stored position if not provided
        if pos is None:
            pos = self.pos

        if pos is None:
            print("Warning: Alien has no position to move from")
            return Direction.DOWN

        assert self.team is not None
        grid = self.team.map

        # 1. Hunt Pacbots
        step = bfs_next_step(
            grid,
            pos,
            is_target=lambda v: v == PACBOT,
            passable=lambda v: v != WALL
        )
        if step:
            self.pos = step
            return step

        # 2. Hunt Survivors
        step = bfs_next_step(
            grid,
            pos,
            is_target=lambda v: v == SURVIVOR,
            passable=lambda v: v != WALL
        )
        if step:
            self.pos = step
            return step

        # 3. Explore unexplored
        step = bfs_next_step(
            grid,
            pos,
            is_target=lambda v: v == UNEXPLORED,
            passable=lambda v: v != WALL
        )
        if step:
            self.pos = step
            return step

        return Direction.DOWN


# =========================
# Team
# =========================
class Team(ABC):
    def __init__(self, map_dims : tuple[int, int]):
        self._map = np.ones(map_dims, dtype=StaticMapState) * UNEXPLORED
        self.entities = []

    @property
    def map(self):
        return self._map

    def update(self, kernel, pos):
        k = kernel.shape[0] // 2
        x0 = max(0, pos[0] - k)
        x1 = min(self._map.shape[0], pos[0] + k + 1)
        y0 = max(0, pos[1] - k)
        y1 = min(self._map.shape[1], pos[1] + k + 1)

        self._map[x0:x1, y0:y1] = kernel[
            (x0 - (pos[0] - k)):(x1 - (pos[0] - k)),
            (y0 - (pos[1] - k)):(y1 - (pos[1] - k))
        ]

    def add_entity(self, entity):
        self.entities.append(entity)
        entity.team = self
        if entity.pos:
            self._map[entity.pos] = entity.icon

    def remove_entity(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)
            if entity.pos:
                self._map[entity.pos] = UNEXPLORED