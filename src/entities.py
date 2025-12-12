from abc import ABC, abstractmethod
import numpy as np
from collections import deque

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
    visited = set()
    queue = deque()

    queue.append((start[0], start[1], None))
    visited.add(start)

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
                visited.add((nx, ny))
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
    def move(self):
        pass

    def give_ui(self):
        return [self.id, self.icon, self.name]

    def assign_id(self, new_id):
        self.id = new_id

    def update_view(self, kernel, pos):
        self.team.update(kernel, pos)


# =========================
# Pacbot
# =========================
class Pacbot(Entity):
    def __init__(self, speed, id, name, team=None, pos=None):
        super().__init__(speed, id, PACBOT, name, team, pos)
        self.carry_survivor = False

    def pickup(self):
        self.carry_survivor = True

    def dropoff(self):
        self.carry_survivor = False

    def check_occupied(self):
        return self.carry_survivor

    def move(self):
        pass  # To be implemented later


# =========================
# Survivor
# =========================
class Survivor(Entity):
    def __init__(self, id, team=None, pos=None):
        super().__init__(0, id, SURVIVOR, "Survivor", team, pos)

    def move(self):
        pass  # Survivors are static


# =========================
# Alien
# =========================
class Alien(Entity):
    def __init__(self, speed, id, name, team=None, pos=None):
        super().__init__(speed, id, ALIEN, name, team, pos)

    def move(self, pos=None):
        # Use stored position if not provided
        if pos is None:
            pos = self.pos
        
        if pos is None:
            print("Warning: Alien has no position to move from")
            return None
            
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

        return None


# =========================
# Team
# =========================
class Team(ABC):
    def __init__(self, map_dims):
        self._map = np.ones(map_dims, dtype=int) * UNEXPLORED
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


# =========================
# Example Usage
# =========================
if __name__ == "__main__":
    team = Team((10, 10))

    # Create alien at position (5, 5)
    alien = Alien(speed=1, id=1, name="Helitha", team=team, pos=(5, 5))
    team.add_entity(alien)

    # Create pacbot at position (3, 4) - within alien's view
    pacbot = Pacbot(speed=1, id=2, name="Pac", team=team, pos=(3, 4))
    team.add_entity(pacbot)

    print("=== Initial Setup ===")
    print("Alien at:", alien.pos)
    print("Pacbot at:", pacbot.pos)
    print("\nInitial team map:")
    print(team.map)
    
    # Simulate alien receiving a view of its surroundings
    # The alien is at (5,5) and sees a 5x5 area around itself
    # This kernel represents what the alien sees from its sensor
    kernel = np.array([
        [EMPTY,  EMPTY,  EMPTY,  EMPTY,  EMPTY],
        [EMPTY,  EMPTY,  PACBOT, EMPTY,  EMPTY],   # Pacbot at relative position (1, 2)
        [EMPTY,  EMPTY,  ALIEN,  EMPTY,  EMPTY],   # Alien itself at center (2, 2)
        [EMPTY,  EMPTY,  EMPTY,  EMPTY,  EMPTY],
        [EMPTY,  EMPTY,  EMPTY,  EMPTY,  EMPTY]
    ])
    
    print("\n=== Alien Updates View ===")
    print("Kernel (what alien sees):")
    print(kernel)
    
    # Alien updates its team's map with what it sees
    alien.update_view(kernel, alien.pos)
    
    print("\nTeam map after alien updates view:")
    print(team.map)
    
    # Now alien moves toward the pacbot
    print("\n=== Alien Moves ===")
    old_pos = alien.pos
    new_pos = alien.move()
    
    print(f"Alien moved from {old_pos} to {new_pos}")
    print(f"Pacbot is at {pacbot.pos}")
    print(f"Distance reduced: {np.linalg.norm(np.array(old_pos) - np.array(pacbot.pos)):.2f} -> {np.linalg.norm(np.array(new_pos) - np.array(pacbot.pos)):.2f}")
    
    # Simulate multiple moves
    print("\n=== Multiple Moves ===")
    for i in range(5):
        old_pos = alien.pos
        new_pos = alien.move()
        if new_pos is None:
            print(f"Move {i+1}: Alien can't move further")
            break
        distance = np.linalg.norm(np.array(new_pos) - np.array(pacbot.pos))
        print(f"Move {i+1}: Alien at {new_pos}, distance to Pacbot: {distance:.2f}")
        
        if new_pos == pacbot.pos:
            print("Alien caught the Pacbot!")
            break
