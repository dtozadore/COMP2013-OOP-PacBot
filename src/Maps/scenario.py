import os
import pandas as pd
import numpy as np
from src.Map import Map, StaticMapState


class Scenario:
    def __init__(self, name, data_path):
        self.name = name
        self.data_path = data_path
        self.data = None
        self.np_data = None
        self.map = None

    def load_data(self):
        """Load data from a CSV file into a pandas DataFrame."""
        file_path = os.path.join(self.data_path, f"{self.name}.csv")
        self.data = pd.read_csv(file_path, header=None)
        self.data.fillna(0, inplace=True)
        self.np_data = self.data.to_numpy().astype(int)
        print(f"Data loaded for scenario '{self.name}' from {file_path}")

    def get_pos(self, x, y):
        """Return the value at position (x, y)."""
        return self.np_data[x, y]

    def get_dimensions(self):
        """Return the map dimensions as (rows, cols)."""
        return self.np_data.shape

    def create_map(self, pacbot_initials=None, alien_initials=None):
        """Create a Map object from the loaded scenario data."""
        if self.np_data is None:
            raise ValueError("No data loaded. Call load_data() first.")

        pacbot_initials = pacbot_initials or [{'id': 'pacbot', 'pos': (1, 1)}]
        alien_initials = alien_initials or []

        dimensions = self.get_dimensions()
        self.map = Map(dimensions, pacbot_initials, alien_initials)
        self.map.set_map(self.np_data)
        return self.map

    def count_survivors(self):
        """Count total survivors (pellets) in the scenario."""
        return np.count_nonzero(self.np_data == StaticMapState.SURVIVOR.value)

    def find_spawn_points(self):
        """Find all empty spaces suitable for spawning entities."""
        empty_positions = []
        for r in range(self.np_data.shape[0]):
            for c in range(self.np_data.shape[1]):
                if self.np_data[r, c] == StaticMapState.BLANK.value:
                    empty_positions.append((r, c))
        return empty_positions


# Example usage
if __name__ == "__main__":
    scenario = Scenario(name="Scenario", data_path="src\\Maps")
    scenario.load_data()

    # Create a game map from the scenario
    game_map = scenario.create_map(
        pacbot_initials=[{'id': 'player1', 'pos': (1, 1)}],
        alien_initials=[{'id': 'alien1', 'pos': (5, 5)}]
    )

    print(f"Map dimensions: {scenario.get_dimensions()}")
    print(f"Survivors to collect: {scenario.count_survivors()}")
