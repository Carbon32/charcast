# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#													   		#
#			     	  Raycasting Engine  	    		    #
#			          Developer: Carbon				        #
#													   		#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

try:
	import pygame 
	import math
	import os
	from pygame import mixer
	from collections import deque
	from numba.core import types
	from numba.typed import Dict
	from numba import int32, njit

except ImportError:
	raise ImportError("The Raycasting Engine couldn't import all of the necessary packages.")

# Pygame and Mixer Initializations #:

pygame.init()
mixer.init()

# Engine Variables: #

# Window:

screenWidth = 1200
screenHeight = 800
engineRunning = True
fpsHandler = pygame.time.Clock()

# Player:

playerPosition = ((screenWidth // 2), (screenHeight // 2))
playerAngle = 5
playerSpeed = 2

# Tiles:

tile = 100

# Textures:

textureWidth = 1200
textureHeight = 1200
textureScale = textureWidth // tile

# Raycasting:

fov = math.pi / 3
rays = 300
maxDepth = 800
deltaAngle = fov / rays
distance = rays / (2 * math.tan(fov / 2))
projection = 3 * distance * tile
scale = screenWidth // rays

# Sprites:

centerRay = rays // 2 - 1
fakeRays = 100
fakeRaysRange = rays - 1 + 2 * fakeRays

# Map & Mini-map:

matrixMap = [
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

miniMapScale = 4
mapScale = 3 * miniMapScale
miniMapResolution = (len(matrixMap[0]) * 8, len(matrixMap) * 8)
miniMapCoordinates = set()
mapTile = tile // mapScale
miniMap = pygame.Surface(miniMapResolution)

# World: 

worldWidth = len(matrixMap[0]) * tile
worldHeight = len(matrixMap) * tile
worldMap = Dict.empty(key_type = types.UniTuple(int32, 2), value_type = int32)

# Collision: 

collisionMap = []

# Engine Window: #

window = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Raycasting Engine: ")

# Engine Functions: #

@njit(fastmath = True)
def mapping(x : int, y : int):
	return (x // tile) * tile, (y // tile) * tile

def clearWindow(window : pygame.Surface):
	window.fill((0, 0, 0))

def updateDisplay(fps : int):
	fpsHandler.tick(fps)
	pygame.display.update()

def drawSky(surface : pygame.Surface, texture : pygame.Surface, offset : int):
	surface.blit(texture, (offset, 0))
	surface.blit(texture, (offset - screenWidth, 0))
	surface.blit(texture, (offset + screenWidth, 0))

def processMap(matrixMap : list, worldMap : dict, miniMapCoordinates : set, collisionMap : list):
    for j, row in enumerate(matrixMap):
        for i, character in enumerate(row):
            if(character):
                miniMapCoordinates.add((i * mapTile, j * mapTile))
                collisionMap.append(pygame.Rect(i * tile, j * tile, tile, tile))
                if(character == 1):
                    worldMap[(i * tile, j * tile)] = 1

                elif(character == 2):
                    worldMap[(i * tile, j * tile)] = 2

                elif(character == 3):
                    worldMap[(i * tile, j * tile)] = 3
    return worldMap, miniMapCoordinates, collisionMap

def loadGameImage(path : str):
	image = pygame.image.load(path).convert_alpha()
	return image

def loadAnimation(path : str):
	animation = deque ([loadGameImage(f'{path}{i}.png') for i in range(len(os.listdir(path)))])
	return animation


def loadGameSound(path : str):
	sound = pygame.mixer.Sound(path)
	return sound

def playMusic(path : str, volume : int):
	pygame.mixer.music.load(path)
	pygame.mixer.music.play(volume)

def setGameIcon(image : pygame.Surface):
	icon = pygame.image.load(image)
	pygame.display.set_icon(icon)

def resizeImage(image : pygame.Surface, size : int):
	scale = pygame.transform.scale(image, (size))
	return scale

def toggleMouseCursorOn():
	pygame.mouse.set_visible(True)

def toggleMouseCursorOff():
	pygame.mouse.set_visible(False)

def destroyGame():
	pygame.quit()
	quit()

@njit(fastmath = True)
def rayCasting(playerPosition : tuple, playerAngle : int, worldMap : Dict):
	castedWalls = []
	playerX, playerY = playerPosition
	textureVertical, textureHorizontal = 1, 1
	xMapping, yMapping = mapping(playerX, playerY)
	angle = playerAngle - (fov / 2)
	
	for ray in range(rays):
		sinA = math.sin(angle)
		cosA = math.cos(angle)
		sinA = sinA if sinA else 0.000001
		cosA = cosA if cosA else 0.000001

		x, deltaX = (xMapping + tile, 1) if cosA >= 0 else (xMapping, -1)
		for i in range(0, worldWidth, tile):
			depthVertical = (x - playerX) / cosA
			yVertical = playerY + depthVertical * sinA
			tileVertical = mapping(x + deltaX, yVertical)
			if(tileVertical in worldMap):
				textureVertical = worldMap[tileVertical]
				break
			x += deltaX * tile

		y, deltaY = (yMapping + tile, 1) if sinA >= 0 else (yMapping, -1)
		for j in range(0, worldHeight, tile):
			depthHorizontal = (y - playerY) / sinA
			xHorizontal  = playerX + depthHorizontal * cosA
			tileHorizontal = mapping(xHorizontal, y + deltaY)
			if(tileHorizontal in worldMap):
				textureHorizontal = worldMap[tileHorizontal]
				break
			y += deltaY * tile

		depth, offset, texture = (depthVertical, yVertical, textureVertical)  if depthVertical < depthHorizontal else (depthHorizontal, xHorizontal, textureHorizontal)
		offset = int(offset) % tile
		depth *= math.cos(playerAngle - angle)
		depth = max(depth, 0.00001)
		projectionHeight = int(projection / depth)
		
		castedWalls.append((depth, offset, projectionHeight, texture))
		angle += deltaAngle

	return castedWalls

def rayCastingWalls(playerPosition : tuple, playerAngle : int, textures : dict, worldMap : Dict):
	walls = []
	castedWalls = rayCasting(playerPosition, playerAngle, worldMap)
	wallShot = castedWalls[centerRay][0], castedWalls[centerRay][2]

	for ray, castedValues in enumerate(castedWalls):
		depth, offset, projectionHeight, texture = castedValues

		if(projectionHeight > screenHeight):
			coefficient = projectionHeight / screenHeight
			newTextureHeight = textureHeight / coefficient
			halfTextureHeight = textureHeight // 2
			wallColumn = textures[texture].subsurface(offset * textureScale, halfTextureHeight - newTextureHeight // 2, textureScale, newTextureHeight)
			wallColumn = resizeImage(wallColumn, (scale, screenHeight))
			wallPosition = (ray * scale, 0)

		else:

			wallColumn = textures[texture].subsurface(offset * textureScale, 0, textureScale, textureHeight)
			wallColumn = resizeImage(wallColumn, (scale, projectionHeight))
			wallPosition = (ray * scale, (screenHeight // 2) - projectionHeight // 2)

		walls.append((depth, wallColumn, wallPosition))

	return walls, wallShot

@njit(fastmath = True, cache = True)
def rayCastingNPC(npcX : int, npcY : int, worldMap : Dict, playerPosition : tuple):
	playerX, playerY = playerPosition
	xMapping, yMapping = mapping(playerX, playerY)
	deltaX, deltaY = playerX - npcX, playerY - npcY
	angle = math.atan2(deltaY, deltaX)
	angle += math.pi
	
	sinA = math.sin(angle)
	cosA = math.cos(angle)
	sinA = sinA if sinA else 0.000001
	cosA = cosA if cosA else 0.000001

	x, deltaX = (xMapping + tile, 1) if cosA >= 0 else (xMapping, -1)
	for i in range(0, int(abs(deltaX)) // tile):
		depthVertical = (x - playerX) / cosA
		yVertical = playerY + depthVertical * sinA
		tileVertical = mapping(x + deltaX, yVertical)
		if(tileVertical in worldMap):
			return False
		x += deltaX * tile

	y, deltaY = (yMapping + tile, 1) if sinA >= 0 else (yMapping, -1)
	for j in range(0, int(abs(deltaY)) // tile):
		depthHorizontal = (y - playerY) / sinA
		xHorizontal  = playerX + depthHorizontal * cosA
		tileHorizontal = mapping(xHorizontal, y + deltaY)
		if(tileHorizontal in worldMap):
			return False
		y += deltaY * tile

	return True

# Map Creation: #

worldMap, miniMapCoordinates, collisionMap = processMap(matrixMap, worldMap, miniMapCoordinates, collisionMap)

# Rendering: #

class Render():
	def __init__(self, display : pygame.Surface, minimap : pygame.Surface, player):
		self.display = display
		self.miniMap = miniMap
		self.player = player
		self.textures = {1: loadGameImage('textures/wall.jpg'),
						 2: loadGameImage('textures/wall2.jpg'),
						 3: loadGameImage('textures/wall3.jpg'),
						 9: loadGameImage('textures/sky.jpg'),
		}

		self.shotgunModel = loadGameImage('sprites/weapon/shotgun/idle/0.png')
		self.shotgunAnimation = deque([loadGameImage(f'sprites/weapon/shotgun/shooting/{i}.png') for i in range(len(os.listdir(f'sprites/weapon/shotgun/shooting')))])

		self.shotgunRect = self.shotgunModel.get_rect()
		self.shotgunPosition = ((screenWidth // 2) - self.shotgunRect.width // 2, screenHeight - self.shotgunRect.height)

		self.shotgunAnimationLength = len(self.shotgunAnimation)
		self.shotgunAnimationLengthCount = 0 

		self.shotgunAnimationCount = 0
		self.shotgunAnimationSpeed = 3
		self.shotgunAnimationTrigger = True

		self.shotgunSound = loadGameSound('sounds/shoot.mp3')

		self.sfx = deque([loadGameImage(f'sprites/weapon/shotgun/sfx/{i}.png') for i in range(len(os.listdir(f'sprites/weapon/shotgun/sfx')))])
		self.sfxLengthCount = 0
		self.sfxLength = len(self.sfx)

	def drawBackground(self, playerAngle : int):
		skyOffset = -10 * math.degrees(playerAngle) % screenWidth
		drawSky(self.display, self.textures[9], skyOffset)
	
	def drawFloor(self, floor : tuple):
		pygame.draw.rect(self.display, floor, (0, screenHeight // 2, screenWidth, screenHeight // 2))

	def drawWorld(self, worldObjects):
		for obj in sorted(worldObjects, key = lambda n : n[0], reverse = True):

			if(obj[0]):
				_, object, objectPosition = obj
				self.display.blit(object, objectPosition)

	def drawText(self, text : str, size : int, color : tuple, x : int, y : int):
		image = pygame.font.SysFont('System', size, bold = True).render(text, True, color)
		self.display.blit(image, (x, y))

	def drawMiniMap(self, player, sprites):
		self.miniMap.fill((0, 0, 0))
		mapX, mapY = player.x // mapScale, player.y // mapScale
		pygame.draw.circle(self.miniMap, (14, 217, 34), (int(mapX), int(mapY)), 2)
		for object in sprites.objectsList:
			if(object.type == 'npc' and not object.isDead):
				npcX, npcY = object.x // mapScale, object.y // mapScale
				pygame.draw.circle(self.miniMap, (217, 18, 34), (int(npcX), int(npcY)), 2)

			if(object.type == 'decoration' and not object.isDead):
				objectX, objectY = object.x // mapScale, object.y // mapScale
				pygame.draw.rect(self.miniMap, (14, 120, 217), (int(objectX), int(objectY), 4, 4))


		for x, y in miniMapCoordinates:
			pygame.draw.rect(self.miniMap, (0, 150, 150), (x, y, mapTile, mapTile))
		self.display.blit(self.miniMap, (0, 0))

	def drawPlayerWeapon(self, shots : list):
		if(self.player.shot):

			if(not self.shotgunAnimationLengthCount):

				self.shotgunSound.play()

			self.shotgunProjection = min(shots)[1] // 2
			self.bulletSFX()
			shotgunSprite = self.shotgunAnimation[0]
			self.display.blit(shotgunSprite, self.shotgunPosition)
			self.shotgunAnimationCount += 1

			if(self.shotgunAnimationCount == self.shotgunAnimationSpeed):

				self.shotgunAnimation.rotate(-1)
				self.shotgunAnimationCount = 0
				self.shotgunAnimationLengthCount += 1
				self.shotgunAnimationTrigger = False

			if(self.shotgunAnimationLengthCount == self.shotgunAnimationLength):

				self.player.shot = False
				self.shotgunAnimationLengthCount = 0
				self.sfxLengthCount = 0
				self.shotgunAnimationTrigger = True
		else:

			self.display.blit(self.shotgunModel, self.shotgunPosition)

	def bulletSFX(self):
		if(self.sfxLengthCount < self.sfxLength):

			sfx = resizeImage(self.sfx[0], (self.shotgunProjection, self.shotgunProjection))
			sfxRect = sfx.get_rect()
			self.display.blit(sfx, ((screenWidth // 2) - sfxRect.w // 2, (screenHeight // 2) - sfxRect.h // 2))
			self.sfxLengthCount += 1
			self.sfx.rotate(-1)

# Sprite Handling: #

class Sprite():
	def __init__(self):
		self.spriteParameters = {

			'barrel': 
			{
				'sprite': loadGameImage('sprites/barrel/model/0.png'),
				'viewAngles': False,
				'height': -0.5,
				'scale': (1.2, 0.8),
				'animation': [],
				'deathAnimation': loadAnimation('sprites/barrel/destroyed/'),
				'isDead': None,
				'animationDistance': 0,
				'animationSpeed': 0,
				'collision': True,
				'sideCollision': 40,
				'type': 'decoration',
				'action': [],

			},

			'troll': 
			{
				'sprite': loadAnimation('sprites/troll/angles/'),
				'viewAngles': True,
				'height': 0.0,
				'scale': (2.1, 1.7),
				'animation': [],
				'deathAnimation': loadAnimation('sprites/troll/death/'),
				'isDead': None,
				'animationDistance': 0,
				'animationSpeed': 1,
				'collision': True,
				'sideCollision': 60,
				'type': 'decoration',
				'action': [],

			},

			'monster': 
			{
				'sprite': loadGameImage('sprites/monster/model/0.png'),
				'viewAngles': False,
				'height': 0.0,
				'scale': (3.5, 2.5),
				'animation': [],
				'deathAnimation': loadAnimation('sprites/monster/death/'),
				'isDead': None,
				'animationDistance': 0,
				'animationSpeed': 3,
				'collision': True,
				'sideCollision': 60,
				'type': 'npc',
				'action': loadAnimation('sprites/monster/model/'),

			},

			'ufo': 
			{
				'sprite': loadGameImage('sprites/ufo/model/0.png'),
				'viewAngles': False,
				'height': 0.0,
				'scale': (1.4, 1.1),
				'animation': [],
				'deathAnimation': loadAnimation('sprites/ufo/death/'),
				'isDead': None,
				'animationDistance': 0,
				'animationSpeed': 3,
				'collision': True,
				'sideCollision': 60,
				'type': 'npc',
				'action': loadAnimation('sprites/ufo/model/'),

			},

		}

		self.objectsList = [
            Object(self.spriteParameters['barrel'], (2.15, 2.75)),
            Object(self.spriteParameters['barrel'], (2.15, 2.25)),
            Object(self.spriteParameters['barrel'], (2.15, 3.10)),
            Object(self.spriteParameters['troll'], (14.8, 2.40)),
            Object(self.spriteParameters['ufo'], (14.8, 2.40)),
            Object(self.spriteParameters['ufo'], (17.30, 3.49)),
            Object(self.spriteParameters['monster'], (16.99, 1.41)),

		]

	@property
	def spriteShot(self):
		return min([object.isShot for object in self.objectsList], default = (float('inf'), 0))

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

		if(self.viewAngles):
			if(len(self.object)):

				self.spriteAngles = [frozenset(range(338, 361)) | frozenset(range(0, 23))] + [frozenset(range(i, i + 45)) for i in range(23, 338, 45)]
			else:

				self.spriteAngles = [frozenset(range(348, 361)) | frozenset(range(0, 11))] + [frozenset(range(i, i + 23)) for i in range(11, 348, 23)]
			self.spritePositions = {angle: position for angle, position in zip(self.spriteAngles, self.object)}


	@property
	def isShot(self):

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
		fakeRay = self.currentRay + 100

		if(0 <= fakeRay <= fakeRaysRange and self.distanceToSprite > 30):

			self.projectionHeight = min(int(projection / self.distanceToSprite), screenHeight * 2)
			spriteWidth = int(self.projectionHeight * self.scale[0])
			spriteHeight = int(self.projectionHeight * self.scale[1])
			halfWidth = spriteWidth // 2
			halfHeight = spriteHeight // 2
			height = halfHeight * self.height

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

# Player: #

class Player():
	def __init__(self, sprites):
		self.x, self.y = playerPosition
		self.sprites = sprites
		self.angle = playerAngle
		self.speed = playerSpeed
		self.sprinting = False
		self.sensitvity = 0.004
		self.sideCollision = 50
		self.rect = pygame.Rect(*playerPosition, self.sideCollision, self.sideCollision)
		self.shot = False

	@property
	def position(self):
		return (self.x, self.y)

	@property
	def collisionList(self):
		return collisionMap + [pygame.Rect(*object.position, object.sideCollision, object.sideCollision) for object in self.sprites.objectsList if object.collision]

	def detectCollision(self, dx : int, dy : int):
		nextRect = self.rect.copy()
		nextRect.move_ip(dx, dy)
		hitIndexes = nextRect.collidelistall(self.collisionList)

		if(len(hitIndexes)):

			deltaX, deltaY = 0, 0

			for index in hitIndexes:

				hitRect = self.collisionList[index]

				if(dx > 0):

					deltaX += nextRect.right - nextRect.left

				else:

					deltaX += hitRect.right - hitRect.left

				if(dy > 0):

					deltaY += nextRect.bottom - hitRect.top

				else:

					deltaY += hitRect.bottom - nextRect.top

			if(abs(deltaX - deltaY) < 10):

				dx, dy = 0, 0

			elif(deltaX > deltaY):

				dy = 0

			elif(deltaY > deltaX):

				dx = 0

		self.x += dx
		self.y += dy

	def handleControl(self):
		self.handleMovement()
		self.handleMouse()
		self.rect.center = self.x, self.y
		self.angle %= (2 * math.pi)

	def handleMovement(self):
		sinA = math.sin(self.angle)
		cosA = math.cos(self.angle)

		if(self.sprinting):

			self.speed = playerSpeed * 2

		else:

			self.speed = playerSpeed
			
		if(pygame.key.get_pressed()[pygame.K_z]):

			dx = self.speed * cosA
			dy = self.speed * sinA
			self.detectCollision(dx, dy)

		if(pygame.key.get_pressed()[pygame.K_s]):

			dx = -self.speed * cosA
			dy = -self.speed * sinA
			self.detectCollision(dx, dy)

		if(pygame.key.get_pressed()[pygame.K_q]):

			dx = self.speed * sinA
			dy = -self.speed * cosA
			self.detectCollision(dx, dy)

		if(pygame.key.get_pressed()[pygame.K_d]):

			dx = -self.speed * sinA
			dy = self.speed * cosA
			self.detectCollision(dx, dy)

		if(pygame.key.get_pressed()[pygame.K_LSHIFT]):

			self.sprinting = True

		else:

			self.sprinting = False

		for event in pygame.event.get():

			if(event.type == pygame.QUIT):

				exit()
				
			if(event.type == pygame.MOUSEBUTTONDOWN):

				if(event.button == True and not self.shot):

					self.shot = True

	def handleMouse(self):
		if(pygame.mouse.get_focused()):

			difference = pygame.mouse.get_pos()[0] - (screenWidth // 2)
			pygame.mouse.set_pos((screenWidth // 2, screenHeight // 2))
			self.angle += difference * self.sensitvity

# Game Interaction: #

class Interaction():
	def __init__(self, player, sprites, render):
		self.player = player
		self.sprites = sprites
		self.render = render

	def interactionObject(self):
		if(self.player.shot and self.render.shotgunAnimationTrigger):

			for object in sorted(self.sprites.objectsList, key = lambda object: object.distanceToSprite):

				if(object.isShot[1]):

					if(not object.isDead):

						if(rayCastingNPC(object.x, object.y, worldMap, self.player.position)):

							object.isDead = True
							object.collision = False
							self.render.shotgunAnimationTrigger = False

					break

	def npcAction(self):
		for object in self.sprites.objectsList:

			if(object.type == 'npc' and not object.isDead):

				if(rayCastingNPC(object.x, object.y, worldMap, self.player.position)):

					object.npcActionTrigger = True
					self.npcMove(object)

				else:

					object.npcActionTrigger = False


	def npcMove(self, object):
		if(abs(object.distanceToSprite) > tile):

			dx = object.x - self.player.position[0]
			dy = object.y - self.player.position[1]
			object.x = object.x + 1 if dx < 0 else object.x - 1
			object.y = object.y + 1 if dy < 0 else object.y - 1

	def clearWorld(self):
		deletedObjects = self.sprites.objectsList[:]
		[self.sprites.objectsList.remove(object) for object in deletedObjects if object.delete]

	def playMusic(self):
		playMusic('sounds/music.mp3', 10)


class Walls():
	def __init__(self):
		self.walls = []
		self.wallShot = ()

	def updateWalls(self, playerPosition : tuple, playerAngle : int, textures : dict, worldMap : Dict):
		self.walls, self.wallShot = rayCastingWalls(playerPosition, playerAngle, textures, worldMap)

	def wallStatus(self):
		return self.walls

	def shotWalls(self):
		return self.wallShot

class Game():
	def __init__(self):
		self.engineRunning = True

	def gameStatus(self):
		if(pygame.key.get_pressed()[pygame.K_ESCAPE]):
			self.engineRunning = False
