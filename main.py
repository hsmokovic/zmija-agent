import argparse
import distutils.util
from snake_app import SnakeApp, run, Player, initialize, get_record, display, config, danger, distance2
from random import randint
import pygame
import time
import numpy as np
from neural_network import NeuralNetwork

cant = {
    'down': 'up',
    'up': 'down',
    'left': 'right',
    'right': 'left'
}

class SnakeAgent:
    def __init__(self, snakeApp: SnakeApp):
        self.snakeApp = snakeApp
        self.generation_id = 1
        self.best_fitness = (0, self.generation_id)
        self.current_id = 0
        self.current_run = 0
        self.current_run_score_sum = 0
        self.runs_per_chromosome = 3

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

                # actions = ['right', 'up', 'left', 'down']
                # actions.remove(cant[player1.direction])
                # action = actions[randint(0, 2)]
                # print(action)
                actions = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
                action = actions[randint(0, 2)]
                danger(player1, game, action)
                player1.move_ai(action, player1.x, player1.y, game, food1)

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

            # danger(player1, game, 'left')
            # danger(player1, game, 'right')
            # danger(player1, game, 'forward')
            player1.move_human(action, player1.x, player1.y, game, food1)
            state = game.get_state()
            #print('POSITION: ', state['position'])
            #distance(player1, food1)
            # distance2(player1, food1, 'left')
            # distance2(player1, food1, 'right')
            # distance2(player1, food1, 'forward')
            # print()
            # print()

            self.snakeApp.record = get_record(game.score, record)
            display(player1, food1, game, self.snakeApp.record)

            game.dont_burn_my_cpu.tick(config['playfps'])



if __name__ == '__main__':
    app = SnakeApp()
    if config['human']:
        print('HUMAN')
        human = HumanPlay(app)
        human.play()
    else:
        print('AGENT')
        agent = SnakeAgent(app)
        agent.start()

    mreza = NeuralNetwork()
    # print(mreza.weights)
    # print(mreza.bias)
    #
    # population = []
    # population.append(NeuralNetwork())
    # population.append(NeuralNetwork())
    # print(population[0].weights)

