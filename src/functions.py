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

def updateWindowTitle(text : str, fps : int):
	pygame.display.set_caption(text + " [" + str(fps) + "]")

def toggleMouseCursorOn():
	pygame.mouse.set_visible(True)

def toggleMouseCursorOff():
	pygame.mouse.set_visible(False)

def drawText(surface : pygame.Surface, text : str, color : tuple, x : int, y : int):
	image = pygame.font.SysFont('System', 30).render(text, True, color)
	surface.blit(image, (x, y))

def destroyGame():
	pygame.quit()
	quit()