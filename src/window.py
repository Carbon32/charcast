# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#													   		#
#			     		Window Class	    		        #
#			          Developer: Carbon				        #
#													   		#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

import pygame

# Pygame Initialization: #

pygame.init()

# Window: 

class Window():
	def __init__(self, screen_width : int, screen_height : int):
		self.window = pygame.display.set_mode((screen_width, screen_height))
		self.gameRunning = True

	def draw(self, surface : pygame.Surface, position : int):
		self.window.blit(surface, position)

	def updateDisplay(self):
		for event in pygame.event.get():
			if(event.type == pygame.QUIT):
				self.gameRunning = False

			if(pygame.key.get_pressed()[pygame.K_ESCAPE]):
				self.gameRunning = False
		pygame.display.update()