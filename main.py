# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                           #
#                     Python Raycasting                     #
#                     Developer: Carbon                     #
#                                                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.engine import *

# Sounds: #

sounds = Sounds()

# Game: #

game = Game(sounds)

# Resolution: #

resolution = Resolution(game)

# Resoltuion Selection: #

while(resolution.resolution_status):
    resolution.update_background()
    if(resolution.resolution_a.render()):
        resolution.set_resolution(1280, 720)
        break

    if(resolution.resolution_b.render()):
        resolution.set_resolution(1920, 1080)
        break

    resolution.update_window()

# Window: #

game.start_window()

# Weapon: #

primary_weapon = Weapon(game, 'assets/sprites/weapon/handgun/0.png', 6.2, 50, 25, 0.3, 'handgun', (game.screen_width // 32, game.screen_height // 16))
secondary_weapon = Weapon(game, 'assets/sprites/weapon/shotgun/0.png', 1.5, 90, 50, 1, 'shotgun',  (game.screen_width // 4, game.screen_height // 4))

# Weapons Manager: #

weapons_manager = WeaponsManager(game, [primary_weapon, secondary_weapon])

# Crosshair: #

crosshair = Crosshair(game)

# Menu: #

menu = Menu(game)

# Fade: #

start_fade = Fade(game, 1, ((0, 0, 0)))

# Music: #

sounds.play_music('sounds/music.mp3', 1)

# Game Loop: #

while(game.engine_running):
    if(game.menu_on):
        menu.handle_menu()
        start_fade.reset()
    else:
        if(menu.restart):
 
            # Player: #

            game.player = Player(game)

            # Map: #

            game_map = Map(game)

            # Pathfinding: #

            pathfinding = Pathfinding(game)

            # Renderer: #

            object_renderer = ObjectRenderer(game)

            # Raycasting: #

            raycasting =  Raycasting(game, object_renderer)

            # Sprites Manager: #

            sprites_handler = SpritesHandler(game, pathfinding)

            # Continue:

            menu.restart = False

        game.toggle_mouse()
        game.set_game_started()
        sprites_handler.update()
        object_renderer.render()
        crosshair.render()
        game_map.draw_map()
        sprites_handler.show_npc_dots()
        weapons_manager.render()
        weapons_manager.check_weapon_change()
        game.player.update(weapons_manager.current_weapon)
        game.show_damage()
        start_fade.fade()
        raycasting.update()

    game.update_display(60)

