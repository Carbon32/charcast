# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#													   		#
#			     Python Raycasting (Remake)	  		  		#
#			          Developer: Carbon				        #
#													   		#
#														    #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Imports: #

from engine import *

# Sprites: #

sprites = Sprite()

# Player: #

player = Player(sprites)

# Draw Elements: #

render = Render(window, miniMap, player)

# Interaction: #

interaction = Interaction(player, sprites, render)

# Music: #

# interaction.playMusic()

# Game Loop: #

def main():
	while(engineRunning):
		clearWindow(window)
		toggleMouseCursorOff()

		# Rendering: 

		render.drawBackground((0, 180, 255), (69, 69, 69), player.angle)
		walls, wallShot = rayCastingWalls(player, render.textures, worldMap)
		render.drawWorld(walls + [object.locateObject(player) for object in sprites.objectsList])
		render.drawText(str(int(fpsHandler.get_fps())), 40, (255, 0, 0), 1150, 30)
		render.drawMiniMap(player)
		render.drawPlayerWeapon([wallShot, sprites.spriteShot])
		interaction.interactionObject()
		interaction.npcAction()

		# Movement:

		player.handleControl()

		# Update Display:

		updateDisplay(60)

	# Quit: #
	
	destroyGame()

main()