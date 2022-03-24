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

# Game Status: #

game = Game()

# Walls: #

walls = Walls()

# Interaction: #

interaction = Interaction(player, sprites, render)

# Music: #

# interaction.playMusic() # Music Disabled

# Game Loop: #

def main():
	while(game.engineRunning):
		clearWindow(window)
		toggleMouseCursorOff()

		# Update Walls:

		walls.updateWalls(player.position, player.angle, render.textures, worldMap)

		# Rendering: 

		render.drawBackground((0, 180, 255), (69, 69, 69), player.angle)
		render.drawWorld(walls.wallStatus() + [object.locateObject(player) for object in sprites.objectsList])
		render.drawText(str(int(fpsHandler.get_fps())), 40, (255, 0, 0), 1150, 30)
		render.drawMiniMap(player, sprites)
		render.drawPlayerWeapon([walls.shotWalls(), sprites.spriteShot])*

		# Game Interaction: 

		interaction.interactionObject()
		interaction.npcAction()

		# Game Status:

		game.gameStatus()

		# Movement:

		player.handleControl()

		# Update Display:
		
		updateDisplay(60)

	# Quit:

	destroyGame()

main()