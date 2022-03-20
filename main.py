# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#													   		#
#			     Python Raycasting (Remake)	  		  		#
#			          Developer: Carbon				        #
#													   		#
#														    #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Imports: #

from config import screenWidth, screenHeight, fpsHandler
from src.window import Window
from src.functions import toggleMouseCursorOff, destroyGame
from src.player import Player
from src.map import miniMap, worldMap
from src.raycasting import rayCastingWalls
from src.render import Render
from src.sprites import Sprite

# Game Window: #

display = Window(screenWidth, screenHeight, "Raycasting: ")

# Sprites: #

sprites = Sprite()

# Player: #

player = Player(sprites)

# Draw Elements: #

render = Render(display.window, miniMap, player)

# Game Loop: #

def main():
	while(display.gameRunning):
		display.clearWindow()
		toggleMouseCursorOff()

		# Rendering: 

		render.drawBackground((0, 180, 255), (69, 69, 69), player.angle)
		walls, wallShot = rayCastingWalls(player, render.textures, worldMap)
		render.drawWorld(walls + [object.locateObject(player) for object in sprites.objectsList])
		render.drawText(str(int(fpsHandler.get_fps())), 40, (255, 0, 0), 1150, 30)
		render.drawMiniMap(player)
		render.drawPlayerWeapon([wallShot, sprites.spriteShot])

		# Movement:

		player.handleControl()

		# Update Display:
		display.updateDisplay(60)

	# Quit: #
	destroyGame()

main()