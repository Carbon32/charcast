# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#													   		#
#			     		Raycasting  	    		        #
#			          Developer: Carbon				        #
#													   		#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from config import *

# Functions: #

def rayCasting(display : pygame.Surface, playerPosition : int, playerAngle : int, gameMap):
	angle = playerAngle - (fov // 2)
	xo, yo = playerPosition

	for ray in range(rays):
		sinA = math.sin(angle)
		cosA = math.cos(angle)
		for depth in range(maxDepth):
			x = xo + depth * cosA
			y = yo + depth * sinA
			# pygame.draw.line(display, (125, 125, 125), playerPosition, (x, y), 2)
			if(x // tile * tile, y // tile * tile) in gameMap:
				depth *= math.cos(playerAngle - angle)
				projectionHeight = projection / depth
				c = 255 / (1 + depth * depth * 0.0001)
				color = (c // 2, c, c // 3)
				pygame.draw.rect(display, color, (ray * scale, (screenHeight // 2) - (projectionHeight // 2), scale, projectionHeight))
				break

		angle += deltaAngle