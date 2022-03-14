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

	@property
	def position(self):
		return (self.x, self.y)

	def handleMovement(self):
		sinA = math.sin(self.angle)
		cosA = math.cos(self.angle)
		if(pygame.key.get_pressed()[pygame.K_z]):
			self.x += playerSpeed * cosA
			self.y += playerSpeed * sinA

		if(pygame.key.get_pressed()[pygame.K_s]):
			self.x += -playerSpeed * cosA
			self.y += -playerSpeed * sinA

		if(pygame.key.get_pressed()[pygame.K_q]):
			self.x += playerSpeed * sinA
			self.y += -playerSpeed * cosA

		if(pygame.key.get_pressed()[pygame.K_d]):
			self.x += -playerSpeed * sinA
			self.y += playerSpeed * cosA

		if(pygame.key.get_pressed()[pygame.K_LEFT]):
			self.angle -= 0.02

		if(pygame.key.get_pressed()[pygame.K_RIGHT]):
			self.angle += 0.02
