import random
from typing import List

from consoleGame.settings import *


def apply_direction_to_grid(grid, x, y, direction):
    dimension_x = len(grid)
    dimension_y = len(grid[0])
    if direction == 0:
        grid[(x - 1) % dimension_x][y] = 1
        return (x - 1) % dimension_x, y
    elif direction == 1:
        grid[x][(y + 1) % dimension_y] = 1
        return x, (y + 1) % dimension_y
    elif direction == 2:
        grid[(x + 1) % dimension_x][y] = 1
        return (x + 1) % dimension_x, y

    grid[x][(y - 1) % dimension_y] = 1
    return x, (y - 1) % dimension_y


def generate_environment():
    grid = [[0 for x in range(DIMENSION_Y)] for x in range(DIMENSION_X)]
    x = random.randint(0, DIMENSION_X - 1)
    y = random.randint(0, DIMENSION_Y - 1)
    grid[x][y] = 1
    direction = random.randint(0, 3)
    for n in range(0, 500):
        if n % 5 == 4:
            direction = random.randint(0, 3)
        x, y = apply_direction_to_grid(grid, x, y, direction)
    print_to_file(grid)
    return grid


def print_to_file(grid: List[List[int]]):
    with open(GRID_FILE, 'w') as f:
        for row in grid:
            print(' '.join(map(lambda x: str(x), row)), file=f)


def read_environment_from_file() -> List[List[int]]:
    with open(GRID_FILE) as f:
        grid = []
        for row in f:
            grid.append(list(map(lambda x: int(x), row.split())))
        return grid


def display_row_by_row(grid):
    for row in grid:
        print(row)
