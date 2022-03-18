# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#													   		#
#			     		   Render   	    		        #
#			          Developer: Carbon				        #
#													   		#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from config import pygame, math, screenWidth, screenHeight, mapScale, mapTile
from src.functions import drawSky, loadGameImage
from src.map import mMap, miniMap

# Draw: #

class Render():
	def __init__(self, display, minimap):
		self.display = display
		self.mMap = mMap
		self.textures = {1: loadGameImage('textures/wall.jpg'),
						 2: loadGameImage('textures/wall2.jpg'),
						 3: loadGameImage('textures/wall3.jpg'),
						 9: loadGameImage('textures/sky.jpg'),
		}

	def drawBackground(self, sky : tuple, floor : tuple, playerAngle : int):
		skyOffset = -10 * math.degrees(playerAngle) % screenWidth
		drawSky(self.display, self.textures[9], skyOffset)
		pygame.draw.rect(self.display, floor, (0, screenHeight // 2, screenWidth, screenHeight // 2))

	def drawWorld(self, worldObjects):
		for obj in sorted(worldObjects, key = lambda n : n[0], reverse = True):
			if(obj[0]):
				_, object, objectPosition = obj
				self.display.blit(object, objectPosition)

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