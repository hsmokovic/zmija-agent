import argparse
from snake_app import SnakeApp, Player, initialize, get_record, display, config, danger, distance2
from neural_network import selection, crossover
from random import randint
import pygame
import time
import numpy as np
from neural_network import NeuralNetwork
import logging

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
        self.generation_size = 50
        self.best_fitness = (0, self.generation_id)
        self.current_id = 0
        self.current_run = 0
        self.current_run_score_sum = 0
        self.runs_per_chromosome = 3

    def start(self):
        population = []
        for i in range(self.generation_size):
            population.append(NeuralNetwork())

        while(1):
            print(f'Generation: {self.generation_id}, record: {self.snakeApp.record}')
            print(population)
            selection(population)
            for neural_network in population:
                while self.current_run != self.runs_per_chromosome:
                    self.play_game()

                    self.current_run += 1
                #print('curent run sum = ', self.current_run_score_sum)
                self.current_id += 1
                self.current_run = 0
                self.current_run_score_sum = 0

            # stvori novu populaciju
            self.generation_id +=1

    def play_game(self):
        # inicijalizacije nove igre
        game, player1, food1, record = initialize(self.snakeApp.record)
        while not game.crash:
            if config['gui']:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

            state = game.get_state()

            actions = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            action = actions[randint(0, 2)]
            #danger(player1, game, action)
            player1.move_ai(action, player1.x, player1.y, game, food1)

            self.snakeApp.record = get_record(game.score, record)
            if config['gui']:
                display(player1, food1, game, self.snakeApp.record)
            # print(player1.direction)

            state = game.get_state()

            if config['gui']:
                game.dont_burn_my_cpu.tick(config['maxfps'])
            #time.sleep(0.1)
        #print(f'score = {game.score}')
        self.current_run_score_sum += game.score


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

            player1.move_human(action, player1.x, player1.y, game, food1)
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

    mama = NeuralNetwork()
    print(mama.weights)
    print(mama.bias)

    tata = NeuralNetwork()
    print(tata.weights)
    print(tata.bias)

    matej = crossover(mama, tata)
    print(matej.weights)
    print(matej.bias)
