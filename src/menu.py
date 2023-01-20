# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                           #
#                     Python Raycasting                     #
#                     Developer: Carbon                     #
#                                                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *
from src.button import *

# Menu: #

class Menu():
	def __init__(self, game):

		# Game:

		self.game = game

		# Restart:

		self.restart = False

		# Buttons:

		self.play_button = Button(self.game, 'Play', self.game.screen_width // 2 - (self.game.screen_width // 8), self.game.screen_height // 2 - (self.game.screen_height // 8), self.game.screen_width // 4, self.game.screen_width // 12, self.game.screen_width // 80, 'large')
		self.exit_button = Button(self.game, 'Exit', self.game.screen_width // 2 - (self.game.screen_width // 8), self.game.screen_height // 3 + (self.game.screen_height // 4), self.game.screen_width // 4, self.game.screen_width // 12, self.game.screen_width // 80, 'large')
		self.back_button = Button(self.game, 'Back', self.game.screen_width // 2 - (self.game.screen_width // 32),  self.game.screen_height // 3 + (self.game.screen_height // 2), self.game.screen_width // 14, self.game.screen_width // 20, self.game.screen_width // 256, 'small')

	def handle_menu(self):
		if(self.game.menu_on):
			pygame.mouse.set_visible(True)
			self.game.display.fill((123, 104, 238))
			if(self.play_button.render()):
				self.restart = True
				self.game.menu_on = False

			if(self.exit_button.render()):
				self.game.engine_running = False
				quit()

			if(self.game.game_started):
				self.play_button.change_text('large', 'Restart')
				if(self.back_button.render()):
					self.game.menu_on = False
