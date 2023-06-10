import pygame
import time
import numpy as np
import logging
from snake_app import SnakeApp, Player, initialize, get_record, display, config, is_danger, distance, generate_network_input
from neural_network import elitism, selection, crossover
from random import randint
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
        self.generation_size = 50
        self.best_fitness = (0, self.generation_id)
        self.current_id = 0
        self.current_run = 0
        self.current_run_score_sum = 0
        self.runs_per_chromosome = 1

    def start(self):
        population = []
        for i in range(self.generation_size):
            population.append(NeuralNetwork())

        while(1):
            #print(f'Generation: {self.generation_id}, record: {self.snakeApp.record}')
            #print(population)
            #selection(population)
            for neural_network in population:
                while self.current_run != self.runs_per_chromosome:
                    self.play_game(neural_network)
                    self.current_run += 1
                #print('curent run sum = ', self.current_run_score_sum)
                neural_network.fitness = np.round(self.current_run_score_sum/self.runs_per_chromosome, decimals=2)
                self.current_id += 1
                self.current_run = 0
                self.current_run_score_sum = 0

            population.sort(key=lambda x: x.fitness, reverse=True)
            if population[0].fitness > self.best_fitness[0]:
                self.best_fitness = (population[0].fitness, self.generation_id)
            print(f'Generation: {self.generation_id}, best fitness: {self.best_fitness}, record: {self.snakeApp.record}')

            # stvori novu populaciju
            self.generation_id += 1
            new_population = elitism(population)
            parents = set()
            while len(new_population) < self.generation_size:
                parent1 = selection(population)
                parent2 = selection(population)
                if (parent1, parent2) not in parents:
                    parents.add((parent1, parent2))
                    child = crossover(parent1, parent2)
                    child.mutate()
                    new_population.append(child)

            population = new_population.copy()

    def play_game(self, neural_network):
        # inicijalizacije nove igre
        game, player1, food1, record = initialize(self.snakeApp.record)
        no_food = 0
        while not game.crash:
            if config['gui']:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

            # actions = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            # action = actions[randint(0, 2)]
            # is_danger(player1, game, action)
            # print(distance(player1, food1, action))

            state1 = game.get_state()
            network_input = generate_network_input(player1, food1, game)
            #print(network_input)
            action = neural_network.forwad_propagation(network_input)
            #print(action)
            player1.move_ai(action, player1.x, player1.y, game, food1)
            state2 = game.get_state()

            if state2['score'] > state1['score']:
                no_food = 0
            else:
                no_food += 1

            if no_food == 100:
                game.crash = True

            self.snakeApp.record = get_record(game.score, record)
            if config['gui']:
                display(player1, food1, game, self.snakeApp.record)
                game.dont_burn_my_cpu.tick(config['maxfps'])
                #time.sleep(1)

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

    # mama = NeuralNetwork()
    # print(mama.weights)
    # print(mama.bias)
    #
    # tata = NeuralNetwork()
    # print(tata.weights)
    # print(tata.bias)
    #
    # matej = crossover(mama, tata)
    # print(matej.weights)
    # print(matej.bias)
