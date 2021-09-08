import random

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
    grid = [[0 for x in range(DIMENSION_Y)] for x in range(DIMENSION_X)]
    x = random.randint(0, DIMENSION_X - 1)
    y = random.randint(0, DIMENSION_Y - 1)
    grid[x][y] = 1
    direction = random.randint(0, 3)
    for n in range(0, 500):
        if n % 5 == 4:
            direction = random.randint(0, 3)
        x, y = apply_direction_to_grid(grid, x, y, direction)
    return grid


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
