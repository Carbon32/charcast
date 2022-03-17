# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#													   		#
#			     		   Player   	    		        #
#			          Developer: Carbon				        #
#													   		#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from config import *

# Player: #

class Player():
	def __init__(self):
		self.x, self.y = playerPosition
		self.angle = playerAngle
		self.speed = playerSpeed
		self.sprinting = False
		self.sensitvity = 0.004

	@property
	def position(self):
		return (self.x, self.y)

	def handleControl(self):
		self.handleMovement()
		self.handleMouse()


	def handleMovement(self):
		sinA = math.sin(self.angle)
		cosA = math.cos(self.angle)

		if(self.sprinting):
			self.speed = playerSpeed * 2
		else:
			self.speed = playerSpeed
			
		if(pygame.key.get_pressed()[pygame.K_z]):
			self.x += self.speed * cosA
			self.y += self.speed * sinA

		if(pygame.key.get_pressed()[pygame.K_s]):
			self.x += -self.speed * cosA
			self.y += -self.speed * sinA

		if(pygame.key.get_pressed()[pygame.K_q]):
			self.x += self.speed * sinA
			self.y += -self.speed * cosA

		if(pygame.key.get_pressed()[pygame.K_d]):
			self.x += -self.speed * sinA
			self.y += self.speed * cosA

		if(pygame.key.get_pressed()[pygame.K_LSHIFT]):
			self.sprinting = True
		else:
			self.sprinting = False

		self.angle %= (2 * math.pi)

	def handleMouse(self):
		if(pygame.mouse.get_focused()):
			difference = pygame.mouse.get_pos()[0] - (screenWidth // 2)
			pygame.mouse.set_pos((screenWidth // 2, screenHeight // 2))
			self.angle += difference * self.sensitvity
