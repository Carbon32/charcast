# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#													   		#
#			     			Sprites	  		  				#
#			          Developer: Carbon				        #
#													   		#
#														    #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Imports: #

from config import math, deque, types, Dict, int32, tile, deltaAngle, centerRay, fov, fakeRaysRange, projection, screenHeight, scale
from src.functions import loadGameImage, resizeImage
from src.raycasting import mapping

# Sprites: #

class Sprite():
	def __init__(self):
		self.spriteParameters = {
			'enemy': {
				'sprite': loadGameImage('sprites/enemy/idle/0.png'),
				'viewAngles': None,
				'height': 0.0,
				'scale': (1.0, 1.0),
				'animation': [],

				'deathAnimation': deque(
					[loadGameImage(f'sprites/enemy/death/{i}.png') for i in range(3)]),
				'isDead': None,
				'animationDistance': 1000,
				'animationSpeed': 10,
				'collision': True,
				'sideCollision': 60,
				'type': 'npc',
				'action': deque(
					[loadGameImage(f'sprites/enemy/blink/{i}.png') for i in range(5)]),

			},

			'doorA1': {
				'sprite': [loadGameImage(f'sprites/door/{i}.png') for i in range(16)],
				'viewAngles': True,
				'height': 0.0,
				'scale': (2.6, 1.2),
				'animation': [],
				'deathAnimation': [],
				'isDead': 'immortal',
				'animationDistance': 0,
				'animationSpeed': 0,
				'collision': True,
				'sideCollision': 60,
				'type': 'doorH',
				'action': [],

			},

			'doorA2': {
				'sprite': [loadGameImage(f'sprites/door/{i}.png') for i in range(16)],
				'viewAngles': True,
				'height': 0.0,
				'scale': (2.6, 1.2),
				'animation': [],
				'deathAnimation': [],
				'isDead': 'immortal',
				'animationDistance': 0,
				'animationSpeed': 0,
				'collision': True,
				'sideCollision': 60,
				'type': 'doorV',
				'action': [],

			},

		}

		self.objectsList = [
            Object(self.spriteParameters['enemy'], (10.0, 10.0)),
            Object(self.spriteParameters['doorA1'], (7, 7)),
            Object(self.spriteParameters['doorA2'], (8, 8)),
		]

	@property
	def spriteShot(self):
		return min([object.isOnFire for object in self.objectsList], default = (float('inf'), 0))

	@property
	def lockedDoors(self):
		blockedDoors = Dict.empty(key_type = types.UniTuple(int32, 2), value_type = int32)
		for object in self.objectsList:
			if(object.type in {'doorH', 'doorV'} and object.collision):
				i, j = mapping(object.x, object.y)
				blockedDoors[(i, j)] = 0
		return blockedDoors

# Objects: #

class Object():
	def __init__(self, parameters, position):
		self.object = parameters['sprite'].copy()
		
		self.viewAngles = parameters['viewAngles']
		self.x, self.y = position[0] * tile, position[1] * tile
		self.height = parameters['height']
		self.scale = parameters['scale']
		
		self.animation = parameters['animation'].copy()
		self.animatinDistance = parameters['animationDistance']
		self.animationSpeed = parameters['animationSpeed']
		self.collision = parameters['collision']

		self.deathAnimation = parameters['deathAnimation'].copy()
		self.isDead = parameters['isDead']

		self.type = parameters['type']
		self.action = parameters['action'].copy()

		self.sideCollision = parameters['sideCollision']
		
		self.animationCount = 0
		self.deathAnimationCount = 0
		self.npcActionTrigger = False

		self.doorOpenTrigger = False
		self.doorPreviousPosition = self.y if self.type == 'doorH' else self.x 
		self.delete = False

		if(self.viewAngles):
			if(len(self.object)):
				self.spriteAngles = [frozenset(range(338, 361)) | frozenset(range(0, 23))] + \
									[frozenset(range(i, i + 45)) for i in range(23, 338, 45)]
			else:
				self.spriteAngles = [frozenset(range(348, 361)) | frozenset(range(0, 11))] + \
									[frozenset(range(i, i + 23)) for i in range(11, 348, 23)]
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
		self.theta -= 1.4 * gamma
		deltaRays = int(gamma / deltaAngle)
		self.currentRay = centerRay + deltaRays
		if(self.type not in {'doorH', 'doorV'}):
			self.distanceToSprite *= math.cos((fov // 2) - self.currentRay * deltaAngle)

		fakeRay = self.currentRay + 100
		if(0 <= fakeRay <= fakeRaysRange and self.distanceToSprite > 30):
			self.projectionHeight = min(int(projection / self.distanceToSprite), screenHeight * 2 if self.type not in {'doorH', 'doorV'} else screenHeight)
			spriteWidth = int(self.projectionHeight * self.scale[0])
			spriteHeight = int(self.projectionHeight * self.scale[1])
			halfWidth = spriteWidth // 2
			halfHeight = spriteHeight // 2
			height = halfHeight * self.height


			if(self.type in {'doorH', 'doorV'}):
				if(self.doorOpenTrigger):
					self.openDoor()
				self.object = self.visibleSprite()
				spriteObject = self.spriteAnimation()
			else:

				if(self.isDead and self.isDead != 'immortal'):
					spriteObject = self.playDeathAnimation()
				elif(self.npcActionTrigger):
					spriteObject = self.npcDoAction()
				else:
					self.object = self.visibleSprite()
					spriteObject = self.spriteAnimation()

			spritePosition = (self.currentRay * scale - halfWidth, (screenHeight // 2) - (halfHeight + height))
			sprite = resizeImage(spriteObject, (spriteWidth, spriteHeight))
			return (self.distanceToSprite, sprite, spritePosition)
		else:
			return (False,)

	def spriteAnimation(self):
		if(self.animation and self.distanceToSprite < self.animatinDistance):
			spriteObject = self.animation[0]

			if(self.animationCount < self.animationSpeed):
				self.animationCount += 1

			else:
				self.animation.rotate()
				self.animationCount = 0
			return spriteObject
		return self.object

	def visibleSprite(self):
		if self.viewAngles:
			if self.theta < 0:
				self.theta += (math.pi * 2)
			self.theta = 360 - int(math.degrees(self.theta))

			for angles in self.spriteAngles:
				if(self.theta in angles):
					return self.spritePositions[angles]

		return self.object

	def playDeathAnimation(self):
		if(len(self.deathAnimation)):
			if(self.deathAnimationCount < self.animationSpeed):
				self.deadSprite = self.deathAnimation[0]
				self.deathAnimationCount += 1
			else:
				self.deadSprite = self.deathAnimation.popleft()
				self.deathAnimationCount = 0
		return self.deadSprite

	def npcDoAction(self):
		spriteObject = self.action[0]
		if(self.animationCount < self.animationSpeed):
			self.animationCount += 1
		else:
			self.action.rotate()
			self.animationCount = 0
		return spriteObject

	def openDoor(self):
		if(self.type == 'doorH'):
			self.y -= 3
			if(abs(self.y - self.doorPreviousPosition) > tile):
				self.delete = True

		elif(self.type == 'doorV'):
			self.x -= 3
			if(abs(self.x - self.doorPreviousPosition) > tile):
				self.delete = True
