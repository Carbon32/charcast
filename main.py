# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                           #
#                     Python Raycasting                     #
#                     Developer: Carbon                     #
#                                                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.engine import *

# Game: #

game = Game()

# Window: #

game.start_window()

# Map: #

game_map = Map(game)

# Player: #

game.player = Player(game)

# Object Renderer: #

object_renderer = ObjectRenderer(game)

# Raycasting: #

raycasting =  Raycasting(game, object_renderer)

# Pathfinding: #

pathfinding = Pathfinding(game)

# Sprite Handler: #

sprites_handler = SpritesHandler(game, pathfinding)

# Weapon: #

weapon = Weapon(game, 'assets/sprites/weapon/shotgun/0.png', 1.5, 90)

# Crosshair: #

crosshair = Crosshair(game)

# Game Loop: #

while(game.engine_running):
    sprites_handler.update()
    object_renderer.render()
    crosshair.render()
    game_map.draw_map()
    sprites_handler.show_npc_dots()
    weapon.draw()
    weapon.update()
    game.player.update(weapon)
    raycasting.update()
    game.update_display(60)

