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
horizontalRes = 200
verticalRes = 150
modifier = horizontalRes / 60
positionX, positionY, rotation = 0, 0, 0

# Create Frames:
frame = numpy.random.uniform(0, 1, (horizontalRes, verticalRes * 2, 3))

# Sky:
sky = pygame.image.load('sky/sky.jpg')
sky = pygame.surfarray.array3d(pygame.transform.scale(sky, (360, verticalRes * 2))) / 255

# Floor: 
floor = pygame.image.load('floor/floor.jpg')
floor = pygame.surfarray.array3d(floor) / 255

# Wall:

wall = pygame.image.load('wall/wall.jpg')
wall = pygame.surfarray.array3d(wall) / 255

# Map:
mapSize = 10
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
		frame[i][:] = sky[int(numpy.rad2deg(rotationAngle) % 359)][:]
		x, y = posx, posy
		
		while wallSet[int(x) % (mapSize - 1)][int(y) % (mapSize - 1)] == 0:
			x, y = x + 0.01 * cos, y + 0.01 * sin
		
		n = abs((x - posx) / cos)
		wallRes = int(verticalRes / (n * secCos + 0.001))
		xx = int(y * 3 % 1 * 99)
		
		if(x % 1 < 0.02 or x % 1 > 0.98):
			xx = int(y * 3 % 1 * 99)

		shadows = 0.3 + 0.7 * (wallRes / verticalRes)
		if(shadows > 1):
			shadows = 1
		yy = numpy.linspace(0, 297, wallRes * 2) % 99
		color = shadows * wallRGB[int(x) % (mapSize - 1)][int(y) % (mapSize - 1)]
		for k in range(wallRes * 2):
			if(verticalRes - wallRes + k >= 0 and verticalRes - wallRes + k < 2 * verticalRes):
				frame[i][verticalRes - wallRes + k] = color * wall[xx][int(yy[k])]
				if(verticalRes + 3 * wallRes - k < verticalRes * 2):
					frame[i][verticalRes - wallRes + k] = color * wall[xx][int(yy[k])]
		for j in range(verticalRes - wallRes):
			n = (verticalRes / (verticalRes - j)) / secCos
			x, y, = posx + cos * n, posy + sin * n
			xx, yy = int(x * 2 % 1 * 99), int(y * 2 % 1 * 99)
			shadows = 0.2 + 0.8 * (1 - j / verticalRes)
			frame[i][verticalRes * 2 - j - 1] = shadows * (floor[xx][yy] + frame[i][verticalRes * 2 - j - 1]) / 2
	return frame

# Game Loop: #

while(gameRunning):
	pygame.display.set_caption("FPS: " + str(fpsHandler.get_fps()))
	pygame.mouse.set_visible(False)
	for event in pygame.event.get():
		if(event.type == pygame.QUIT):
			gameRunning = False

	frame =  newFrame(positionX, positionY, rotation, frame, sky, floor, wallSet, mapSize, wallRGB)
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
