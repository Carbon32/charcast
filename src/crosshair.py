# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                           #
#                     Python Raycasting                     #
#                     Developer: Carbon                     #
#                                                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: # 

from src.modules import *

# Crosshair: #

class Crosshair():
	def __init__(self, game):

		# Game:

		self.game = game

		# Crosshair:

		self.crosshair = pygame.transform.scale(pygame.image.load('assets/crosshair/crosshair.png'), (self.game.screen_width // 64, self.game.screen_width // 64))

	def render(self):
		self.game.display.blit(self.crosshair, (self.game.screen_width // 2, self.game.screen_height // 2))