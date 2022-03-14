# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#													   		#
#			     		   Drawing  	    		        #
#			          Developer: Carbon				        #
#													   		#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from config import *
from src.raycasting import *
from src.map import *

# Draw: #

class Render():
	def __init__(self, display, minimap):
		self.display = display
		self.mMap = mMap

	def drawBackground(self, sky : tuple, floor : tuple):
		pygame.draw.rect(self.display, sky, (0, 0, screenWidth, screenHeight // 2))
		pygame.draw.rect(self.display, floor, (0, screenHeight // 2, screenWidth, screenHeight // 2))

	def drawWorld(self, playerPosition : int, playerAngle : int, gameMap):
		rayCasting(self.display, playerPosition, playerAngle, gameMap)

	def drawText(self, text : str, size : int, color : tuple, x : int, y : int):
		image = pygame.font.SysFont('System', size, bold = True).render(text, True, color)
		self.display.blit(image, (x, y))

	def drawMiniMap(self, player):
		self.mMap.fill((0, 0, 0))
		mapX, mapY = player.x // mapScale, player.y // mapScale
		pygame.draw.circle(self.mMap, (217, 18, 34), (int(mapX), int(mapY)), 5)

		for x, y in miniMap:
			pygame.draw.rect(self.mMap, (0, 150, 150), (x, y, mapTile, mapTile))
		self.display.blit(self.mMap, (0, 0))