import random

import pygame

from src.entity import Entity
from src.settings import *


class Spirit(pygame.sprite.Sprite, Entity):
    def __init__(self, image_path, grid, player_i, player_j):
        pygame.sprite.Sprite.__init__(self)
        Entity.__init__(self, grid)

        self.change_x = 0
        self.change_y = 0
        # load image
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = self.get_random_start_position()
        self.search = self.uniform_cost_search
        self.change_direction(player_i, player_j)

        self.intersection_position = self.get_intersection_position()

    def update(self, player_i, player_j):
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
            self.change_direction(player_i, player_j)

    def change_direction(self, player_i, player_j):

        # direction = random.choice(self.get_available_directions())
        direction = self.search(player_i, player_j)
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

    def get_intersection_position(self):
        items = set()
        for i, row in enumerate(self.grid):
            for j, item in enumerate(row):
                if item != 0 and not is_tube(get_cell_neighbours(self.grid, i, j)):
                    items.add((j * BLOCK_SIZE, i * BLOCK_SIZE))

        return items

    def breadth_first_search(self, want_i, want_j):
        i, j = self.get_coordinates()
        visited = {(i, j)}
        next_nodes_to_visit = get_available_directions_coordinates(self.grid, i, j)
        while len(next_nodes_to_visit) != 0:
            nodes_to_visit = next_nodes_to_visit
            next_nodes_to_visit = []
            for node_to_visit_i, node_to_visit_j, direction in nodes_to_visit:
                if not (node_to_visit_i, node_to_visit_j) in visited:
                    visited.add((node_to_visit_i, node_to_visit_j))
                    if node_to_visit_i == want_i and node_to_visit_j == want_j:
                        return direction
                    next_nodes_to_visit += list(
                        map(lambda available_directions_coordinate: [available_directions_coordinate[0],
                                                                     available_directions_coordinate[1],
                                                                     direction],
                            get_available_directions_coordinates(self.grid, node_to_visit_i,
                                                                 node_to_visit_j)))

    def deep_first_search(self, want_i, want_j):
        i, j = self.get_coordinates()
        visited = {(i, j)}
        next_nodes_to_visit = get_available_directions_coordinates(self.grid, i, j)
        while len(next_nodes_to_visit) != 0:
            node_to_visit_i, node_to_visit_j, direction = next_nodes_to_visit[-1]
            if not (node_to_visit_i, node_to_visit_j) in visited:
                visited.add((node_to_visit_i, node_to_visit_j))
                if node_to_visit_i == want_i and node_to_visit_j == want_j:
                    return direction
                next_nodes_to_visit += list(
                    map(lambda available_directions_coordinate: [available_directions_coordinate[0],
                                                                 available_directions_coordinate[1],
                                                                 direction],
                        get_available_directions_coordinates(self.grid, node_to_visit_i,
                                                             node_to_visit_j)))
            else:
                next_nodes_to_visit = next_nodes_to_visit[:-1]

    def uniform_cost_search(self, want_i, want_j):
        i, j = self.get_coordinates()
        visited = {(i, j)}
        prices = dict()

        for node_to_visit_i, node_to_visit_j, direction in get_available_directions_coordinates(self.grid, i, j):
            prices[(node_to_visit_i, node_to_visit_j)] = [1, direction]

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
            if not (visit_i, visit_j) in visited:
                visited.add((visit_i, visit_j))
                if visit_i == want_i and visit_j == want_j:
                    return direction
                for node_to_visit_i, node_to_visit_j, _ in get_available_directions_coordinates(self.grid, visit_i,
                                                                                                visit_j):
                    if (node_to_visit_i, node_to_visit_j) not in visited and (
                            (node_to_visit_i, node_to_visit_j) not in prices or
                            prices[(node_to_visit_i, node_to_visit_j)][0] > cheapest_price + 1):
                        prices[(node_to_visit_i, node_to_visit_j)] = [cheapest_price + 1, direction]

    def random_search(self, want_i, want_j):
        i, j = self.get_coordinates()
        return random.choice(get_available_directions(self.grid, i, j))

    def get_coordinates(self):
        j = self.rect.topleft[0] // BLOCK_SIZE
        i = self.rect.topleft[1] // BLOCK_SIZE
        return i, j

    def a_star(self, want_i, want_j):
        i, j = self.get_coordinates()
        visited = {(i, j)}
        prices = dict()

        for node_to_visit_i, node_to_visit_j, direction in get_available_directions_coordinates(self.grid, i, j):
            prices[(node_to_visit_i, node_to_visit_j)] = [
                1 + heuristic(node_to_visit_i, node_to_visit_j, want_i, want_j), direction]

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


def pacman_distance(x1, x2, dimension):
    if x1 > x2:
        x1, x2 = x2, x1
    return min(x2 - x1, x1 + dimension - x2)


def heuristic(x, y, aim_x, aim_y):
    return 1 * (pacman_distance(x, aim_x, DIMENSION_X) + pacman_distance(y, aim_y, DIMENSION_Y))


def get_available_directions_coordinates(grid, i, j):
    dimension_x = len(grid)
    dimension_y = len(grid[0])
    coordinates_list = [[(i + 1) % dimension_x, j % dimension_y, 'down'],
                        [(i - 1) % dimension_x, j % dimension_y, 'up'],
                        [i % dimension_x, (j + 1) % dimension_y, 'right'],
                        [i % dimension_x, (j - 1) % dimension_y, 'left']]
    result = []
    for coordinates in coordinates_list:
        if grid[coordinates[0]][coordinates[1]] != 0:
            result.append(coordinates)

    return result


def get_available_directions(grid, i, j) -> [str]:
    dimension_x = len(grid)
    dimension_y = len(grid[0])
    directions = []
    if grid[(i + 1) % dimension_x][j % dimension_y] != 0:
        directions.append('down')
    if grid[(i - 1) % dimension_x][j % dimension_y] != 0:
        directions.append('up')
    if grid[i % dimension_x][(j + 1) % dimension_y] != 0:
        directions.append('right')
    if grid[i % dimension_x][(j - 1) % dimension_y] != 0:
        directions.append('left')
    return directions


def is_tube(neighbours):
    return len(list(filter(lambda x: x != 0, neighbours))) == 2 and (
            (neighbours[0] != 0 and neighbours[1] != 0) or (neighbours[2] != 0 and neighbours[3] != 0))


def get_cell_neighbours(grid, x, y):
    dimension_x = len(grid)
    dimension_y = len(grid[0])
    neighbours = [grid[(x + 1) % dimension_x][y], grid[(x - 1) % dimension_x][y], grid[x][(y + 1) % dimension_y],
                  grid[x][(y - 1) % dimension_y]]
    return neighbours


class Blinky(Spirit):

    def __init__(self, grid, player_i, player_j):
        super().__init__('./src/sprites/blinky.png', grid, player_i, player_j)


class Clyde(Spirit):

    def __init__(self, grid, player_i, player_j):
        super().__init__('./src/sprites/clyde.png', grid, player_i, player_j)
        self.search = self.breadth_first_search


class Inky(Spirit):

    def __init__(self, grid, player_i, player_j):
        super().__init__('./src/sprites/inky.png', grid, player_i, player_j)
        self.search = self.a_star


class Pinky(Spirit):

    def __init__(self, grid, player_i, player_j):
        super().__init__('./src/sprites/pinky.png', grid, player_i, player_j)
        self.search = self.random_search
