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

# Game Window: #

display = Window(screenWidth, screenHeight, "Raycasting: ")

# Player: #

player = Player()

# Draw Elements: #

render = Render(display.window)

# Game Loop: #

def main():
	while(display.gameRunning):
		display.clearWindow()
		toggleMouseCursorOff()

		render.drawBackground((0, 180, 255), (69, 69, 69))
		render.drawWorld(player.position, player.angle, worldMap)
		render.drawText(str(int(fpsHandler.get_fps())), 40, (255, 0, 0), 10, 30)

		player.handleMovement()

		# Update Display:
		display.updateDisplay(60)

	# Quit: #
	destroyGame()

main()