import pygame
import sys
import time
import numpy as np
from random import randint

'''
Tipke za upravljanje:
Left - kretanje lijevo
Right - kretanje desno
Up - kretanje gore
Down - kretanje dolje
Escape - izlaz iz igre
P - pauziranje igre
'''

config = {
    'cell_size': 20,
    'cols': 30,
    'rows': 30,
    'delay': 750,
    'maxfps': 30
}

black = (0, 0, 0)
white = (255, 255, 255)
green = (119, 221, 119)
red = (139, 0, 0)
blue = (41, 136, 181)


class SnakeApp(object):
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(250, 25)
        self.width = config['cell_size']*config['cols']
        self.height = config['cell_size']*config['rows']

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake Game')
        self.font = pygame.font.SysFont('Arial', 20)
        self.click = False
        self.clock = pygame.time.Clock()
        self.record = 0

        #self.actions = []
        #self.needs_actions = True

        #self.init_game()
        self.main_menu()
        self.human = False


    def main_menu(self):
        intro = True

        while intro:
            self.screen.fill(black)
            self.draw_text('Main Menu', self.font, white, self.screen, 260, 80)

            # kreiranje buttona
            button_1 = pygame.Rect(200, 140, 200, 50)
            button_2 = pygame.Rect(200, 220, 200, 50)

            mx, my = pygame.mouse.get_pos()
            if button_1.collidepoint((mx, my)):
                if self.click:
                    # initialize()
                    # self.human = True
                    # print('tu sam')
                    #humanPlay()
                    config['human'] = True
                    intro = False

            if button_2.collidepoint((mx, my)):
                if self.click:
                    #()
                    config['human'] = False
                    pygame.event.set_blocked(pygame.MOUSEMOTION)
                    intro = False

            pygame.draw.rect(self.screen, blue, button_1, border_radius=15)
            pygame.draw.rect(self.screen, blue, button_2, border_radius=15)

            # writing text on top of button
            self.draw_text('Play Snake', self.font, white, self.screen, 260, 155)
            self.draw_text('Train', self.font, white, self.screen, 280, 235)

            self.click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True

            pygame.display.update()
            self.clock.tick(60)


    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)



class Game(object):
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(250, 25)
        self.width = config['cell_size']*config['cols']
        self.height = config['cell_size']*config['rows']
        self.gameDisplay = pygame.display.set_mode((self.width, self.height))
        self.gameDisplay.fill(white)

        pygame.display.set_caption('Snake Game')
        self.font = pygame.font.SysFont('Arial', 20)
        self.dont_burn_my_cpu = pygame.time.Clock()

        self.actions = []
        self.needs_actions = True

        self.crash = False
        self.player = Player(self)
        self.food = Food()
        self.score = 0
        self.human = True

        #self.init_game()

        #pygame.display.flip()
        #pygame.display.update()
        #self.clock.tick(60)

    # pokrece igru
    # def init(self):
    #     # upravljanje preko tipkovnice
    #     self.key_actions = {
    #         'ESCAPE': self.quit,
    #         'LEFT': lambda: self.move(0),
    #         'RIGHT': lambda: self.move(1),
    #         'UP': lambda: self.move(2),
    #         'DOWN': lambda: self.move(3),
    #         'p': self.pause,
    #         'SPACE': self.start_game
    #     }
    #
    #     self.crash = False
    #     self.paused = False
    #
    #     # timer ?
    #     pygame.time.set_timer(pygame.USEREVENT + 1, config['delay'])
    #     self.clock = pygame.time.Clock()
    #
    # def init_game(self):
    #     self.score = 0
    #     return
    #
    # def start_game(self):
    #     print('start')
    #     if self.crash:
    #         self.game = Game()
    #         self.score = 0
    #         #self.init_game()
    #         self.crash = False

    def get_state(self):
        return {"position": np.copy(self.player.position),
                "food_x": self.food.x_food,
                "food_y": self.food.y_food,
                "score": self.score,
                "crash": self.crash,
                "needs_actions": self.needs_actions}



class Food(object):
    def __init__(self):
        self.width = config['cell_size'] * config['cols']
        self.height = config['cell_size'] * config['rows']
        x_rand = randint(0, self.width)
        y_rand = randint(0, self.height)
        # self.x_food = x_rand - x_rand % 20
        # self.y_food = y_rand - y_rand % 20
        self.x_food = x_rand - x_rand % 20
        self.y_food = 0.5 * self.height
        self.image = pygame.image.load('img/food.png')

    def food_coord(self, game, player):
        x_rand = randint(0, game.width)
        self.x_food = x_rand - x_rand % 20
        y_rand = randint(0, game.height)
        self.y_food = y_rand - y_rand % 20
        if [self.x_food, self.y_food] not in player.position:
            return self.x_food, self.y_food
        else:
            self.food_coord(game, player)

    def display_food(self, x, y, game):
        game.gameDisplay.blit(self.image, (x, y))




class Player(object):
    def __init__(self, game):
        x = 0.45 * game.width
        y = 0.5 * game.height
        self.x = x - x % 20
        self.y = y - y % 20
        self.position = []
        self.position.append([self.x, self.y])
        self.food = 1
        self.eaten = False
        self.image = pygame.image.load('img/snake.png')
        self.x_change = 20
        self.y_change = 0
        self.direction = 'right'

    def update_position(self, x, y):
        if self.position[-1][0] != x or self.position[-1][1] != y:
            if self.food > 1:
                for i in range(0, self.food - 1):
                    self.position[i][0], self.position[i][1] = self.position[i + 1]
            self.position[-1][0] = x
            self.position[-1][1] = y

    def do_move(self, move, x, y, game, food):
        move_array = [self.x_change, self.y_change]

        # if self.eaten:
        #     self.position.append([self.x, self.y])
        #     self.eaten = False
        #     self.food = self.food + 1
        if np.array_equal(move, [1, 0, 0]):
            print('1')
            print(self.x_change)
            print(self.y_change)
            move_array = self.x_change, self.y_change
        elif np.array_equal(move, [0, 1, 0]) and self.y_change == 0:  # right - going horizontal
            print('2')
            print(self.x_change)
            print(self.y_change)
            move_array = [0, self.x_change]
        elif np.array_equal(move, [0, 1, 0]) and self.x_change == 0:  # right - going vertical
            print('3')
            print(self.x_change)
            print(self.y_change)
            move_array = [-self.y_change, 0]
        elif np.array_equal(move, [0, 0, 1]) and self.y_change == 0:  # left - going horizontal
            print('4')
            print(self.x_change)
            print(self.y_change)
            move_array = [0, -self.x_change]
        elif np.array_equal(move, [0, 0, 1]) and self.x_change == 0:  # left - going vertical
            print('5')
            print(self.x_change)
            print(self.y_change)
            move_array = [self.y_change, 0]
        self.x_change, self.y_change = move_array
        self.x = x + self.x_change
        self.y = y + self.y_change

        if self.x < 20 or self.x > game.width \
                or self.y < 20 \
                or self.y > game.height \
                or [self.x, self.y] in self.position:
            game.crash = True
        eat(self, food, game)
        if self.eaten:
            self.position.append([self.x, self.y])
            self.eaten = False
            self.food = self.food + 1

        self.update_position(self.x, self.y)

    def do_move2(self, move, x, y, game, food):
        move_array = [self.x_change, self.y_change]
        done = True

        if self.direction == 'right':
            if move == 'down':
                move_array = [0, self.x_change]
            elif move == 'right':
                move_array = self.x_change, self.y_change
            elif move == 'up':
                move_array = [0, -self.x_change]
            else:
                done = False
        if self.direction == 'up':
            if move == 'left':
                move_array = [self.y_change, 0]
            elif move == 'up':
                move_array = self.x_change, self.y_change
            elif move == 'right':
                move_array = [-self.y_change, 0]
            else:
                done = False
        if self.direction == 'left':
            if move == 'up':
                move_array = [0, self.x_change]
            elif move == 'left':
                move_array = self.x_change, self.y_change
            elif move == 'down':
                move_array = [0, -self.x_change]
            else:
                done = False
        if self.direction == 'down':
            if move == 'left':
                move_array = [-self.y_change, 0]
            elif move == 'down':
                move_array = self.x_change, self.y_change
            elif move == 'right':
                move_array = [self.y_change, 0]
            else:
                done = False
        if done:
            self.direction = move

        self.x_change, self.y_change = move_array
        self.x = x + self.x_change
        self.y = y + self.y_change

        if self.x < 20 or self.x > game.width \
                or self.y < 20 \
                or self.y > game.height \
                or [self.x, self.y] in self.position:
            game.crash = True
        eat(self, food, game)
        if self.eaten:
            self.position.append([self.x, self.y])
            self.eaten = False
            self.food = self.food + 1

        self.update_position(self.x, self.y)

    def display_player(self, x, y, food, game):
        self.position[-1][0] = x
        self.position[-1][1] = y

        if game.crash == False:
            for i in range(food):
                x_temp, y_temp = self.position[len(self.position) - 1 - i]
                game.gameDisplay.blit(self.image, (x_temp, y_temp))
        else:
            pygame.time.wait(300)




def eat(player, food, game):
    if player.x == food.x_food and player.y == food.y_food:
        food.food_coord(game, player)
        player.eaten = True
        game.score = game.score + 1


def get_record(score, record):
    if score >= record:
        return score
    else:
        return record


def display_score(game, score, record):
    #myfont = pygame.font.SysFont('Segoe UI', 20)
    #myfont_bold = pygame.font.SysFont('Segoe UI', 20, True)
    myfont = pygame.font.SysFont('Arial', 20)
    myfont_bold = pygame.font.SysFont('Arial', 20, True)
    text_score = myfont.render('SCORE: ', True, black)
    text_score_number = myfont.render(str(score), True, black)
    text_highest = myfont.render('HIGH SCORE: ', True, black)
    text_highest_number = myfont_bold.render(str(record), True, black)
    game.gameDisplay.blit(text_score, (10, 10))
    game.gameDisplay.blit(text_score_number, (90, 10))
    game.gameDisplay.blit(text_highest, (10, 35))
    game.gameDisplay.blit(text_highest_number, (130, 35))
    #game.gameDisplay.blit(game.bg, (10, 10))


def display(player, food, game, record):
    game.gameDisplay.fill(white)
    display_score(game, game.score, record)
    player.display_player(player.position[-1][0], player.position[-1][1], player.food, game)
    food.display_food(food.x_food, food.y_food, game)
    update_screen()


def update_screen():
    pygame.display.update()
    # pygame.event.get() # <--- Add this line (for MAC users) if having problems with UI ###

def initialize_game(player, game, food, agent, batch_size, is_train):
    state_init1 = agent.get_state(game, player, food)  # [0 0 0 0 0 0 0 0 0 1 0 0 0 1 0 0]
    action = [1, 0, 0]
    player.do_move(action, player.x, player.y, game, food, agent)
    state_init2 = agent.get_state(game, player, food)
    reward1 = agent.set_reward(player, game.crash)
    if is_train:
        agent.remember(state_init1, action, reward1, state_init2, game.crash)
        agent.replay_mem(agent.memory, batch_size)

def initialize(record=0):
    pygame.init()
    if record == 0:
        record = 0
    else:
        record = record
    game = Game()
    player1 = game.player
    food1 = game.food
    return game, player1, food1, record

def run(game, player1, food1, record):
    # pygame.init()
    # record = 0
    # game = Game()
    # player1 = game.player
    # food1 = game.food
    print('run')

    while not game.crash:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Initialize classes

        display(player1, food1, game, record)

        state = game.get_state()
        action = [1, 0, 0]
        player1.do_move(action, player1.x, player1.y, game, food1)
        state = game.get_state()

        game.dont_burn_my_cpu.tick(config['maxfps'])
        #time.sleep(0.5)

    while not game.crash:
        display(player1, food1, game, record)


def humanPlay():
    print('human in snake_app')
    pygame.init()
    game, player1, food1, record = initialize()
    game.human = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    # Initialize classes
    game = Game()
    player1 = game.player
    food1 = game.food

    display(player1, food1, game, record)

