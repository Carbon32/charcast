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


# Game Window: #

display = Window(screenWidth, screenHeight)
setGameIcon('wall/wall.png')

# Player: #

player = Player()

# Game Loop: #

def main():
	while(display.gameRunning):
		updateWindowTitle("Raycasting: ", fpsHandler.get_fps())
		display.clearWindow()
		toggleMouseCursorOff()

		pygame.draw.rect(display.window, (0, 0, 255), (0, 0, screenWidth, screenHeight // 2))
		pygame.draw.rect(display.window, (120, 120, 0), (0, screenHeight // 2, screenWidth, screenHeight // 2))

		rayCasting(display.window, player.position, player.angle, worldMap)
		player.handleMovement()
		'''pygame.draw.circle(display.window, (255, 0, 0), (int(player.x), int(player.y)), 12)
		pygame.draw.line(display.window, (255, 0, 0), player.position,   (player.x + screenWidth * math.cos(player.angle), player.y + screenWidth * math.sin(player.angle)))
		
		for x, y in worldMap:
			pygame.draw.rect(display.window, (125, 125, 125), (x, y, tile, tile), 2)

'''

		# Update Display:
		display.updateDisplay(60)

	# Quit: #
	destroyGame()

main()