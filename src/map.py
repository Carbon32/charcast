# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#													   		#
#			     		    Map	    		  		        #
#			          Developer: Carbon				        #
#													   		#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from config import *

# Text Map: #

textMap = [
	'111111111111',
	'2..........3',
	'2..........3',
	'2..........3',
	'2..........3',
	'2..........3',
	'2..........3',
	'111111111111'
]

# Mini-map: #

mMap = pygame.Surface((screenWidth // mapScale, screenHeight // mapScale))

# World Map: #

worldMap = {}
miniMap = set()

for j, row in enumerate(textMap):
	for i, character in enumerate(row):
		if(character != '.'):
			miniMap.add((i * mapTile, j * mapTile))
			if(character == '1'):
				worldMap[(i * tile, j * tile)] = '1'

			if(character == '2'):
				worldMap[(i * tile, j * tile)] = '2'

			if(character == '3'):
				worldMap[(i * tile, j * tile)] = '3'

