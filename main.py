# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#													   		#
#			          Python Raycasting 					#
#			          Developer: Carbon				        #
#													   		#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Imports: #

import pygame
import numpy 
from numba import njit

# Pygame Initialization: #

pygame.init()

# Game Variables: #

# Window:
screenWidth = 800
screenHeight = 600
gameRunning = True
fpsHandler = pygame.time.Clock()

# Floor Casting:
horizontalRes = 120
verticalRes = 100 
modifier = horizontalRes / 60
positionX, positionY, rotation = 0, 0, 0

# Create Frames:
frame = numpy.random.uniform(0, 1, (horizontalRes, verticalRes * 2, 3))

# Sky:
sky = pygame.image.load('sky/sky.jpg')
sky = pygame.surfarray.array3d(pygame.transform.scale(sky, (360, verticalRes * 2)))

# Floor: 
floor = pygame.image.load('floor/floor.jpg')
floor = pygame.surfarray.array3d(floor)

# Wall:

wall = pygame.image.load('wall/wall.jpg')
wall = pygame.surfarray.array3d(wall)

# Map:
mapSize = 5
wallSet = numpy.random.choice([0, 0, 0, 1], (mapSize, mapSize))
wallRGB = numpy.random.uniform(0, 1, (mapSize, mapSize, 3))

# Game Window: #

gameWindow = pygame.display.set_mode((screenWidth, screenHeight))

# Game Functions: #

def handleMovement(x, y, rotate, fps):
	if(pygame.key.get_pressed()[ord('q')]):
		rotate = rotation - 0.001 * fps

	if(pygame.key.get_pressed()[ord('d')]):
		rotate = rotation + 0.001 * fps

	if(pygame.key.get_pressed()[ord('z')]):
		x, y = x + numpy.cos(rotation) * 0.005  * fps, y + numpy.sin(rotate) * 0.005 * fps

	if(pygame.key.get_pressed()[ord('s')]):
		x, y = x - numpy.cos(rotate) * 0.005 * fps, y - numpy.sin(rotate) * 0.005 * fps

	return x, y, rotate

@njit()
def newFrame(posx, posy, rotate, frame, sky, floor, wallSet, mapSize, wallRGB):
	for i in range(horizontalRes):
		rotationAngle = rotate + numpy.deg2rad(i / modifier - 30)
		sin, cos, secCos = numpy.sin(rotationAngle), numpy.cos(rotationAngle), numpy.cos(numpy.deg2rad(i / modifier - 30))
		frame[i][:] = sky[int(numpy.rad2deg(rotationAngle) % 359)][:] / 255
		for j in range(verticalRes):
			n = (verticalRes / (verticalRes - j)) / secCos
			x, y, = posx + cos * n, posy + sin * n
			xx, yy = int(x * 2 % 1 * 100), int(y * 2 % 1 * 100)
			shadows = 0.2 + 0.8 * (1 - j / verticalRes)
			if(wallSet[int(x) % (mapSize - 1)][int(y) % (mapSize - 1)]):
				wallRes = verticalRes - j
				if(x % 1 < 0.02 or x % 1 > 0.98):
					xx = yy
				yy = numpy.linspace(0, 198, wallRes * 2) % 99
				color = shadows * wallRGB[int(x) % (mapSize - 1)][int(y) % (mapSize - 1)]
				for k in range(wallRes * 2):
					frame[i][verticalRes - wallRes + k] = color * wall[xx][int(yy[k])] / 255
				break
			else:
				frame[i][verticalRes * 2 - j - 1] = shadows * floor[xx][yy] / 255

	return frame 

# Game Loop: #

while(gameRunning):
	pygame.display.set_caption("FPS: " + str(fpsHandler.get_fps()))
	for event in pygame.event.get():
		if(event.type == pygame.QUIT):
			gameRunning = False

	frame = newFrame(positionX, positionY, rotation, frame, sky, floor, wallSet, mapSize, wallRGB)
	# Movement: #
	positionX, positionY, rotation = handleMovement(positionX, positionY, rotation, fpsHandler.tick())

	# Convert & Scale Frames:
	surface = pygame.surfarray.make_surface(frame * 255)
	surface = pygame.transform.scale(surface, (800, 600))

	# Display Frames:
	gameWindow.blit(surface, (0, 0))

	# Update Display:
	pygame.display.update()

# Quit: #
pygame.quit()
quit()
