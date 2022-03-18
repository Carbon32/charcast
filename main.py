# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#													   		#
#			     Python Raycasting (Remake)	  		  		#
#			          Developer: Carbon				        #
#													   		#
#														    #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Imports: #

from config import *
from src.window import *
from src.functions import *
from src.player import *
from src.map import *
from src.raycasting import *
from src.render import *
from src.sprites import *

# Game Window: #

display = Window(screenWidth, screenHeight, "Raycasting: ")

# Sprites: #

sprites = Sprite()

# Player: #

player = Player(sprites)

# Draw Elements: #

render = Render(display.window, miniMap)

# Game Loop: #

def main():
	while(display.gameRunning):
		display.clearWindow()
		toggleMouseCursorOff()

		render.drawBackground((0, 180, 255), (69, 69, 69), player.angle)
		render.drawWorld(rayCastingWalls(player, render.textures) + [object.locateObject(player) for object in sprites.objectsList])
		render.drawText(str(int(fpsHandler.get_fps())), 40, (255, 0, 0), 1150, 30)
		render.drawMiniMap(player)
		player.handleControl()

		# Update Display:
		display.updateDisplay(120)

	# Quit: #
	destroyGame()

main()