import random


class Entity:
    def __init__(self, grid) -> None:
        super().__init__()
        self.grid = grid
        self.current_x = 0
        self.current_y = 0
        self.get_random_start_position()

    def get_random_start_position(self):
        dimension_x = len(self.grid)
        dimension_y = len(self.grid[0])
        position = ()
        while len(position) == 0:
            x = random.randint(0, dimension_x - 1)
            y = random.randint(0, dimension_y - 1)
            if self.grid[x][y] != 0:
                position = x, y
        self.current_x, self.current_y = position
