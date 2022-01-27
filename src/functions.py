# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#													   		#
#			     		   Functions:	    		        #
#			          Developer: Carbon				        #
#													   		#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

import pygame
import numpy

# Functions: #

def loadGameImage(path : str):
	image = pygame.image.load(path)
	return image

def setGameIcon(image : pygame.Surface):
	icon = pygame.image.load(image)
	pygame.display.set_icon(icon)

def resizeImage(image : pygame.Surface, size : int):
	scale = pygame.transform.scale(image, (size))
	return scale

def convert3DArray(image : pygame.Surface):
	array = pygame.surfarray.array3d(image)
	return array

def convertToSurface(frame : numpy.ndarray):
	surface = pygame.surfarray.make_surface(frame * 255)
	return surface

def updateWindowTitle(text : str, fps : int):
	pygame.display.set_caption(text + " (" + str(fps) + ")")

def toggleMouseCursorOn():
	pygame.mouse.set_visible(True)

def toggleMouseCursorOff():
	pygame.mouse.set_visible(False)

def resetMousePosition():
	pygame.mouse.set_pos(400, 300)
	
def destroyGame():
	pygame.quit()
	quit()