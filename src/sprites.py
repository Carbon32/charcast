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

# Sprites: #

class Sprite():
	def __init__(self):
		self.spriteTypes = {
			'barrel': loadGameImage('sprites/barrel/0.png'),
			'steve': loadGameImage('sprites/steve/0.png'),
			'round': [loadGameImage(f'sprites/guy/{i}.png') for i in range(8)]
		}

		self.objectsList = [
            Object(self.spriteTypes['round'], False, (5, 5), -0.7, 0.7),
		]

# Objects: #

class Object():
	def __init__(self, object, static, position, height, scale):
		self.object = object
		self.static = static
		self.position = self.x, self.y = position[0] * tile, position[1] * tile
		self.height = height
		self.scale = scale

		if not static:
			self.spriteAngles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
			self.spritePositions = {angle: position for angle, position in zip(self.spriteAngles, self.object)}

	def locateObject(self, player, walls):
		fakeWalls0 = [walls[0] for i in range(100)]
		fakeWalls1 = [walls[-1] for i in range(100)]
		fakeWalls = fakeWalls0 + walls + fakeWalls1

		dx, dy = self.x - player.x, self.y - player.y
		distanceToSprite = math.sqrt(dx ** 2 + dy ** 2)

		theta = math.atan2(dy, dx)
		gamma = theta - player.angle
		if(dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0):
			gamma += (math.pi * 2)

		deltaRays = int(gamma / deltaAngle)
		currentRay = centerRay + deltaRays
		distanceToSprite *= math.cos((fov // 2) - currentRay * deltaAngle)

		fakeRay = currentRay + 100
		if(0 <= fakeRay <= rays - 1 + 2 * 100 and distanceToSprite < fakeWalls[fakeRay][0]):
			projectionHeight = int(projection / distanceToSprite * self.scale)
			height = (projectionHeight // 2) * self.height

			if not self.static:
				if theta < 0:
					theta += (math.pi * 2)
				theta = 360 - int(math.degrees(theta))

				for angles in self.spriteAngles:
					if(theta in angles):
						self.object = self.spritePositions[angles]
						break

			spritePosition = (currentRay * scale - (projectionHeight // 2), (screenHeight // 2) - ((projectionHeight // 2) + height))
			sprite = resizeImage(self.object, (projectionHeight, projectionHeight))
			return (distanceToSprite, sprite, spritePosition)
		else:
			return (False,)