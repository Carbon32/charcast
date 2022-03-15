# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#													   		#
#			     		Raycasting  	    		        #
#			          Developer: Carbon				        #
#													   		#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from config import *
from src.functions import *

# Functions: #

def mapping(x : int, y : int):
	return (x // tile) * tile, (y // tile) * tile

def rayCasting(player, textures, gameMap):
	walls = []
	xo, yo = player.position
	xm, ym = mapping(xo, yo)
	angle = player.angle - (fov / 2)
	
	for ray in range(rays):
		sinA = math.sin(angle)
		cosA = math.cos(angle)

		x, dx = (xm + tile, 1) if cosA >= 0 else (xm, -1)
		for i in range(0, screenWidth, tile):
			depthVertical = (x - xo) / cosA
			yv = yo + depthVertical * sinA
			tileVertical = mapping(x + dx, yv)
			if(tileVertical in gameMap):
				textureVertical = gameMap[tileVertical]
				break
			x += dx * tile

		y, dy = (ym + tile, 1) if sinA >= 0 else (ym, -1)
		for j in range(0, screenHeight, tile):
			depthHorizontal = (y - yo) / sinA
			xh  = xo + depthHorizontal * cosA
			tileHorizontal = mapping(xh, y + dy)
			if( tileHorizontal in gameMap):
				textureHorizontal = gameMap[tileHorizontal]
				break
			y += dy * tile

		depth, offset, texture = (depthVertical, yv, textureVertical)  if depthVertical < depthHorizontal else (depthHorizontal, xh, textureHorizontal)
		offset = int(offset) % tile
		depth *= math.cos(player.angle - angle)
		depth = max(depth, 0.00001)
		projectionHeight = min(int(projection / depth), 2 * screenHeight)
		
		wallColumn = textures[texture].subsurface(offset * textureScale, 0, textureScale, textureHeight)
		wallColumn = resizeImage(wallColumn, (scale, projectionHeight))
		wallPositon = (ray * scale, (screenHeight // 2) - projectionHeight // 2)
		walls.append((depth, wallColumn, wallPositon))
		angle += deltaAngle
	return walls