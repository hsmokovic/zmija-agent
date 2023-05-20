import pygame
import sys
import time

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
    'delay': 750
}

black = (0, 0, 0)
white = (255, 255, 255)
green = (119, 221, 119)
red = (139, 0, 0)

class SnakeApp(object):
    def __init__(self):
        pygame.init()
        #pygame.key.set_repeat(250, 25)
        self.width = config['cell_size']*config['cols']
        self.height = config['cell_size']*config['rows']

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake Game')
        self.font = pygame.font.SysFont('Arial', 20)
        self.click = False
        self.clock = pygame.time.Clock()

        self.actions = []
        self.needs_actions = True

        self.main_menu()
        #self.init_game()

    def init_game(self):
        self.score = 0
        return

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def main_menu(self):
        intro = True

        while intro:
            self.screen.fill(black)
            self.draw_text('Main Menu', self.font, white, self.screen, 250, 80)

            mx, my = pygame.mouse.get_pos()

            # kreiranje buttona
            button_1 = pygame.Rect(200, 140, 200, 50)
            button_2 = pygame.Rect(200, 220, 200, 50)

            if button_1.collidepoint((mx, my)):
                if self.click:
                    self.start_game()
            if button_2.collidepoint((mx, my)):
                if self.click:
                    self.start_game()

            pygame.draw.rect(self.screen, (255, 0, 0), button_1, border_radius=15)
            pygame.draw.rect(self.screen, (255, 0, 0), button_2, border_radius=15)

            # writing text on top of button
            self.draw_text('PLAY SNAKE', self.font, (255, 255, 255), self.screen, 250, 155)
            self.draw_text('TRAIN', self.font, (255, 255, 255), self.screen, 270, 235)

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



    def move(self, where):
        print('!!!')

    def start_game(self):
        if self.gameover:
            self.init_game()
            self.gameover = False

    # pokrece igru
    def init(self):
        # upravljanje preko tipkovnice
        self.key_actions = {
            'ESCAPE': self.quit,
            'LEFT': lambda:self.move(0),
            'RIGHT': lambda:self.move(1),
            'UP': lambda:self.move(2),
            'DOWN': lambda:self.move(3),
            'p': self.pause
        }

        self.gameover = False
        self.paused = False

        # timer ?
        pygame.time.set_timer(pygame.USEREVENT + 1, config['delay'])
        self.clock = pygame.time.Clock()


if __name__ == '__main__':
    App = SnakeApp()
    #App.run()

