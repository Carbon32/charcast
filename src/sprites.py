# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#													   		#
#			     			Sprites	  		  				#
#			          Developer: Carbon				        #
#													   		#
#														    #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Imports: #

from config import math, deque, tile, deltaAngle, centerRay, fov, fakeRaysRange, projection, screenHeight, scale
from src.functions import loadGameImage, resizeImage

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

	@property
	def spriteShot(self):
		return min([object.isOnFire for object in self.objectsList], default = (float('inf'), 0))

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


		if(self.viewAngles):
			self.spriteAngles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
			self.spritePositions = {angle: position for angle, position in zip(self.spriteAngles, self.object)}


	@property
	def isOnFire(self):
		if(centerRay - self.sideCollision // 2 < self.currentRay < centerRay + self.sideCollision // 2 and self.collision):
			return self.distanceToSprite, self.projectionHeight
		return float('inf'), None


	@property
	def position(self):
		return self.x - self.sideCollision // 2, self.y - self.sideCollision // 2

	def locateObject(self, player):
		dx, dy = self.x - player.x, self.y - player.y
		self.distanceToSprite = math.sqrt(dx ** 2 + dy ** 2)

		self.theta = math.atan2(dy, dx)
		gamma = self.theta - player.angle
		if(dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0):
			gamma += (math.pi * 2)

		deltaRays = int(gamma / deltaAngle)
		self.currentRay = centerRay + deltaRays
		self.distanceToSprite *= math.cos((fov // 2) - self.currentRay * deltaAngle)

		fakeRay = self.currentRay + 100
		if(0 <= fakeRay <= fakeRaysRange and self.distanceToSprite > 30):
			self.projectionHeight = min(int(projection / self.distanceToSprite * self.scale), screenHeight * 2)
			height = (self.projectionHeight // 2) * self.height

			if self.viewAngles:
				if self.theta < 0:
					self.theta += (math.pi * 2)
				self.theta = 360 - int(math.degrees(self.theta))

				for angles in self.spriteAngles:
					if(self.theta in angles):
						self.object = self.spritePositions[angles]
						break

			spriteObject = self.object
			if(self.animation and self.distanceToSprite < self.animatinDistance):
				spriteObject = self.animation[0]

				if(self.animationCount < self.animationSpeed):
					self.animationCount += 1

				else:
					self.animation.rotate()
					self.animationCount = 0

			spritePosition = (self.currentRay * scale - (self.projectionHeight // 2), (screenHeight // 2) - ((self.projectionHeight // 2) + height))
			sprite = resizeImage(spriteObject, (self.projectionHeight, self.projectionHeight))
			return (self.distanceToSprite, sprite, spritePosition)
		else:
			return (False,)