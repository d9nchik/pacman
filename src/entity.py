import random

import pygame

BLACK = (0, 0, 0)


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        # set the background to transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Ellipse(pygame.sprite.Sprite):
    def __init__(self, x, y, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        # set the background to transparent
        self.image = pygame.Surface([width, height])
        self.image.set_colorkey(BLACK)
        self.image.fill(BLACK)
        # draw ellipse
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


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
