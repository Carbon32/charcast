# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#													   		#
#			          Python Raycasting 					#
#			          Developer: Carbon				        #
#													   		#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Imports: #

import pygame
import numpy 

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
sky = pygame.transform.scale(sky, (360, 100))
sky = pygame.surfarray.array3d(pygame.transform.scale(sky, (360, verticalRes * 2)))

# Game Window: #

gameWindow = pygame.display.set_mode((screenWidth, screenHeight))

# Game Functions: #

def handleMovement(x, y, rotation):
	if(pygame.key.get_pressed()[ord('q')]):
		rotation = rotation - 0.1

	if(pygame.key.get_pressed()[ord('d')]):
		rotation = rotation + 0.1

	if(pygame.key.get_pressed()[ord('z')]):
		x, y = x + numpy.cos(rotation) * 0.1, y + numpy.sin(rotation) * 0.1

	if(pygame.key.get_pressed()[ord('s')]):
		x, y = x - numpy.cos(rotation) * 0.1, y - numpy.sin(rotation) * 0.1

	return x, y, rotation
# Game Loop: #

while(gameRunning):
	for event in pygame.event.get():
		if(event.type == pygame.QUIT):
			gameRunning = False

	for i in range(horizontalRes):
		rotationAngle = rotation + numpy.deg2rad(i / modifier - 30)
		sin, cos, secCos = numpy.sin(rotationAngle), numpy.cos(rotationAngle), numpy.cos(numpy.deg2rad(i / modifier - 30))
		frame[i][:] = sky[int(numpy.rad2deg(rotationAngle) % 360)][:] / 255
		for j in range(verticalRes):
			n = (verticalRes / (verticalRes - j)) / secCos
			x, y, = positionX + cos * n, positionY + sin * n

			if(int(x) % 2 == int(y) % 2):
				frame[i][verticalRes * 2 - j - 1] = [0, 0, 0]
			else:
				frame[i][verticalRes * 2 - j - 1] = [1, 1, 1]

	# Movement: #
	positionX, positionY, rotation = handleMovement(positionX, positionY, rotation)

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