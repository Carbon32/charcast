# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                           #
#                     Python Raycasting                     #
#                     Developer: Carbon                     #
#                                                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports:

from src.modules import *
from src.game import *
from src.map import *
from src.player import *
from src.raycasting import *
from src.renderer import *
from src.sprites import *
from src.pathfinding import *
from src.crosshair import *
from src.weapons_manager import *
from src.menu import *
from src.fade import *
from src.sounds import *

# Resolution: #

class Resolution():
    def __init__(self, game):
        
        # Game: 

        self.game = game

        # Display:

        self.resolution_window = pygame.display.set_mode((300, 400))
        pygame.display.set_caption("Raycasting:  ")
        pygame.display.set_icon(pygame.transform.scale(pygame.image.load('assets/icon.png'), (32, 32)))
        self.resolution_status = True

        # Buttons: 

        self.resolution_a = ButtonImage(self.resolution_window, pygame.transform.scale(pygame.image.load('assets/Resolution/B.png'), (150, 100)), 55, 200, 200, 100, 10, 50) # 1280 x 720
        self.resolution_b = ButtonImage(self.resolution_window, pygame.transform.scale(pygame.image.load('assets/Resolution/A.png'), (150, 100)), 55, 50, 200, 100, 10, 50) # 1920 x 1080

    def update_background(self):
        self.resolution_window.fill((40, 42, 53))

    def set_resolution(self, screen_width, screen_height):
        self.game.screen_width = screen_width
        self.game.screen_height = screen_height
        self.resolution_status = False

    def update_window(self):
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                self.resolution_status = False
                exit()

        pygame.display.update()