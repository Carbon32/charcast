# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#													   		#
#			     		Raycasting  	    		        #
#			          Developer: Carbon				        #
#													   		#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from config import *

# Functions: #

def mapping(x : int, y : int):
	return (x // tile) * tile, (y // tile) * tile

def rayCasting(display : pygame.Surface, playerPosition : int, playerAngle : int, gameMap):
	xo, yo = playerPosition
	xm, ym = mapping(xo, yo)
	angle = playerAngle - (fov / 2)
	
	for ray in range(rays):
		sinA = math.sin(angle)
		cosA = math.cos(angle)

		x, dx = (xm + tile, 1) if cosA >= 0 else (xm, -1)
		for i in range(0, screenWidth, tile):
			depthVertical = (x - xo) / cosA
			y = yo + depthVertical * sinA
			if(mapping(x + dx, y) in gameMap):
				break
			x += dx * tile

		y, dy = (ym + tile, 1) if sinA >= 0 else (ym, -1)
		for j in range(0, screenHeight, tile):
			depthHorizontal = (y - yo) / sinA
			x  = xo + depthHorizontal * cosA
			if(mapping(x, y + dy) in gameMap):
				break
			y += dy * tile

		depth = depthVertical if depthVertical < depthHorizontal else depthHorizontal
		depth *= math.cos(playerAngle - angle)
		projectionHeight = projection / depth
		c = 255 / (1 + depth * depth * 0.0002)
		color = (c, c // 2, c // 3)
		pygame.draw.rect(display, color, (ray * scale, (screenHeight // 2) - (projectionHeight // 2), scale, projectionHeight))
		angle += deltaAngle
