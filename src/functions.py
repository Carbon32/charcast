# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#													   		#
#			     		   Functions:	    		        #
#			          Developer: Carbon				        #
#													   		#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from config import *

# Functions: #

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