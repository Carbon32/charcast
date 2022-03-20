# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#													   		#
#			     		Raycasting  	    		        #
#			          Developer: Carbon				        #
#													   		#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from config import math, njit, fov, rays, tile, projection, screenHeight, deltaAngle, textureScale, textureHeight, scale, centerRay
from src.functions import resizeImage
from src.map import worldWidth, worldHeight

# Functions: #

@njit(fastmath = True)
def mapping(x : int, y : int):
	return (x // tile) * tile, (y // tile) * tile


@njit(fastmath = True)
def rayCasting(playerPosition, playerAngle, worldMap):
	castedWalls = []
	xo, yo = playerPosition
	textureVertical, textureHorizontal = 1, 1
	xm, ym = mapping(xo, yo)
	angle = playerAngle - (fov / 2)
	
	for ray in range(rays):
		sinA = math.sin(angle)
		cosA = math.cos(angle)
		sinA = sinA if sinA else 0.000001
		cosA = cosA if cosA else 0.000001

		x, dx = (xm + tile, 1) if cosA >= 0 else (xm, -1)
		for i in range(0, worldWidth, tile):
			depthVertical = (x - xo) / cosA
			yv = yo + depthVertical * sinA
			tileVertical = mapping(x + dx, yv)
			if(tileVertical in worldMap):
				textureVertical = worldMap[tileVertical]
				break
			x += dx * tile

		y, dy = (ym + tile, 1) if sinA >= 0 else (ym, -1)
		for j in range(0, worldHeight, tile):
			depthHorizontal = (y - yo) / sinA
			xh  = xo + depthHorizontal * cosA
			tileHorizontal = mapping(xh, y + dy)
			if(tileHorizontal in worldMap):
				textureHorizontal = worldMap[tileHorizontal]
				break
			y += dy * tile

		depth, offset, texture = (depthVertical, yv, textureVertical)  if depthVertical < depthHorizontal else (depthHorizontal, xh, textureHorizontal)
		offset = int(offset) % tile
		depth *= math.cos(playerAngle - angle)
		depth = max(depth, 0.00001)
		projectionHeight = int(projection / depth)
		
		castedWalls.append((depth, offset, projectionHeight, texture))
		angle += deltaAngle
	return castedWalls

def rayCastingWalls(player, textures, worldMap):
	walls = []
	castedWalls = rayCasting(player.position, player.angle, worldMap)
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