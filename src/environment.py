from typing import List

import pygame

from src.settings import *


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
    return read_environment_from_file()


def display_row_by_row(grid):
    for row in grid:
        print(row)


def draw_environment(screen, grid):
    dimension_x = len(grid)
    dimension_y = len(grid[0])
    for i, row in enumerate(grid):
        for j, item in enumerate(row):
            if item != 0:
                if grid[(i - 1) % dimension_x][j] == 0:
                    pygame.draw.line(screen, GREEN, [j * BLOCK_SIZE, i * BLOCK_SIZE],
                                     [(j + 1) * BLOCK_SIZE, i * BLOCK_SIZE], 3)
                if grid[(i + 1) % dimension_x][j] == 0:
                    pygame.draw.line(screen, GREEN, [j * BLOCK_SIZE, (i + 1) * BLOCK_SIZE],
                                     [(j + 1) * BLOCK_SIZE, (i + 1) * BLOCK_SIZE],
                                     3)
                if grid[i][(j - 1) % dimension_y] == 0:
                    pygame.draw.line(screen, GREEN, [j * BLOCK_SIZE, i * BLOCK_SIZE],
                                     [j * BLOCK_SIZE, (i + 1) * BLOCK_SIZE], 3)
                if grid[i][(j + 1) % dimension_y] == 0:
                    pygame.draw.line(screen, GREEN, [(j + 1) * BLOCK_SIZE, i * BLOCK_SIZE],
                                     [(j + 1) * BLOCK_SIZE, (i + 1) * BLOCK_SIZE], 3)


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
