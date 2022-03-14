# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#													   		#
#			     		   Drawing  	    		        #
#			          Developer: Carbon				        #
#													   		#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from config import *
from src.raycasting import *

# Draw: #

class Render():
	def __init__(self, display):
		self.display = display

	def drawBackground(self, sky : tuple, floor : tuple):
		pygame.draw.rect(self.display, sky, (0, 0, screenWidth, screenHeight // 2))
		pygame.draw.rect(self.display, floor, (0, screenHeight // 2, screenWidth, screenHeight // 2))

	def drawWorld(self, playerPosition : int, playerAngle : int, gameMap):
		rayCasting(self.display, playerPosition, playerAngle, gameMap)

	def drawText(self, text : str, size : int, color : tuple, x : int, y : int):
		image = pygame.font.SysFont('System', size, bold = True).render(text, True, color)
		self.display.blit(image, (x, y))