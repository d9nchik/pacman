import pygame

from src.entity import Entity
from src.settings import *


class Player(pygame.sprite.Sprite, Entity):
    change_x = 0
    change_y = 0
    explosion = False
    game_over = False

    def __init__(self, grid):
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

    def update(self, empty_blocks):
        if not self.explosion:
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

            # This will stop user from moving through walls
            if len(pygame.sprite.spritecollide(self, empty_blocks, False)) > 0:
                self.rect.centerx -= self.change_x
                self.rect.centery -= self.change_y
                self.change_x = 0
                self.change_y = 0

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

    def move_right(self):
        self.change_x = 3

    def move_left(self):
        self.change_x = -3

    def move_up(self):
        self.change_y = -3

    def move_down(self):
        self.change_y = 3

    def stop_move_horizontal(self):
        self.change_x = 0

    def stop_move_vertical(self):
        self.change_y = 0

    def breadth_first_search(self, want_i: int, want_j: int):
        j = self.rect.centerx // BLOCK_SIZE
        i = self.rect.centery // BLOCK_SIZE

        if len(self.grid) <= i or len(self.grid[0]) <= j:
            return [(i, j), (i, j)]

        visited = {(i, j)}
        paths = dict()
        next_nodes_to_visit = get_available_directions_coordinates(self.grid, i, j)
        for node in next_nodes_to_visit:
            paths[node] = [(i, j)]

        while len(next_nodes_to_visit) != 0:
            nodes_to_visit = next_nodes_to_visit
            next_nodes_to_visit = []
            for node_to_visit in nodes_to_visit:
                if node_to_visit not in visited:
                    visited.add(node_to_visit)
                    path = paths.get(node_to_visit)
                    if node_to_visit == (want_i, want_j):
                        return path + [(want_i, want_j)]
                    new_nodes = get_available_directions_coordinates(self.grid, node_to_visit[0],
                                                                     node_to_visit[1])
                    for new_node in new_nodes:
                        paths[new_node] = path + [node_to_visit]
                    next_nodes_to_visit += new_nodes
                    del paths[node_to_visit]
        return [(i, j), (i, j)]

    def deep_first_search(self, want_i: int, want_j: int):
        j = self.rect.centerx // BLOCK_SIZE
        i = self.rect.centery // BLOCK_SIZE

        if len(self.grid) <= i or len(self.grid[0]) <= j:
            return [(i, j), (i, j)]

        visited = {(i, j)}
        path = [(i, j)]
        next_nodes_to_visit = get_available_directions_coordinates(self.grid, i, j)
        while len(next_nodes_to_visit) != 0:
            node_to_visit = next_nodes_to_visit[-1]
            path += [node_to_visit]
            if node_to_visit not in visited:
                visited.add(node_to_visit)
                if node_to_visit == (want_i, want_j):
                    return path
                next_nodes_to_visit += get_available_directions_coordinates(self.grid, node_to_visit[0],
                                                                            node_to_visit[1])
            else:
                path = path[:-1]
                next_nodes_to_visit = next_nodes_to_visit[:-1]
        return [(i, j), (i, j)]

    def uniform_cost_search(self, want_i, want_j):
        j = self.rect.centerx // BLOCK_SIZE
        i = self.rect.centery // BLOCK_SIZE

        if len(self.grid) <= i or len(self.grid[0]) <= j:
            return [(i, j), (i, j)]

        visited = {(i, j)}
        prices = dict()
        previous_points = dict()

        for node_to_visit in get_available_directions_coordinates(self.grid, i, j):
            prices[node_to_visit] = 1
            previous_points[node_to_visit] = (i, j)

        while len(prices) != 0:
            cheapest_node = list(prices.keys())[0]
            cheapest_price = prices[cheapest_node]

            for key, value in prices.items():
                if value < cheapest_price:
                    cheapest_price = value
                    cheapest_node = key

            del prices[cheapest_node]
            if cheapest_node not in visited:
                visited.add(cheapest_node)
                if cheapest_node == (want_i, want_j):
                    path = [cheapest_node]
                    while path[0] in previous_points:
                        path = [previous_points[path[0]]] + path
                    return path
                for node_to_visit in get_available_directions_coordinates(self.grid, cheapest_node[0],
                                                                          cheapest_node[1]):
                    if node_to_visit not in visited \
                            and (node_to_visit not in prices or prices[node_to_visit] > cheapest_price + 1):
                        prices[node_to_visit] = cheapest_price + 1
                        previous_points[node_to_visit] = cheapest_node
        return [(i, j), (i, j)]


def get_available_directions_coordinates(grid, i, j):
    dimension_x = len(grid)
    dimension_y = len(grid[0])
    coordinates_list = [((i + 1) % dimension_x, j), ((i - 1) % dimension_x, j),
                        (i, (j + 1) % dimension_y), (i, (j - 1) % dimension_y)]
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
