# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#													   		#
#			     		   Functions:	    		        #
#			          Developer: Carbon				        #
#													   		#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from config import *

# Functions: #

def drawSky(surface : pygame.Surface, texture : pygame.Surface, offset : int):
	surface.blit(texture, (offset, 0))
	surface.blit(texture, (offset - screenWidth, 0))
	surface.blit(texture, (offset + screenWidth, 0))

def mapping(x : int, y : int):
	return (x // tile) * tile, (y // tile) * tile

def processMap(matrixMap : list, worldMap : dict, miniMap : set):
    for j, row in enumerate(matrixMap):
        for i, character in enumerate(row):
            if(character):
                miniMap.add((i * mapTile, j * mapTile))
                if(character == 1):
                    worldMap[(i * tile, j * tile)] = 1

                elif(character == 2):
                    worldMap[(i * tile, j * tile)] = 2

                elif(character == 3):
                    worldMap[(i * tile, j * tile)] = 3
    return worldMap, miniMap

def loadGameImage(path : str):
	image = pygame.image.load(path).convert_alpha()
	return image

def setGameIcon(image : pygame.Surface):
	icon = pygame.image.load(image)
	pygame.display.set_icon(icon)

def resizeImage(image : pygame.Surface, size : int):
	scale = pygame.transform.scale(image, (size))
	return scale

def toggleMouseCursorOn():
	pygame.mouse.set_visible(True)

def toggleMouseCursorOff():
	pygame.mouse.set_visible(False)

def destroyGame():
	pygame.quit()
	quit()