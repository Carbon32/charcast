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
	'WWWWWWWWWWWW',
	'W..........W',
	'W.....W....W',
	'W..W.......W',
	'W.......W..W',
	'W..........W',
	'W..W.....W.W',
	'WWWWWWWWWWWW'
]

# Mini-map: #

mMap = pygame.Surface((screenWidth // mapScale, screenHeight // mapScale))

# World Map: #

worldMap = set()
miniMap = set()

for j, row in enumerate(textMap):
	for i, character in enumerate(row):
		if(character == 'W'):
			worldMap.add((i * tile, j * tile)) 
			miniMap.add((i * mapTile, j * mapTile))

