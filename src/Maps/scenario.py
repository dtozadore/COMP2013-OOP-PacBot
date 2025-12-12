import os
import pandas as pd
import numpy as np

class Scenario:
    def __init__(self, name, data_path):
        self.name = name
        self.data_path = data_path
        self.data = None

    def load_data(self):
        """Load data from a CSV file into a pandas DataFrame."""
        file_path = os.path.join(self.data_path, f"{self.name}.csv")
        self.data = pd.read_csv(file_path, header=None)

        self.data.fillna(0, inplace=True)
        self.np_data = self.data.to_numpy()
        # self.data = np.array(self.data)
        print(f"Data loaded for scenario '{self.name}' from {file_path}")

   
    def get_pos(self, x, y):
        """Return the position of the scenario."""
        return self.np_data[x, y]


# Example usage:if __name__ == "__main__":
scenario = Scenario(name="Scenario", data_path=".\Week 10")

scenario.load_data()
# scenario.preprocess_data()

# print(scenario.get_summary())
# print(scenario.data)

sentence = '| '
for i in range(scenario.np_data.shape[0]):
   sentence += str(scenario.get_pos(0, i)) + ' | '

# sentence += ' |'


   
print(sentence)

