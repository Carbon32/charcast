# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#													   		#
#			     		Window Class	    		        #
#			          Developer: Carbon				        #
#													   		#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from config import *

# Pygame Initialization: #

pygame.init()

# Window: 

class Window():
	def __init__(self, screen_width : int, screen_height : int):
		self.window = pygame.display.set_mode((screen_width, screen_height))
		self.gameRunning = True

	def clearWindow(self):
		self.window.fill((0, 0, 0))

	def draw(self, surface : pygame.Surface, position : int):
		self.window.blit(surface, position)

	def updateDisplay(self, fps : int):
		fpsHandler.tick(fps)
		for event in pygame.event.get():
			if(event.type == pygame.QUIT):
				self.gameRunning = False

			if(pygame.key.get_pressed()[pygame.K_ESCAPE]):
				self.gameRunning = False
		pygame.display.update()