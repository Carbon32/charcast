# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#													   		#
#			     		   Config    	    		        #
#			          Developer: Carbon				        #
#													   		#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

import pygame ; import math

# Window Variables: #

screenWidth = 1200 ; screenHeight = 800 ; gameRunning = True ; fpsHandler = pygame.time.Clock()

# Player Variables: #

playerPosition = (screenWidth // 2, screenHeight // 2)
playerAngle = 0
playerSpeed = 2

# World: #

tile = 100

# Raycasting: #

fov = math.pi / 3
rays = 120
maxDepth = 800
deltaAngle = fov / rays
distance = rays / (2 * math.tan(fov / 2))
projection = 3 * distance * tile
scale = screenWidth // rays
