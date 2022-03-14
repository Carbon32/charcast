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
	'W...W......W',
	'W.....W....W',
	'W..W.......W',
	'W.......W..W',
	'W..........W',
	'W..W.....W.W',
	'WWWWWWWWWWWW'
]

# World Map: #

worldMap = set()
for j, row in enumerate(textMap):
	for i, character in enumerate(row):
		if(character == 'W'):
			worldMap.add((i * tile, j * tile)) 

