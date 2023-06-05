import argparse
import distutils.util
from snake_app import SnakeApp, run, Player, initialize, get_record, display, config
from random import randint
import pygame
import time

class SnakeAgent:
    def __init__(self, snakeApp: SnakeApp):
        self.snakeApp = snakeApp

    def start2(self):
        while(1):
            game, player1, food1, record = initialize(self.snakeApp.record)
            while not game.crash:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

                display(player1, food1, game, record)
                state = game.get_state()
                action = [1, 0, 0]
                player1.do_move(action, player1.x, player1.y, game, food1)
                state = game.get_state()

                game.dont_burn_my_cpu.tick(config['maxfps'])
                #time.sleep(0.5)

            self.snakeApp.record = get_record(game.score, record)
            print('score = ', game.score)


    def start(self):
        while(1):
            game, player1, food1, record = initialize(self.snakeApp.record)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            state = game.get_state()
            if not state['crash']:
                run(game, player1, food1, record)

            self.snakeApp.record = get_record(game.score, record)
            print('score = ', game.score)


class HumanPlay:
    def __init__(self, snakeApp: SnakeApp):
        self.snakeApp = snakeApp

    def play(self):
        pygame.display.set_caption("Keyboard_Input")
        game, player1, food1, record = initialize()
        while not game.crash:
            print('human')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            display(player1, food1, game, record)

            key_input = pygame.key.get_pressed()
            if key_input[pygame.K_LEFT]:
                action = [1, 0, 0]
                player1.do_move(action, player1.x, player1.y, game, food1)
            if key_input[pygame.K_UP]:
                action = [1, 0, 0]
                player1.do_move(action, player1.x, player1.y, game, food1)
            if key_input[pygame.K_RIGHT]:
                action = [1, 0, 0]
                player1.do_move(action, player1.x, player1.y, game, food1)
            if key_input[pygame.K_DOWN]:
                action = [1, 0, 0]
                player1.do_move(action, player1.x, player1.y, game, food1)

            time.sleep(0.5)



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
        agent.start2()
