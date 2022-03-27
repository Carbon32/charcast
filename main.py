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

# Menu: #

menu = Menu(window)

# Walls: #

walls = Walls()

# Interaction: #

interaction = Interaction(player, sprites, render)

# Sounds: #

sounds = Sounds()
sounds.playMusic()

# Game Loop: #

def main():
	while(game.engineRunning):

		# Clear Window:

		clearWindow(window)

		# User Interface: 

		render.drawUI(sounds.musicStatus, sounds.soundStatus)

		# Menu: 

		if(menu.menuStatus):
			menu.handleMenu(sounds.musicStatus, sounds.soundStatus)
			if(menu.playButton.render(window)):

				menu.menuStatus = False
				toggleMouseCursorOff()

			if(menu.exitButton.render(window)):

				game.engineRunning = False

			if(menu.musicButton.render(window)):

				if(sounds.musicStatus):

					sounds.musicStatus = False
					stopMusic()

				else:

					sounds.musicStatus = True
					sounds.playMusic()

			if(menu.soundButton.render(window)):

				if(sounds.soundStatus):

					sounds.soundStatus = False

				else:

					sounds.soundStatus = True

		else:

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
			render.drawCrosshair()

			# Game Interaction: 

			interaction.interactionObject()
			interaction.npcAction()
			menu.checkMenu()

			# Movement:

			player.handleControl()

		# Update Display:
		
		updateDisplay(60)

	# Quit:

	destroyGame()

main()