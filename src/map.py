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
            [1, _, _, _, _, _, _, _, _, _, _, _, _, 2, _, 1],
            [1, _, _, _, _, 2, _, _, _, _, _, _, _, 2, _, 1],
            [2, _, _, _, _, 2, _, _, _, _, _, _, _, 2, _, 1],
            [1, _, _, _, _, 2, 2, 2, 2, _, _, _, _, 2, _, 1],
            [1, _, _, _, _, _, _, _, 2, _, 2, 2, 2, 2, _, 1],
            [1, _, _, _, _, _, _, _, 2, _, _, _, _, _, _, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],

        ]

        # Load Map:

        self.load_map()

    def load_map(self):
        for j, row in enumerate(self.game.mini_map):
            for i, value in enumerate(row):
                if(value):
                    self.game.world_map[(i, j)] = value

    def draw_map(self):
        for position in self.game.world_map:
            pass
            # pygame.draw.rect(self.game.display, (255, 255, 255), (position[0] * (self.game.screen_width // 80), position[1] * (self.game.screen_width // 80), (self.game.screen_width // 100), (self.game.screen_width // 100)), 2)