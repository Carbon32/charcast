# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#													   		#
#			     			Sprites	  		  				#
#			          Developer: Carbon				        #
#													   		#
#														    #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Imports: #

from config import *
from src.functions import *

# Sprite: #

class Sprite():
	def __init__(self):
		self.spriteTypes = {
			'barrel': loadGameImage('sprites/barrel/0.png'),
			'steve': loadGameImage('sprites/steve/0.png'),
		}

		self.objectsList = [
			Object(self.spriteTypes['steve'], True, (5, 5), -0.7, 0.7),
		]

class Object():
	def __init__(self, object, static, position, height, scale):
		self.object = object
		self.static = static
		self.position = self.x, self.y = position[0] * tile, position[1] * tile
		self.height = height
		self.scale = scale

	def locateObject(self, player, walls):
		dx, dy = self.x - player.x, self.y - player.y
		distanceToSprite = math.sqrt(dx ** 2 + dy ** 2)

		theta = math.atan2(dy, dx)
		gamma = theta - player.angle
		if(dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0):
			gamma += (math.pi * 2)

		deltaRays = int(gamma / deltaAngle)
		currentRay = centerRay + deltaRays
		distanceToSprite *= math.cos((fov // 2) - currentRay * deltaAngle)

		if(0 <= currentRay <= rays - 1 and distanceToSprite < walls[currentRay][0]):
			projectionHeight = int(projection / distanceToSprite * self.scale)
			height = (projectionHeight // 2) * self.height

			spritePosition = (currentRay * scale - (projectionHeight // 2), (screenHeight // 2) - ((projectionHeight // 2) + height))
			sprite = resizeImage(self.object, (projectionHeight, projectionHeight))
			return (distanceToSprite, sprite, spritePosition)
		else:
			return (False,)



