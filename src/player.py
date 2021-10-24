from copy import copy

import pygame
from pygame.sprite import Group

from src.enemies import Pinky
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

        self.dots_group = dots_group
        self.enemies = enemies
        self.min_algorithm = self.min_turn

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
        j = self.rect.topleft[0] // BLOCK_SIZE
        i = self.rect.topleft[1] // BLOCK_SIZE
        if 0 > i or i >= DIMENSION_X or 0 > j or j >= DIMENSION_Y:
            return

        direction = self.alfa_betta_pruning()
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

    def alfa_betta_pruning(self):
        j = self.rect.topleft[0] // BLOCK_SIZE
        i = self.rect.topleft[1] // BLOCK_SIZE
        all_coins = self.all_coins_indexes()
        recursion_index = MAX_ALFA_BETTA_RECURSION
        betta = float('inf')
        v = float('-inf')
        best_direction = ''

        grid = self.grid
        all_directions = get_available_directions_coordinates(grid, i, j)

        for direction_i, direction_j, direction in all_directions:
            new_enemies = list(map(lambda enemy: copy(enemy), self.enemies.sprites()))
            count = 0
            available_coins = list(all_coins)
            if len(available_coins) == 0:
                return float('+inf')
            if (direction_i, direction_j) in available_coins:
                available_coins.remove((direction_i, direction_j))
                count += 10
            count += 1
            result = self.min_algorithm(direction_i, direction_j, count, all_coins, v, betta, recursion_index - 1,
                                        (i, j),
                                        new_enemies)
            if result >= v:
                v = result
                best_direction = direction
        return best_direction

    def all_coins_indexes(self):
        return tuple(map(lambda topleft: ((topleft[1] - 12) // BLOCK_SIZE, (topleft[0] - 12) // BLOCK_SIZE),
                         map(lambda coin: coin.rect.topleft, self.dots_group.sprites())))


    def max_turn(self, i, j, score, dots, alfa, betta, recursion_index, previous, enemies) -> float:
        if recursion_index == 0:
            return score

        v = float('-inf')

        all_directions = get_available_directions_coordinates(self.grid, i, j)
        for direction_i, direction_j, direction in all_directions:
            if (direction_i, direction_j) == previous and len(all_directions) != 1:
                continue

            available_coins = list(dots)
            new_score = score
            if (direction_i, direction_j) in available_coins:
                available_coins.remove((direction_i, direction_j))
                new_score += 1
            result = self.min_algorithm(direction_i, direction_j, new_score, available_coins, max(alfa, v), betta,
                                        recursion_index - 1, (i, j), enemies)
            if result > v:
                v = result
                if v > betta:
                    return v
        if v > 0:
            return v

        for direction_i, direction_j, direction in all_directions:
            if (direction_i, direction_j) != previous or len(all_directions) == 1:
                continue

            available_coins = list(dots)
            new_score = score
            if (direction_i, direction_j) in available_coins:
                available_coins.remove((direction_i, direction_j))
                new_score += 10
            result = self.min_algorithm(direction_i, direction_j, new_score, available_coins, max(alfa, v), betta,
                                        recursion_index - 1, (i, j), enemies)
            if result > v:
                v = result
                if v > betta:
                    return v
        return v

    def min_turn(self, i, j, score, dots, alfa, betta, recursion_index, previous, enemies) -> float:
        new_enemies = list(map(lambda enemy: copy(enemy), enemies))

        x_dimension = len(self.grid)
        y_dimension = len(self.grid[0])

        for enemy in new_enemies:
            enemy.rect = enemy.rect.copy()
            enemy.update(i, j)
            enemy_i, enemy_j = enemy.get_coordinates()
            if pacman_distance(i, enemy_i, x_dimension) + pacman_distance(j, enemy_j, y_dimension) < 3:
                return float('-inf')

        return self.max_turn(i, j, score, dots, alfa, betta, recursion_index, previous, new_enemies)

    def expect_turn(self, i, j, score, dots, alfa, betta, recursion_index, previous, enemies) -> float:
        new_enemies = list(map(lambda enemy: copy(enemy), enemies))

        x_dimension = len(self.grid)
        y_dimension = len(self.grid[0])

        for enemy in new_enemies:
            enemy.rect = enemy.rect.copy()
            enemy.update(i, j)
            enemy_i, enemy_j = enemy.get_coordinates()
            if pacman_distance(i, enemy_i, x_dimension) + pacman_distance(j, enemy_j, y_dimension) < 3 \
                    and not isinstance(enemy, Pinky):
                return float('-inf')

        for enemy in new_enemies:
            enemy_i, enemy_j = enemy.get_coordinates()
            if pacman_distance(i, enemy_i, x_dimension) + pacman_distance(j, enemy_j, y_dimension) < 3:
                return 1 / 3 * self.max_turn(i, j, score, dots, alfa, betta, recursion_index, previous, new_enemies)

        return self.max_turn(i, j, score, dots, alfa, betta, recursion_index, previous, new_enemies)


def pacman_distance(x1, x2, dimension):
    if x1 > x2:
        x1, x2 = x2, x1
    return min(x2 - x1, x1 + dimension - x2)


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


class ExpectPacman(Player):
    def __init__(self, grid, dots_group: Group, enemies: Group):
        super().__init__(grid, dots_group, enemies)
        self.min_algorithm = self.expect_turn
