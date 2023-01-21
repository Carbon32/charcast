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

		self.play_button = Button(self.game, 'Play', self.game.screen_width // 2 - (self.game.screen_width // 10), self.game.screen_height // 2 - (self.game.screen_height // 8), self.game.screen_width // 4, self.game.screen_width // 12, self.game.screen_width // 80, 'large')
		self.exit_button = Button(self.game, 'Exit', self.game.screen_width // 2 - (self.game.screen_width // 10), self.game.screen_height // 3 + (self.game.screen_height // 4), self.game.screen_width // 4, self.game.screen_width // 12, self.game.screen_width // 80, 'large')
		self.back_button = Button(self.game, 'Back', self.game.screen_width // 2 - (self.game.screen_width // 64),  self.game.screen_height // 3 + (self.game.screen_height // 2), self.game.screen_width // 14, self.game.screen_width // 20, self.game.screen_width // 256, 'small')

		# Title:

		self.step = 0
		self.title_background_color = (184, 160, 238)

	def handle_menu(self):
		if(self.game.menu_on):
			self.game.display.fill((40, 42, 53))
			bounce = -1 * math.sin(self.step) * self.game.screen_width // 64
			pygame.draw.rect(self.game.display, self.title_background_color, pygame.Rect(self.game.screen_width // 3.7, self.game.screen_height // 24 + bounce, self.game.screen_width - (self.game.screen_width // 2), self.game.screen_height // 5), border_radius = self.game.screen_width // 38)
			pygame.draw.rect(self.game.display, (0, 0, 0), pygame.Rect(self.game.screen_width // 3.7, self.game.screen_height // 24 + bounce, self.game.screen_width - (self.game.screen_width // 2), self.game.screen_height // 5), self.game.screen_width // 128, border_radius = self.game.screen_width // 38)
			self.game.draw_custom_text(self.game.fonts['huge'], 'Raycasting', (0, 0, 0), self.game.screen_width // 2.9, (0 + self.game.screen_height // 12) + bounce)
			self.step += 0.05
			pygame.mouse.set_visible(True)
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
