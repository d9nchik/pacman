from timeit import default_timer as timer

from consoleGame.enemies import Inky, Pinky
from consoleGame.environment import read_environment_from_file
from consoleGame.player import Player, ExpectPacman
from consoleGame.settings import *


class Game(object):

    def __init__(self, records, clever_enemies=2, dum_enemies=2, strategy='mini'):
        self.records = records

        self.game_over = False
        self.win = False
        self.life = MAX_LIFE_LEVEL
        # font for score on the screen
        self.score = 0
        self.level = 1
        # Static grid
        self.grid = read_environment_from_file()

        # paths blocks
        self.dots_group = []
        self.start = timer()

        for i, row in enumerate(self.grid):
            for j, item in enumerate(row):
                if item != 0:
                    self.dots_group.append((i, j))

        self.enemies = []
        self.player = Player(self.grid, self.dots_group, self.enemies) if strategy == 'mini' \
            else ExpectPacman(self.grid, self.dots_group, self.enemies)

        for x in range(clever_enemies):
            self.enemies.append(Inky(self.grid, self.player.current_x, self.player.current_y))
        for x in range(dum_enemies):
            self.enemies.append(Pinky(self.grid, self.player.current_x, self.player.current_y))

        self.hit = 0

    def run_logic(self):
        if not self.game_over:
            self.hit += 1
            self.player.update()
            if (self.player.current_x, self.player.current_y) in self.dots_group:
                self.dots_group.remove((self.player.current_x, self.player.current_y))
                self.score += 1
                self.hit = 0
            if self.life > 1:
                if (self.player.current_x, self.player.current_y) in map(
                        lambda enemy: (enemy.current_x, enemy.current_y), self.enemies):
                    self.decrease_life_level()
            else:
                if (self.player.current_x, self.player.current_y) in map(
                        lambda enemy: (enemy.current_x, enemy.current_y), self.enemies):
                    self.life = 0
                    self.player.explosion = True
            self.game_over = self.player.game_over

            for enemy in self.enemies:
                enemy.update(self.player.current_x, self.player.current_y)
            if self.hit == 100:
                self.__init__(self.records)
                return
            # win effect
            if len(self.dots_group) == 0:
                self.increase_level()

            if self.level == MAX_LEVEL + 1:
                self.game_over = True
                self.win = True
            if self.game_over:
                end = timer()
                time = round(end - self.start, 3)
                self.records.add_score(self.score, self.win, time)

    def decrease_life_level(self):
        self.life -= 1
        self.player = Player(self.grid, self.dots_group, self.enemies)

    def increase_level(self):
        level = self.level + 1
        score = self.score
        life = self.life
        start = self.start
        self.__init__(self.records)
        self.start = start
        self.level = level
        self.life = life
        self.score = score
        self.game_over = False

    def draw_game(self):
        print("Score: {}; Level: {}: HP: {}".format(self.score, self.level, self.life))
        print('Player coordinates: {} {}'.format(self.player.current_x, self.player.current_y))
