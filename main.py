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

# Sounds: #

sounds = Sounds()
sounds.musicStatus = True
sounds.soundStatus = False
sounds.playMusic()

# Game Loop: #

def main():
	while(game.engineRunning):
		clearWindow(window)
		toggleMouseCursorOff()

		# Update Walls:

		walls.updateWalls(player.position, player.angle, render.textures, worldMap)

		# Rendering: 

		render.drawBackground(player.angle)
		render.drawFloor((80, 80, 80))
		render.drawWorld(walls.wallStatus() + [object.locateObject(player) for object in sprites.objectsList])
		render.drawText(str(int(fpsHandler.get_fps())), 40, (255, 0, 0), 1150, 30)
		render.drawMiniMap(player, sprites)
		render.drawPlayerWeapon([walls.shotWalls(), sprites.spriteShot], sounds.soundStatus)
		render.drawUI(sounds.musicStatus, sounds.soundStatus)

		# Game Interaction: 

		interaction.interactionObject()
		interaction.npcAction()

		# Game Status:

		game.gameStatus()

		# Movement:

		player.handleControl()
		sounds.soundControl()

		# Update Display:
		
		updateDisplay(60)

	# Quit:

	destroyGame()

main()