# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#													   		#
#			     		   Movement:	    		        #
#			          Developer: Carbon				        #
#													   		#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

import pygame
import numpy

# Movement: #

def handleMovement(posx : int, posy : int, rotate : int, fps : float, wall_set : numpy.ndarray):
	x = posx
	y = posy
	diag = 0
	if(pygame.mouse.get_focused):
		playerMouse = pygame.mouse.get_pos()
		rotate = rotate + numpy.clip((playerMouse[0] - 400) / 200, -0.2, .2)

	if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[ord('z')]:
		x, y, diag = x + fps * numpy.cos(rotate), y + fps * numpy.sin(rotate), 1

	elif pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[ord('s')]:
		x, y, diag = x - fps * numpy.cos(rotate), y - fps * numpy.sin(rotate), 1
        
	if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[ord('q')]:
		fps = fps/(diag + 1)
		x, y = x + fps * numpy.sin(rotate), y - fps * numpy.cos(rotate)
        
	elif pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[ord('d')]:
		fps = fps/(diag + 1)
		x, y = x - fps * numpy.sin(rotate), y + fps * numpy.cos(rotate)

	if not (wall_set[int(x - 0.3)][int(y)] or wall_set[int(x + 0.3)][int(y)] or wall_set[int(x)][int(y - 0.3)] or wall_set[int(x)][int(y + 0.3)]):
		posx, posy = x, y

	elif not (wall_set[int(posx - 0.3)][int(y)] or wall_set[int(posx + 0.3)][int(y)] or wall_set[int(posx)][int(y - 0.3)] or wall_set[int(posx)][int(y + 0.3)]):
		posy = y

	elif not (wall_set[int(x - 0.3)][int(posy)] or wall_set[int(x + 0.3)][int(posy)] or wall_set[int(x)][int(posy - 0.3)] or wall_set[int(x)][int(posy + 0.3)]):
		posx = x

	return posx, posy, rotate