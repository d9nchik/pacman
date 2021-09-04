import random


class Entity:
    def __init__(self, grid) -> None:
        super().__init__()
        self.grid = grid

    def get_random_start_position(self):
        dimension_x = len(self.grid)
        dimension_y = len(self.grid[0])
        position = ()
        while len(position) == 0:
            x = random.randint(0, dimension_x - 1)
            y = random.randint(0, dimension_y - 1)
            if self.grid[x][y] != 0:
                position = (y * 32, x * 32)
        return position
