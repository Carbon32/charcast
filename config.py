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

# Textures: #

textureWidth = 1200
textureHeight = 1200
textureScale = textureWidth // tile

# Raycasting: #

fov = math.pi / 3
rays = 300
maxDepth = 800
deltaAngle = fov / rays
distance = rays / (2 * math.tan(fov / 2))
projection = 3 * distance * tile
scale = screenWidth // rays

# Sprites: #

centerRay = rays // 2 - 1
fakeRays = 100
fakeRaysRange = rays - 1 + 2 * fakeRays

# Map & Mini-map: #

miniMapScale = 4
mapScale = 3 * miniMapScale
miniMapResolution = (192, 128)
mapTile = tile // mapScale
