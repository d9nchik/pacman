import argparse

import pygame.mixer

from src.game import Game
from src.menu import Menu
from src.records import Records
from src.settings import *


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [-v=2] [-c=2] [-s=mini]",
        description="Pacman AI simulator"
    )
    parser.add_argument("-v", "--version", action="version", version=f"{parser.prog} version 1.0.0")

    parser.add_argument('-c', '--clever_enemies', type=int, dest="clever_enemies", default=2,
                        help='provide an integer (default: 2)')
    parser.add_argument('-d', '--dum_enemies', type=int, dest="dum_enemies", default=2,
                        help='provide an integer (default: 2)')
    parser.add_argument('-s', '--strategy', dest="strategy", choices=['mini', 'expecti'], default='mini',
                        help='provide string value  (default: mini)')
    return parser


class GameWindow:
    def __init__(self, screen):
        parser = init_argparse()
        args = parser.parse_args()
        self.strategy = args.strategy
        self.dum_enemies = args.dum_enemies
        self.clever_enemies = args.clever_enemies

        self.screen = screen

        self.records_page = False
        # font for score on the screen
        self.font = pygame.font.Font(None, 35)

        self.records = Records(RECORDS_PATH, self.clever_enemies, self.dum_enemies, self.strategy)
        self.game = Game(self.records, self.clever_enemies, self.dum_enemies, self.strategy)

        self.menu = Menu(("Start", "Records", "Exit"), font_color=WHITE, font_size=60)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            self.menu.event_handler(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.game.game_over and not self.records_page:
                        if self.menu.state == 0:
                            # start
                            self.game = Game(self.records, self.clever_enemies, self.dum_enemies, self.strategy)
                            self.game.game_over = False
                        elif self.menu.state == 1:
                            # records
                            self.records_page = True
                        elif self.menu.state == 2:
                            # exit
                            return True

                elif event.key == pygame.K_ESCAPE:
                    if self.game.game_over:
                        self.game.score = 0
                    else:
                        self.records.add_score(self.game.score, False)
                    self.game.game_over = True
                    self.records_page = False

        return False

    def run_logic(self):
        self.game.run_logic()

    def display_frame(self) -> None:
        # clear the screen
        self.screen.fill(BLACK)
        if self.game.game_over:
            if self.game.score:
                message = 'You win)' if self.game.win else 'You lose('
                self.display_message("Game Over! {} Final Score: {}".format(message, self.game.score), WHITE)
            elif self.records_page:
                self.display_message_block(self.records.get_scores())
            else:
                self.menu.display_frame(self.screen)
        else:
            self.game.draw_game(self.screen)

        # update the screen with new draw
        pygame.display.flip()

    def display_message(self, message, color=RED) -> None:
        label = self.font.render(message, True, color)
        width = label.get_width()
        height = label.get_height()
        # get the position of the label
        pos_x = SCREEN_WIDTH / 2 - width / 2
        pos_y = SCREEN_HEIGHT / 2 - height / 2
        # draw label
        self.screen.blit(label, (pos_x, pos_y))

    def display_message_block(self, message_block: [str]) -> None:
        if len(message_block) == 0:
            self.display_message(self.screen, 'No records')
            return

        number_of_messages = len(message_block)
        list_of_labels = list(map(lambda message: self.font.render(str(message), True, WHITE), message_block))
        height = list_of_labels[0].get_height() + 2
        # get the position of the label
        pos_x = SCREEN_WIDTH * 0.3
        pos_y = SCREEN_HEIGHT / 2 - height * number_of_messages / 2
        # draw label
        for label in list_of_labels:
            self.screen.blit(label, (pos_x, pos_y))
            pos_y += height
