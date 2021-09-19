from random import choice

import pygame
from pygame.sprite import Group, Sprite

from src.entity import Entity
from src.settings import *


class Player(pygame.sprite.Sprite, Entity):
    change_x = 0
    change_y = 0
    explosion = False
    game_over = False

    def __init__(self, grid, dots_group: Group, enemies: Group):
        pygame.sprite.Sprite.__init__(self)

        Entity.__init__(self, grid)
        self.image = pygame.image.load("./src/sprites/player.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.get_random_start_position()

        img = pygame.image.load("./src/sprites/walk.png").convert()

        self.move_right_animation = Animation(img, BLOCK_SIZE, BLOCK_SIZE)
        self.move_left_animation = Animation(pygame.transform.flip(img, True, False), BLOCK_SIZE, BLOCK_SIZE)
        self.move_up_animation = Animation(pygame.transform.rotate(img, 90), BLOCK_SIZE, BLOCK_SIZE)
        self.move_down_animation = Animation(pygame.transform.rotate(img, 270), BLOCK_SIZE, BLOCK_SIZE)

        img = pygame.image.load("./src/sprites/explosion.png").convert()
        self.explosion_animation = Animation(img, 30, 30)

        self.want_coin = Sprite()
        self.dots_group = dots_group
        self.enemies = enemies
        self.change_want_coin()

    def update(self, empty_blocks):
        if not self.explosion:
            if self.rect.topleft[0] % BLOCK_SIZE == 0 and self.rect.topleft[1] % BLOCK_SIZE == 0:
                self.change_direction()

            if self.rect.right < 0:
                self.rect.left = SCREEN_WIDTH
            elif self.rect.left > SCREEN_WIDTH:
                self.rect.right = 0
            if self.rect.bottom < 0:
                self.rect.top = SCREEN_HEIGHT
            elif self.rect.top > SCREEN_HEIGHT:
                self.rect.bottom = 0
            self.rect.x += self.change_x
            self.rect.y += self.change_y

            # This will cause the animation to start

            if self.change_x > 0:
                self.move_right_animation.update(10)
                self.image = self.move_right_animation.get_current_image()
            elif self.change_x < 0:
                self.move_left_animation.update(10)
                self.image = self.move_left_animation.get_current_image()

            if self.change_y > 0:
                self.move_down_animation.update(10)
                self.image = self.move_down_animation.get_current_image()
            elif self.change_y < 0:
                self.move_up_animation.update(10)
                self.image = self.move_up_animation.get_current_image()
        else:
            if self.explosion_animation.index == self.explosion_animation.get_length() - 1:
                pygame.time.wait(500)
                self.game_over = True
            self.explosion_animation.update(12)
            self.image = self.explosion_animation.get_current_image()

    def change_direction(self):
        if self.want_coin not in self.dots_group:
            self.change_want_coin()
        j = self.rect.topleft[0] // BLOCK_SIZE
        i = self.rect.topleft[1] // BLOCK_SIZE
        if 0 > i or i >= DIMENSION_X or 0 > j or j >= DIMENSION_Y:
            return
        want_i, want_j = self.sprite_to_coordinates()
        direction = self.a_star(want_i, want_j)
        if direction == "left":
            self.change_x = -4
            self.change_y = 0
        elif direction == "right":
            self.change_x = 4
            self.change_y = 0
        elif direction == "up":
            self.change_x = 0
            self.change_y = -4
        elif direction == "down":
            self.change_x = 0
            self.change_y = 4

    def change_want_coin(self):
        self.want_coin = choice(self.dots_group.sprites())

    def sprite_to_coordinates(self):
        return (self.want_coin.rect.topleft[1] - 12) // BLOCK_SIZE, (self.want_coin.rect.topleft[0] - 12) // BLOCK_SIZE

    def a_star(self, want_i, want_j):
        j = self.rect.topleft[0] // BLOCK_SIZE
        i = self.rect.topleft[1] // BLOCK_SIZE
        visited = {(i, j)}
        prices = dict()

        for node_to_visit_i, node_to_visit_j, direction in get_available_directions_coordinates(self.grid, i, j):
            prices[(node_to_visit_i, node_to_visit_j)] = [
                1 + heuristic(node_to_visit_i, node_to_visit_j, want_i, want_j) + self.enemies_heuristic(
                    node_to_visit_i, node_to_visit_j),
                direction]

        while len(prices) != 0:
            cheapest_node = list(prices.keys())[0]
            cheapest_price = prices[cheapest_node][0]

            for key, value in prices.items():
                if value[0] < cheapest_price:
                    cheapest_price = value[0]
                    cheapest_node = key

            visit_i, visit_j = cheapest_node
            direction = prices[cheapest_node][1]
            del prices[cheapest_node]
            cheapest_price -= heuristic(visit_i, visit_j, want_i, want_j)

            if not (visit_i, visit_j) in visited:
                visited.add((visit_i, visit_j))
                if visit_i == want_i and visit_j == want_j:
                    return direction
                for node_to_visit_i, node_to_visit_j, _ in get_available_directions_coordinates(self.grid, visit_i,
                                                                                                visit_j):
                    h = heuristic(node_to_visit_i, node_to_visit_j, want_i, want_j)
                    if (node_to_visit_i, node_to_visit_j) not in visited and (
                            (node_to_visit_i, node_to_visit_j) not in prices or
                            prices[(node_to_visit_i, node_to_visit_j)][0] > cheapest_price + 1 + h):
                        prices[(node_to_visit_i, node_to_visit_j)] = [
                            cheapest_price + 1 + h, direction]

    def enemies_heuristic(self, x, y):
        h = 0
        for sprite in self.enemies.sprites():
            h += 118 / (1 + pacman_distance(sprite.rect.topleft[1] // BLOCK_SIZE, x, DIMENSION_X) + pacman_distance(
                sprite.rect.topleft[0] // BLOCK_SIZE, y, DIMENSION_Y))
        return h


def pacman_distance(x1, x2, dimension):
    if x1 > x2:
        x1, x2 = x2, x1
    return min(x2 - x1, x1 + dimension - x2)


def heuristic(x, y, aim_x, aim_y):
    return 1 * (pacman_distance(x, aim_x, DIMENSION_X) + pacman_distance(y, aim_y, DIMENSION_Y))


def get_available_directions_coordinates(grid, i, j):
    dimension_x = len(grid)
    dimension_y = len(grid[0])
    coordinates_list = [[(i + 1) % dimension_x, j, 'down'], [(i - 1) % dimension_x, j, 'up'],
                        [i, (j + 1) % dimension_y, 'right'],
                        [i, (j - 1) % dimension_y, 'left']]
    result = []
    for coordinates in coordinates_list:
        if grid[coordinates[0]][coordinates[1]] != 0:
            result.append(coordinates)

    return result


class Animation(object):
    def __init__(self, img, width, height):
        # load sprite
        self.sprite_sheet = img
        self.image_list = []
        self.load_images(width, height)
        # current image in list
        self.index = 0
        # time variable
        self.clock = 1

    def load_images(self, width, height):
        # iterate over image in the sprite sheet
        for y in range(0, self.sprite_sheet.get_height(), height):
            for x in range(0, self.sprite_sheet.get_width(), width):
                # load images into a list
                img = self.get_image(x, y, width, height)
                self.image_list.append(img)

    def get_image(self, x, y, width, height):
        # create a new blank image
        image = pygame.Surface([width, height]).convert()
        # scale sprite
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        # let black is transparent color
        image.set_colorkey(BLACK)
        return image

    def get_current_image(self):
        return self.image_list[self.index]

    def get_length(self):
        return len(self.image_list)

    def update(self, fps=30):
        self.clock += 1
        self.clock %= fps + 1

        if self.clock in range(1, fps, 8):
            self.index += 1
            self.index %= self.get_length()
