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
mapSize = 25
wallSet = numpy.random.choice([0, 0, 0, 1], (mapSize, mapSize))
wallRGB = numpy.random.uniform(1, 1, (mapSize, mapSize, 3))

# Game Window: #

gameWindow = pygame.display.set_mode((screenWidth, screenHeight))

# Game Functions: #

def handleMovement(posx, posy, rotate, fps, wallSet):
	x = posx
	y = posy
	diag = 0
	if(pygame.mouse.get_focused):
		playerMouse = pygame.mouse.get_pos()
		rotate = rotate + numpy.clip((playerMouse[0] - 400) / 200, -0.2, .2)

	if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[ord('z')]:
		x, y, diag = x + fps * numpy.cos(rotate), y + fps*numpy.sin(rotate), 1

	elif pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[ord('s')]:
		x, y, diag = x - fps*numpy.cos(rotate), y - fps*numpy.sin(rotate), 1
        
	if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[ord('q')]:
		fps = fps/(diag+1)
		x, y = x + fps*numpy.sin(rotate), y - fps*numpy.cos(rotate)
        
	elif pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[ord('d')]:
		fps = fps/(diag+1)
		x, y = x - fps*numpy.sin(rotate), y + fps*numpy.cos(rotate)

	if not (wallSet[int(x - 0.2)][int(y)] or wallSet[int(x + 0.2)][int(y)] or wallSet[int(x)][int(y - 0.2)] or wallSet[int(x)][int(y + 0.2)]):
		posx, posy = x, y

	elif not (wallSet[int(posx - 0.2)][int(y)] or wallSet[int(posx + 0.2)][int(y)] or wallSet[int(posx)][int(y - 0.2)] or wallSet[int(posx)][int(y + 0.2)]):
		posy = y

	elif not (wallSet[int(x - 0.2)][int(posy)] or wallSet[int(x + 0.2)][int(posy)] or wallSet[int(x)][int(posy - 0.2)] or wallSet[int(x)][int(posy + 0.2)]):
		posx = x

	return posx, posy, rotate

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
		xx = int(x * 3 % 1 * 99)
		
		if(x % 1 < 0.02 or x % 1 > 0.98):
			xx = int(y * 3 % 1 * 99)

		shadows = 0.3 + 0.7 * (wallRes / verticalRes)
		if(shadows > 1):
			shadows = 1
		yy = numpy.linspace(0, 3, wallRes * 2) * 99 % 99
		wallAsh = 0 
		if(wallSet[int(x - 0.33) % (mapSize - 1)][int(y - 0.33) % (mapSize - 1)]):
			wallAsh = 1

		if(wallSet[int(x - 0.01) % (mapSize - 1)][int(y - 0.01) % (mapSize - 1)]):
			shadows, wallAsh = shadows * 0.5, 0

		color = shadows * wallRGB[int(x) % (mapSize - 1)][int(y) % (mapSize - 1)]
		for k in range(wallRes * 2):
			if(verticalRes - wallRes + k >= 0 and verticalRes - wallRes + k < 2 * verticalRes):
				if(wallAsh and 1 - k / (2 * wallRes) < 1 - xx / 99):
					color, wallAsh = 0.5 * color, 0
				frame[i][verticalRes - wallRes + k] = color * wall[xx][int(yy[k])]
				if(verticalRes + 3 * wallRes - k < verticalRes * 2):
					frame[i][verticalRes + 3 * wallRes - k] = (frame[i][verticalRes + 3 * wallRes - k] + color * wall[xx][int(yy[k])]) / 2
		
		for j in range(verticalRes - wallRes):
			n = (verticalRes / (verticalRes - j)) / secCos
			x, y, = posx + cos * n, posy + sin * n
			xx, yy = int(x * 2 % 1 * 99), int(y * 2 % 1 * 99)
			shadows = 0.2 + 0.8 * (1 - j / verticalRes)
			if(wallSet[int(x - 0.33) % (mapSize - 1)][int(y - 0.33) % (mapSize - 1)]):
				shadows = shadows * 0.5
			elif(wallSet[int(x - 0.33) % (mapSize - 1)][int(y - 0.33) % (mapSize - 1)] and y % 1 > x % 1 or wallSet[int(x) % (mapSize - 1)][int(y - 0.33) % (mapSize - 1)] and x % 1 > y % 1):
				shadows = shadows * 0.5
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
	positionX, positionY, rotation = handleMovement(positionX, positionY, rotation, fpsHandler.tick() / 500, wallSet)
	pygame.mouse.set_pos(400, 300)

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
