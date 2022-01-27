# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#													   		#
#			     		   Frame:	    		            #
#			          Developer: Carbon				        #
#													   		#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

import numpy
from numba import njit

# Floor Casting:
horizontalRes = 200
verticalRes = 150
modifier = horizontalRes / 60

# Player:
positionX, positionY, rotation = 0, 0, 0

# Create Frames:
frame = numpy.random.uniform(0, 1, (horizontalRes, verticalRes * 2, 3))

# Map:
mapSize = 25
wallSet = numpy.random.choice([0, 0, 0, 0, 1, 1], (mapSize, mapSize))
wallRGB = numpy.random.uniform(1, 1, (mapSize, mapSize, 3)) # Colors (default: transparent)

@njit()
def updateFrame(posx, posy, rotate, frame, sky, floor, wall):
	for i in range(horizontalRes):
		# Field of View: 
		rotationAngle = rotate + numpy.deg2rad(i / modifier - 30)
		sin, cos, secCos = numpy.sin(rotationAngle), numpy.cos(rotationAngle), numpy.cos(numpy.deg2rad(i / modifier - 30))
		frame[i][:] = sky[int(numpy.rad2deg(rotationAngle) % 359)][:]
		x, y = posx, posy
		

		while wallSet[int(x) % (mapSize - 1)][int(y) % (mapSize - 1)] == 0:
			x, y = x + 0.01 * cos, y + 0.01 * sin
		
		# Modifier: 
		n = abs((x - posx) / cos)

		# Wall Resolution:
		wallRes = int(verticalRes / (n * secCos + 0.001))

		# Update X: 
		xx = int(x * 3 % 1 * 99)

		if(x % 1 < 0.02 or x % 1 > 0.98):
			xx = int(y * 3 % 1 * 99)
		yy = numpy.linspace(0, 3, wallRes * 2) * 99 % 99

		# Shadows & Shaders:
		shadows = 0.3 + 0.7 * (wallRes / verticalRes)
		if(shadows > 1):
			shadows = 1

		wallAsh = 0 
		if(wallSet[int(x - 0.33) % (mapSize - 1)][int(y - 0.33) % (mapSize - 1)]):
			wallAsh = 1

		if(wallSet[int(x - 0.01) % (mapSize - 1)][int(y - 0.01) % (mapSize - 1)]):
			shadows, wallAsh = shadows * 0.3, 0

		# Colors:
		color = shadows * wallRGB[int(x) % (mapSize - 1)][int(y) % (mapSize - 1)]

		# Wall Creation:
		for k in range(wallRes * 2):
			if(verticalRes - wallRes + k >= 0 and verticalRes - wallRes + k < 2 * verticalRes):
				if(wallAsh and 1 - k / (2 * wallRes) < 1 - xx / 99):
					color, wallAsh = 0.3 * color, 0
				frame[i][verticalRes - wallRes + k] = color * wall[xx][int(yy[k])]
				if(verticalRes + 3 * wallRes - k < verticalRes * 2):
					frame[i][verticalRes + 3 * wallRes - k] = (frame[i][verticalRes + 3 * wallRes - k] + color * wall[xx][int(yy[k])]) / 2
		
		# Floor Creation: 
		for j in range(verticalRes - wallRes):
			n = (verticalRes / (verticalRes - j)) / secCos
			x, y, = posx + cos * n, posy + sin * n
			xx, yy = int(x * 2 % 1 * 99), int(y * 2 % 1 * 99)
			shadows = 0.2 + 0.8 * (1 - j / verticalRes)
			if(wallSet[int(x - 0.33) % (mapSize - 1)][int(y - 0.33) % (mapSize - 1)]):
				shadows = shadows * 0.3

			elif(wallSet[int(x - 0.33) % (mapSize - 1)][int(y - 0.33) % (mapSize - 1)] and y % 1 > x % 1 or wallSet[int(x) % (mapSize - 1)][int(y - 0.33) % (mapSize - 1)] and x % 1 > y % 1):
				shadows = shadows * 0.3

			frame[i][verticalRes * 2 - j - 1] = shadows * (floor[xx][yy] + frame[i][verticalRes * 2 - j - 1]) / 2

	# Return frame: 
	return frame