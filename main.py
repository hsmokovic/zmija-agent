from snake_app import SnakeApp, run, Player, initialize, get_record
from random import randint
import pygame

class SnakeAgent():
    def __init__(self, snakeApp: SnakeApp):
        self.snakeApp = snakeApp

    def start(self):
        game, player1, food1, record = initialize()

        while(1):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            state = game.get_state()
            if not state['crash']:
                run(game, player1, food1, record)
            record = get_record(game.score, record)


            # if not state['crash'] and not self.snakeApp.actions:
            #     print(state)
            #     print(self.snakeApp.actions)
            #     actions = []
            #
            #     if randint(1, 2) % 1:
            #         actions.append('LEFT')
            #     elif randint(1, 2) % 2:
            #         actions.append('RIGHT')
            #     elif randint(1, 2) % 3:
            #         actions.append('UP')
            #     elif randint(1, 2) % 4:
            #         actions.append('DOWN')
            # self.snakeApp.tick()
            print(game.crash)
            action = [1, 0, 0]




if __name__ == '__main__':
    app = SnakeApp()
    agent = SnakeAgent(app)
    agent.start()
