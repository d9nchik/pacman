import pygame

from src.entity import Entity
from src.settings import *


class Spirit(pygame.sprite.Sprite, Entity):
    def __init__(self, image_path, grid, player_i, player_j, spirit_x, spirit_y):
        pygame.sprite.Sprite.__init__(self)
        Entity.__init__(self, grid)

        self.change_x = 0
        self.change_y = 0
        # load image
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (spirit_y, spirit_x)
        self.search = self.a_star
        self.change_direction(player_i, player_j)

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

        self.change_direction(player_i, player_j)

    def change_direction(self, player_i, player_j):

        # direction = random.choice(self.get_available_directions())
        direction = self.search(player_i, player_j)
        if direction == "left":
            self.change_x = -BLOCK_SIZE
            self.change_y = 0
        elif direction == "right":
            self.change_x = BLOCK_SIZE
            self.change_y = 0
        elif direction == "up":
            self.change_x = 0
            self.change_y = -BLOCK_SIZE
        elif direction == "down":
            self.change_x = 0
            self.change_y = BLOCK_SIZE

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


class Inky(Spirit):
    def __init__(self, grid, player_i, player_j, inky_x, inky_y):
        super().__init__('./src/sprites/inky.png', grid, player_i, player_j, inky_x, inky_y)
        self.search = self.a_star
