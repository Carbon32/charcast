# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#													   		#
#			     		   Player   	    		        #
#			          Developer: Carbon				        #
#													   		#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from config import *
from src.map import *

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
		self.spritesCollision = [pygame.Rect(*object.position, object.sideCollision, object.sideCollision) for object in self.sprites.objectsList if object.collision]
		self.collisionList = collisionMap + self.spritesCollision

	@property
	def position(self):
		return (self.x, self.y)

	def detectCollision(self, dx, dy):
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

	def handleMouse(self):
		if(pygame.mouse.get_focused()):
			difference = pygame.mouse.get_pos()[0] - (screenWidth // 2)
			pygame.mouse.set_pos((screenWidth // 2, screenHeight // 2))
			self.angle += difference * self.sensitvity
