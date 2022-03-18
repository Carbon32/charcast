# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#													   		#
#			     		   Functions:	    		        #
#			          Developer: Carbon				        #
#													   		#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from config import pygame, mapTile, tile, screenWidth

# Functions: #

def drawSky(surface : pygame.Surface, texture : pygame.Surface, offset : int):
	surface.blit(texture, (offset, 0))
	surface.blit(texture, (offset - screenWidth, 0))
	surface.blit(texture, (offset + screenWidth, 0))

def processMap(matrixMap : list, worldMap : dict, miniMap : set, collisionMap : list):
    for j, row in enumerate(matrixMap):
        for i, character in enumerate(row):
            if(character):
                miniMap.add((i * mapTile, j * mapTile))
                collisionMap.append(pygame.Rect(i * tile, j * tile, tile, tile))
                if(character == 1):
                    worldMap[(i * tile, j * tile)] = 1

                elif(character == 2):
                    worldMap[(i * tile, j * tile)] = 2

                elif(character == 3):
                    worldMap[(i * tile, j * tile)] = 3
    return worldMap, miniMap, collisionMap

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