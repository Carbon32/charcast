# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                           #
#                     Python Raycasting                     #
#                     Developer: Carbon                     #
#                                                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: # 

from src.modules import *

# Map: #

class Map():
    def __init__(self, game):

        # Game: 

        self.game = game

        # Mini-Map:

        _ = False
        self.game.mini_map = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
            [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
            [1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, _, _, 1, 1, 1],
            [1, _, _, 2, _, _, _, 2, _, _, _, _, _, _, _, 1],
            [1, _, _, 2, _, _, _, 2, _, _, _, _, _, _, _, 1],
            [1, _, _, 2, _, _, _, 2, 2, _, _, _, _, _, _, 1],
            [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
            [1, _, _, 2, _, _, _, 2, _, _, _, 2, 2, 2, 2, 1],
            [1, _, _, 2, _, _, _, 2, _, _, _, _, _, _, _, 1],
            [1, _, _, 2, _, _, _, 2, _, _, _, _, _, _, _, 1],
            [1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1],

        ]

        # Load Map:

        self.load_map()

    def load_map(self):
        for j, row in enumerate(self.game.mini_map):
            for i, value in enumerate(row):
                if(value):
                    self.game.world_map[(i, j)] = value

    def draw_map(self):
        if(self.game.map_status):
            for j, row in enumerate(self.game.mini_map):
                for i, value in enumerate(row):
                    pygame.draw.rect(self.game.display, (0, 0, 0), (i * (self.game.screen_width // 80), j * (self.game.screen_width // 80), (self.game.screen_width // 80), (self.game.screen_width // 80)))

            for position in self.game.world_map:
                pygame.draw.rect(self.game.display, (205, 92, 92), (position[0] * (self.game.screen_width // 80), position[1] * (self.game.screen_width // 80), (self.game.screen_width // 80), (self.game.screen_width // 80)))
                pygame.draw.rect(self.game.display, (255, 255, 255), (position[0] * (self.game.screen_width // 80), position[1] * (self.game.screen_width // 80), (self.game.screen_width // 80), (self.game.screen_width // 80)), self.game.screen_width // 512)