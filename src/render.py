# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#													   		#
#			     		   Render   	    		        #
#			          Developer: Carbon				        #
#													   		#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from config import pygame, math, deque, screenWidth, screenHeight, mapScale, mapTile
from src.functions import drawSky, loadGameImage
from src.map import mMap, miniMap

# Draw: #

class Render():
	def __init__(self, display, minimap, player):
		self.display = display
		self.mMap = mMap
		self.player = player
		self.textures = {1: loadGameImage('textures/wall.jpg'),
						 2: loadGameImage('textures/wall2.jpg'),
						 3: loadGameImage('textures/wall3.jpg'),
						 9: loadGameImage('textures/sky.jpg'),
		}

		self.shotgunModel = loadGameImage('sprites/weapon/shotgun/idle/0.png')
		self.shotgunAnimation = deque([loadGameImage(f'sprites/weapon/shotgun/shooting/{i}.png') for i in range(20)])

		self.shotgunRect = self.shotgunModel.get_rect()
		self.shotgunPosition = ((screenWidth // 2) - self.shotgunRect.width // 2, screenHeight - self.shotgunRect.height)
		self.shotgunLength = len(self.shotgunAnimation)
		self.shotgunLengthCount = 0 
		self.shotgunAnimationCount = 0
		self.shotgunAnimationSpeed = 3
		self.shotgunAnimationTrigger = True


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

	def drawPlayerWeapon(self):
		if(self.player.shot):
			shotgunSprite = self.shotgunAnimation[0]
			self.display.blit(shotgunSprite, self.shotgunPosition)
			self.shotgunAnimationCount += 1
			if(self.shotgunAnimationCount == self.shotgunAnimationSpeed):
				self.shotgunAnimation.rotate(-1)
				self.shotgunAnimationCount = 0
				self.shotgunLengthCount += 1
				self.shotgunAnimationTrigger = False
			if(self.shotgunLengthCount == self.shotgunLength):
				self.player.shot = False
				self.shotgunLengthCount = 0
				self.shotgunAnimationTrigger = True
		else:
			self.display.blit(self.shotgunModel, self.shotgunPosition)
