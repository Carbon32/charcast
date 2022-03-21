# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#													   		#
#			     			Sprites	  		  				#
#			          Developer: Carbon				        #
#													   		#
#														    #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Imports: #

from config import pygame, math, njit, tile
from src.map import worldMap
from src.raycasting import mapping
from src.functions import playMusic

# NPC Rendering: #

@njit(fastmath = True, cache = True)
def rayCastingNPC(npcX, npcY, lockedDoors, worldMap, playerPosition):
	xo, yo = playerPosition
	xm, ym = mapping(xo, yo)
	deltaX, deltaY = xo - npcX, yo - npcY
	angle = math.atan2(deltaY, deltaX)
	angle += math.pi
	
	sinA = math.sin(angle)
	cosA = math.cos(angle)
	sinA = sinA if sinA else 0.000001
	cosA = cosA if cosA else 0.000001

	x, dx = (xm + tile, 1) if cosA >= 0 else (xm, -1)
	for i in range(0, int(abs(deltaX)) // tile):
		depthVertical = (x - xo) / cosA
		yv = yo + depthVertical * sinA
		tileVertical = mapping(x + dx, yv)
		if(tileVertical in worldMap or tileVertical in lockedDoors):
			return False
		x += dx * tile

	y, dy = (ym + tile, 1) if sinA >= 0 else (ym, -1)
	for j in range(0, int(abs(deltaY)) // tile):
		depthHorizontal = (y - yo) / sinA
		xh  = xo + depthHorizontal * cosA
		tileHorizontal = mapping(xh, y + dy)
		if(tileHorizontal in worldMap or tileHorizontal in lockedDoors):
			return False
		y += dy * tile
	return True

class Interaction():
	def __init__(self, player, sprites, render):
		self.player = player
		self.sprites = sprites
		self.render = render

	def interactionObject(self):
		if(self.player.shot and self.render.shotgunAnimationTrigger):
			for object in sorted(self.sprites.objectsList, key = lambda object: object.distanceToSprite):
				if(object.isOnFire[1]):
					if(not object.isDead):
						if(rayCastingNPC(object.x, object.y, self.sprites.lockedDoors, worldMap, self.player.position)):
							object.isDead = True
							object.collision = False
							self.render.shotgunAnimationTrigger = False
					if(object.type in {'doorH', 'doorV'} and object.distanceToSprite < tile):
						object.doorOpenTrigger = True
						object.collision = None
					break

	def npcAction(self):
		for object in self.sprites.objectsList:
			if(object.type == 'npc' and not object.isDead):
				if(rayCastingNPC(object.x, object.y, self.sprites.lockedDoors, worldMap, self.player.position)):
					object.npcActionTrigger = True
					self.npcMove(object)
				else:
					object.npcActionTrigger = False


	def npcMove(self, object):
		if(abs(object.distanceToSprite) > tile):
			dx = object.x - self.player.position[0]
			dy = object.y - self.player.position[1]
			object.x = object.x + 1 if dx < 0 else object.x - 1
			object.y = object.y+ 1 if dy < 0 else object.y - 1

	def clearWorld(self):
		deletedObjects = self.sprites.objectsList[:]
		[self.sprites.objectsList.remove(object) for object in deletedObjects if object.delete]

	def playMusic(self):
		playMusic('sounds/music.mp3', 10)