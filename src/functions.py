# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#													   		#
#			     		   Functions:	    		        #
#			          Developer: Carbon				        #
#													   		#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

import pygame

# Functions: #

def loadGameImage(path):
	image = pygame.image.load(path)
	return image

def setGameIcon(path):
	image = pygame.image.load(path)
	pygame.display.set_icon(image)

def resizeImage(image, size):
	scale = pygame.transform.scale(image, (size))
	return scale


def convert3DArray(image):
	array = pygame.surfarray.array3d(image)
	return array
