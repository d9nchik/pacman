from copy import copy
from typing import List, Tuple, Union

from consoleGame.enemies import Pinky, Spirit
from consoleGame.entity import Entity
from consoleGame.settings import *


class Player(Entity):
    change_x = 0
    change_y = 0
    explosion = False
    game_over = False

    def __init__(self, grid, dots_group: List[Tuple[int, int]], enemies: List[Spirit]):
        Entity.__init__(self, grid)

        self.dots_group = dots_group
        self.enemies = enemies
        self.min_algorithm = self.min_turn

    def update(self):
        if not self.explosion:
            self.change_direction()

            if self.current_x < 0:
                self.current_x += DIMENSION_X
            elif self.current_x >= DIMENSION_X:
                self.current_x -= DIMENSION_X
            if self.current_y < 0:
                self.current_y += DIMENSION_Y
            elif self.current_y >= DIMENSION_Y:
                self.current_y -= DIMENSION_Y
            self.current_x += self.change_x
            self.current_y += self.change_y
        else:
            self.game_over = True
            # This will cause the animation to start

    def change_direction(self):
        j = self.current_y
        i = self.current_x
        if 0 > i or i >= DIMENSION_X or 0 > j or j >= DIMENSION_Y:
            return

        direction = self.alfa_betta_pruning()
        if direction == "left":
            self.change_x = 0
            self.change_y = -1
        elif direction == "right":
            self.change_x = 0
            self.change_y = 1
        elif direction == "up":
            self.change_x = -1
            self.change_y = 0
        elif direction == "down":
            self.change_x = 1
            self.change_y = 0

    def alfa_betta_pruning(self):
        j = self.current_y
        i = self.current_x
        all_coins = copy(self.dots_group)
        recursion_index = MAX_ALFA_BETTA_RECURSION
        betta = float('inf')
        v = float('-inf')

        grid = self.grid
        all_directions = get_available_directions_coordinates(grid, i, j)
        best_direction = all_directions[0][2]

        for direction_i, direction_j, direction in all_directions:
            new_enemies = list(map(lambda enemy: copy(enemy), self.enemies))
            count = 0
            available_coins = list(all_coins)
            if (direction_i, direction_j) in available_coins:
                available_coins.remove(tuple((direction_i, direction_j)))
                count += 10
            count += 1
            result = self.min_algorithm(direction_i, direction_j, count, all_coins, v, betta, recursion_index - 1,
                                        (i, j),
                                        new_enemies)
            if result > v:
                v = result
                best_direction = direction
        return best_direction

    def max_turn(self, i: int, j: int, score: int, dots: List[Tuple[int, int]], alfa: float, betta: float,
                 recursion_index: int, previous: Tuple[int, int], enemies: List[Spirit]) -> float:
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
            if len(available_coins) == 0:
                return float('+inf')
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

    def min_turn(self, i: int, j: int, score: int, dots: List[Tuple[int, int]], alfa: float, betta: float,
                 recursion_index: int, previous: Tuple[int, int], enemies: List[Spirit]) -> float:
        new_enemies = list(map(lambda enemy: copy(enemy), enemies))

        x_dimension = len(self.grid)
        y_dimension = len(self.grid[0])

        for enemy in new_enemies:
            enemy.update(i, j)
            enemy_i, enemy_j = enemy.current_x, enemy.current_y
            if pacman_distance(i, enemy_i, x_dimension) + pacman_distance(j, enemy_j, y_dimension) < 3:
                return float('-inf')

        return self.max_turn(i, j, score, dots, alfa, betta, recursion_index, previous, new_enemies)

    def expect_turn(self, i, j, score, dots, alfa, betta, recursion_index, previous, enemies) -> float:
        new_enemies = list(map(lambda enemy: copy(enemy), enemies))

        x_dimension = len(self.grid)
        y_dimension = len(self.grid[0])

        for enemy in new_enemies:
            enemy.update(i, j)
            enemy_i, enemy_j = enemy.current_x, enemy.current_y
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


def get_available_directions_coordinates(grid, i, j) -> List[List[Union[int, str]]]:
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


class ExpectPacman(Player):
    def __init__(self, grid, dots_group: List[Tuple[int, int]], enemies: List[Spirit]):
        super().__init__(grid, dots_group, enemies)
        self.min_algorithm = self.expect_turn
