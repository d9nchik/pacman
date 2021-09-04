import random

import pygame

from src.entity import Entity

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Ellipse(pygame.sprite.Sprite):
    def __init__(self, x, y, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        # Draw the ellipse
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Slime(pygame.sprite.Sprite, Entity):
    def __init__(self, image_path, grid):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        Entity.__init__(self, grid)
        # Set the direction of the slime
        self.change_x = 0
        self.change_y = 0
        # Load image
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = self.get_random_start_position()
        self.change_direction()
        # compute intersection position
        self.intersection_position = self.get_intersection_position()

    def update(self):
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
        elif self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = SCREEN_HEIGHT
        elif self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0

        if self.rect.topleft in self.intersection_position:
            self.change_direction()

    def change_direction(self):

        direction = random.choice(self.get_available_directions())
        if direction == "left":
            self.change_x = -2
            self.change_y = 0
        elif direction == "right":
            self.change_x = 2
            self.change_y = 0
        elif direction == "up":
            self.change_x = 0
            self.change_y = -2
        elif direction == "down":
            self.change_x = 0
            self.change_y = 2

    def get_available_directions(self):
        dimension_x = len(self.grid)
        dimension_y = len(self.grid[0])
        j = self.rect.topleft[0] // 32
        i = self.rect.topleft[1] // 32
        directions = []
        if self.grid[(i + 1) % dimension_x][j] != 0:
            directions.append('down')
        if self.grid[(i - 1) % dimension_x][j] != 0:
            directions.append('up')
        if self.grid[i][(j + 1) % dimension_y] != 0:
            directions.append('right')
        if self.grid[i][(j - 1) % dimension_y] != 0:
            directions.append('left')
        return directions

    def get_intersection_position(self):
        items = set()
        for i, row in enumerate(self.grid):
            for j, item in enumerate(row):
                if item != 0 and len(list(filter(lambda x: x != 0, get_cell_neighbours(self.grid, i, j)))) != 2:
                    items.add((j * 32, i * 32))

        return items


def get_cell_neighbours(grid, x, y):
    dimension_x = len(grid)
    dimension_y = len(grid[0])
    neighbours = [grid[(x + 1) % dimension_x][y], grid[(x - 1) % dimension_x][y], grid[x][(y + 1) % dimension_y],
                  grid[x][(y - 1) % dimension_y]]
    return neighbours


class Blinky(Slime):

    def __init__(self, grid):
        super().__init__('./src/sprites/blinky.png', grid)


class Clyde(Slime):

    def __init__(self, grid):
        super().__init__('./src/sprites/clyde.png', grid)


class Inky(Slime):

    def __init__(self, grid):
        super().__init__('./src/sprites/inky.png', grid)


class Pinky(Slime):

    def __init__(self, grid):
        super().__init__('./src/sprites/pinky.png', grid)
