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

primary_weapon = Weapon(game, 'assets/sprites/weapon/handgun/0.png', 6.2, 50, 25, 0.3)
secondary_weapon = Weapon(game, 'assets/sprites/weapon/shotgun/0.png', 1.5, 90, 50, 1)

# Weapons Manager: #

weapons_manager = WeaponsManager(game, [primary_weapon, secondary_weapon])

# Crosshair: #

crosshair = Crosshair(game)

# Game Loop: #

while(game.engine_running):
    sprites_handler.update()
    object_renderer.render()
    crosshair.render()
    game_map.draw_map()
    sprites_handler.show_npc_dots()
    weapons_manager.render()
    weapons_manager.check_weapon_change()
    game.player.update(weapons_manager.current_weapon)
    raycasting.update()
    game.update_display(60)

