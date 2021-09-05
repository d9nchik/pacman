import pygame.mixer

from src.enemies import Blinky, Inky, Pinky, Clyde
from src.entity import Block, Ellipse
from src.environment import generate_environment, draw_environment
from src.menu import Menu
from src.player import Player
from src.settings import *


# TODO: add table of records
# TODO: change resolution
# TODO: add rage
# FIXME: refactor

class Game(object):
    def __init__(self):
        self.about = False
        self.game_over = True
        self.win = False
        self.life = MAX_LIFE_LEVEL
        # font for score on the screen
        self.font = pygame.font.Font(None, 35)

        self.menu = Menu(("Start", "Rules", "Exit"), font_color=WHITE, font_size=60)

        # load sounds
        self.pacman_sound = pygame.mixer.Sound("./src/sounds/pacman_sound.ogg")
        self.game_over_sound = pygame.mixer.Sound("./src/sounds/game_over_sound.ogg")
        self.win_sound = pygame.mixer.Sound('./src/sounds/win.ogg')
        self.hurt = pygame.mixer.Sound('./src/sounds/hurt.wav')
        self.upgrade = pygame.mixer.Sound('./src/sounds/upgrade.wav')

        self.score = 0
        self.level = 1
        self.grid = generate_environment()

        self.player = Player(self.grid)
        # paths blocks
        self.empty_blocks = pygame.sprite.Group()
        self.non_empty_blocks = pygame.sprite.Group()
        self.dots_group = pygame.sprite.Group()

        for i, row in enumerate(self.grid):
            for j, item in enumerate(row):
                if item == 0:
                    self.empty_blocks.add(
                        Block(j * BLOCK_SIZE + 8, i * BLOCK_SIZE + 8, BLACK, HALF_BLOCK_SIZE + 4, HALF_BLOCK_SIZE + 4))
                else:
                    self.non_empty_blocks.add(
                        Block(j * BLOCK_SIZE + QUARTER_BLOCK_SIZE, i * BLOCK_SIZE + QUARTER_BLOCK_SIZE, BLACK,
                              HALF_BLOCK_SIZE, HALF_BLOCK_SIZE))
                    self.dots_group.add(Ellipse(j * BLOCK_SIZE + 12, i * BLOCK_SIZE + 12, WHITE, QUARTER_BLOCK_SIZE,
                                                QUARTER_BLOCK_SIZE))

        self.enemies = pygame.sprite.Group()
        self.enemies.add(Blinky(self.grid))
        self.enemies.add(Clyde(self.grid))
        self.enemies.add(Inky(self.grid))
        self.enemies.add(Pinky(self.grid))

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            self.menu.event_handler(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.game_over and not self.about:
                        if self.menu.state == 0:
                            # start
                            self.__init__()
                            self.game_over = False
                        elif self.menu.state == 1:
                            # rules
                            self.about = True
                        elif self.menu.state == 2:
                            # exit
                            return True

                elif event.key == pygame.K_RIGHT:
                    self.player.move_right()

                elif event.key == pygame.K_LEFT:
                    self.player.move_left()

                elif event.key == pygame.K_UP:
                    self.player.move_up()

                elif event.key == pygame.K_DOWN:
                    self.player.move_down()

                elif event.key == pygame.K_ESCAPE:
                    if self.game_over:
                        self.score = 0
                    self.game_over = True
                    self.about = False

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.player.stop_move_right()
                elif event.key == pygame.K_LEFT:
                    self.player.stop_move_left()
                elif event.key == pygame.K_UP:
                    self.player.stop_move_up()
                elif event.key == pygame.K_DOWN:
                    self.player.stop_move_down()

        return False

    def run_logic(self):
        if not self.game_over:
            self.player.update(self.empty_blocks)
            block_hit_list = pygame.sprite.spritecollide(self.player, self.dots_group, True)
            if len(block_hit_list) > 0:
                self.pacman_sound.play()
                self.score += len(block_hit_list)
            if self.life != 1:
                block_hit_list = pygame.sprite.spritecollide(self.player, self.enemies, False)
                if len(block_hit_list) > 0:
                    self.decrease_life_level()
            else:
                block_hit_list = pygame.sprite.spritecollide(self.player, self.enemies, True)
                if len(block_hit_list) > 0:
                    self.life -= 1
                    self.player.explosion = True
                    self.game_over_sound.play()
            self.game_over = self.player.game_over
            self.enemies.update()
            # win effect
            if len(self.dots_group) == 0:
                self.upgrade.play()
                self.increase_level()

            if self.level == MAX_LEVEL + 1:
                self.game_over = True
                self.about = False
                self.win = True
                self.win_sound.play()

    def decrease_life_level(self):
        self.life -= 1
        self.player = Player(self.grid)
        self.hurt.play()

    def increase_level(self):
        level = self.level + 1
        score = self.score
        life = self.life
        self.__init__()
        self.level = level
        self.life = life
        self.score = score
        self.game_over = False

    def display_frame(self, screen):
        # clear the screen
        screen.fill(BLACK)
        if self.game_over:
            if self.score:
                message = 'You win)' if self.win else 'You lose('
                self.display_message(screen, "Game Over! {} Final Score: {}".format(message, self.score), WHITE)
            elif self.about:
                self.display_message(screen, "It is an arcade Game")
                # "a maze containing various dots,\n"
                # known as Pac-Dots, and four ghosts.\n"
                # "The four ghosts roam the maze, trying to kill Pac-Man.\n"
                # "If any of the ghosts hit Pac-Man, he loses a life;\n"
                # "the game is over.\n")
            else:
                self.menu.display_frame(screen)
        else:
            # draw game
            draw_environment(screen, self.grid)
            self.dots_group.draw(screen)
            self.enemies.draw(screen)
            screen.blit(self.player.image, self.player.rect)
            # Render the text for the score
            text = self.font.render("Score: {}; Level: {}: HP: {}".format(self.score, self.level, self.life), True,
                                    WHITE)
            # put text on screen
            screen.blit(text, [120, 20])

        # update the screen with new draw
        pygame.display.flip()

    def display_message(self, screen, message, color=RED):
        label = self.font.render(message, True, color)
        width = label.get_width()
        height = label.get_height()
        # get the position of the label
        pos_x = (SCREEN_WIDTH / 2) - (width / 2)
        pos_y = (SCREEN_HEIGHT / 2) - (height / 2)
        # draw label
        screen.blit(label, (pos_x, pos_y))
