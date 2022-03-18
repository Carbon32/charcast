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
		self.spriteParameters = {
			'explosion': {
				'sprite': loadGameImage('sprites/explosion/0.png'),
				'viewAngles': None,
				'height': 0.5,
				'scale': 5.0,
				'animation': deque(
					[loadGameImage(f'sprites/explosion/{i}.png') for i in range(18)]),
				'animationDistance': 1000,
				'animationSpeed': 2,
				'collision': False,
			},

			'barrel': {
				'sprite': loadGameImage('sprites/barrel/0.png'),
				'viewAngles': None,
				'height': 0.0,
				'scale': 1.0,
				'animation': deque(
					[loadGameImage(f'sprites/barrel/{i}.png') for i in range(0)]),
				'animationDistance': 0,
				'animationSpeed': 0,
				'collision': True,
			},
		}

		self.objectsList = [
            Object(self.spriteParameters['explosion'], (10.0, 2.0)),
            Object(self.spriteParameters['barrel'], (20.0, 8.0)),
		]

# Objects: #

class Object():
	def __init__(self, parameters, position):
		self.object = parameters['sprite']
		self.viewAngles = parameters['viewAngles']
		self.x, self.y = position[0] * tile, position[1] * tile
		self.height = parameters['height']
		self.scale = parameters['scale']
		self.animation = parameters['animation']
		self.animatinDistance = parameters['animationDistance']
		self.animationSpeed = parameters['animationSpeed']
		self.collision = parameters['collision']
		self.sideCollision = 30
		self.animationCount = 0
		self.position = self.x - self.sideCollision // 2, self.y - self.sideCollision // 2


		if(self.viewAngles):
			self.spriteAngles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
			self.spritePositions = {angle: position for angle, position in zip(self.spriteAngles, self.object)}

	def locateObject(self, player):
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
		if(0 <= fakeRay <= fakeRaysRange and distanceToSprite > 30):
			projectionHeight = min(int(projection / distanceToSprite * self.scale), screenHeight * 2)
			height = (projectionHeight // 2) * self.height

			if self.viewAngles:
				if theta < 0:
					theta += (math.pi * 2)
				theta = 360 - int(math.degrees(theta))

				for angles in self.spriteAngles:
					if(theta in angles):
						self.object = self.spritePositions[angles]
						break

			spriteObject = self.object
			if(self.animation and distanceToSprite < self.animatinDistance):
				spriteObject = self.animation[0]

				if(self.animationCount < self.animationSpeed):
					self.animationCount += 1

				else:
					self.animation.rotate()
					self.animationCount = 0

			spritePosition = (currentRay * scale - (projectionHeight // 2), (screenHeight // 2) - ((projectionHeight // 2) + height))
			sprite = resizeImage(spriteObject, (projectionHeight, projectionHeight))
			return (distanceToSprite, sprite, spritePosition)
		else:
			return (False,)