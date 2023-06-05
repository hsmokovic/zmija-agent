import argparse
import distutils.util
from snake_app import SnakeApp, run, Player, initialize, get_record, display, config
from random import randint
import pygame
import time

cant = {
    'down': 'up',
    'up': 'down',
    'left': 'right',
    'right': 'left'
}

class SnakeAgent:
    def __init__(self, snakeApp: SnakeApp):
        self.snakeApp = snakeApp

    def start(self):
        counter = 0
        while(1):
            counter += 1
            game, player1, food1, record = initialize(self.snakeApp.record)
            while not game.crash:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

                state = game.get_state()

                actions = ['right', 'up', 'left', 'down']
                actions.remove(cant[player1.direction])
                action = actions[randint(0, 2)]
                #print(action)
                player1.do_move(action, player1.x, player1.y, game, food1)


                self.snakeApp.record = get_record(game.score, record)
                display(player1, food1, game, self.snakeApp.record)
                #print(player1.direction)

                state = game.get_state()
                game.dont_burn_my_cpu.tick(config['maxfps'])
                #time.sleep(2)

            print(f'{counter}. score={game.score}')


class HumanPlay:
    def __init__(self, snakeApp: SnakeApp):
        self.snakeApp = snakeApp

    def play(self):
        pygame.display.set_caption("Keyboard_Input")
        game, player1, food1, record = initialize()
        action = 'right'
        while not game.crash:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        action = 'left'
                    elif event.key == pygame.K_UP:
                        action = 'up'
                    elif event.key == pygame.K_RIGHT:
                        action = 'right'
                    elif event.key == pygame.K_DOWN:
                        action = 'down'


            player1.do_move(action, player1.x, player1.y, game, food1)
            self.snakeApp.record = get_record(game.score, record)
            display(player1, food1, game, self.snakeApp.record)

            game.dont_burn_my_cpu.tick(config['playfps'])



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--display", nargs='?', type=distutils.util.strtobool, default=True)
    args = parser.parse_args()
    print("Args", args)
    config['display'] = args.display

    app = SnakeApp()
    #print(app.human)
    if config['human']:
        print('HUMAN')
        human = HumanPlay(app)
        human.play()
    else:
        print('AGENT')
        agent = SnakeAgent(app)
        agent.start()
