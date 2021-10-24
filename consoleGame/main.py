from consoleGame.game import Game
from consoleGame.records import Records
from consoleGame.settings import *

if __name__ == '__main__':
    algo = 'mini'
    for clever in range(1, 11):
        print('Start clever: {}'.format(clever))
        records = Records(RECORDS_PATH, clever, 0, algo)
        for x in range(100):
            game = Game(records, clever, 0, algo)
            # Max: 290
            # print(len(game.dots_group))

            while not game.game_over:
                game.run_logic()
                # game.draw_game()
            print('End, {}'.format(x))
