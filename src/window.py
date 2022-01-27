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
	def __init__(self, screen_width, screen_height):
		self.window = pygame.display.set_mode((screen_width, screen_height))
		self.gameRunning = True

	def updateDisplay(self):
		pygame.display.update()