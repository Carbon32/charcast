# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                           #
#                     Python Raycasting                     #
#                     Developer: Carbon                     #
#                                                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *
from src.button import *

# Menu: #

class Menu():
    def __init__(self, game):

        # Game:

        self.game = game

        # Restart:

        self.restart = False

        # Button Properties:

        self.buttons = {
            'music_on' : pygame.transform.scale(pygame.image.load('assets/Buttons/music_on.png'), (self.game.screen_width // 64, self.game.screen_width // 64)),
            'music_off' : pygame.transform.scale(pygame.image.load('assets/Buttons/music_off.png'), (self.game.screen_width // 64, self.game.screen_width // 64)),
            'sound_on' : pygame.transform.scale(pygame.image.load('assets/Buttons/sound_on.png'), (self.game.screen_width // 64, self.game.screen_width // 64)),
            'sound_off' : pygame.transform.scale(pygame.image.load('assets/Buttons/sound_off.png'), (self.game.screen_width // 64, self.game.screen_width // 64)),
            'map_on' : pygame.transform.scale(pygame.image.load('assets/Buttons/map_on.png'), (self.game.screen_width // 64, self.game.screen_width // 64)),
            'map_off' : pygame.transform.scale(pygame.image.load('assets/Buttons/map_off.png'), (self.game.screen_width // 64, self.game.screen_width // 64))

        }

        # Buttons:

        self.play_button = Button(self.game, 'Play', self.game.screen_width // 2 - (self.game.screen_width // 10), self.game.screen_height // 2 - (self.game.screen_height // 8), self.game.screen_width // 4, self.game.screen_width // 12, self.game.screen_width // 80, 'large')
        self.exit_button = Button(self.game, 'Exit', self.game.screen_width // 2 - (self.game.screen_width // 10), self.game.screen_height // 3 + (self.game.screen_height // 4), self.game.screen_width // 4, self.game.screen_width // 12, self.game.screen_width // 80, 'large')
        self.back_button = Button(self.game, 'Back', self.game.screen_width // 2 - (self.game.screen_width // 64),  self.game.screen_height // 3 + (self.game.screen_height // 2), self.game.screen_width // 14, self.game.screen_width // 20, self.game.screen_width // 256, 'small')
        self.music_button = ButtonImage(self.game.display, self.buttons["music_on"], self.game.screen_width // 2 + (self.game.screen_width // 2.3), self.game.screen_height // 2 - (self.game.screen_height // 2.1), self.game.screen_width // 32, self.game.screen_width // 32, self.game.screen_width // 256, self.game.screen_width // 64)
        self.sound_button = ButtonImage(self.game.display, self.buttons["sound_on"], self.game.screen_width // 2 + (self.game.screen_width // 2.8), self.game.screen_height // 2 - (self.game.screen_height // 2.1), self.game.screen_width // 32, self.game.screen_width // 32, self.game.screen_width // 256, self.game.screen_width // 64)
        self.map_button = ButtonImage(self.game.display, self.buttons["map_on"], self.game.screen_width // 2 + (self.game.screen_width // 2.3), self.game.screen_height // 2 - (self.game.screen_height // 2.6), self.game.screen_width // 32, self.game.screen_width // 32, self.game.screen_width // 256, self.game.screen_width // 64)

        # Title:

        self.step = 0
        self.title_background_color = (184, 160, 238)

    def handle_menu(self):
        if(self.game.menu_on):
            self.game.display.fill((40, 42, 53))
            bounce = -1 * math.sin(self.step) * self.game.screen_width // 64
            pygame.draw.rect(self.game.display, self.title_background_color, pygame.Rect(self.game.screen_width // 3.7, self.game.screen_height // 24 + bounce, self.game.screen_width - (self.game.screen_width // 2), self.game.screen_height // 5), border_radius = self.game.screen_width // 38)
            pygame.draw.rect(self.game.display, (0, 0, 0), pygame.Rect(self.game.screen_width // 3.7, self.game.screen_height // 24 + bounce, self.game.screen_width - (self.game.screen_width // 2), self.game.screen_height // 5), self.game.screen_width // 128, border_radius = self.game.screen_width // 38)
            self.game.draw_custom_text(self.game.fonts['huge'], 'Raycasting', (0, 0, 0), self.game.screen_width // 2.9, (0 + self.game.screen_height // 12) + bounce)
            self.step += 0.05
            pygame.mouse.set_visible(True)
            if(self.play_button.render()):
                self.restart = True
                self.game.menu_on = False

            if(self.exit_button.render()):
                self.game.engine_running = False
                quit()

            if(self.music_button.render()):
                if(self.game.sounds.music_status):
                    self.music_button.change_button(self.buttons["music_off"])
                    self.game.sounds.music_status = False
                    self.game.sounds.stop_music()
                else:
                    self.music_button.change_button(self.buttons["music_on"])
                    self.game.sounds.music_status = True
                    self.game.sounds.play_music('sounds/music.mp3', 1)

            if(self.sound_button.render()):
                if(self.game.sounds.sound_status):
                    self.sound_button.change_button(self.buttons["sound_off"])
                    self.game.sounds.sound_status = False
                else:
                    self.sound_button.change_button(self.buttons["sound_on"])
                    self.game.sounds.sound_status = True

            if(self.map_button.render()):
                if(self.game.map_status):
                    self.map_button.change_button(self.buttons["map_off"])
                    self.game.map_status = False
                else:
                    self.map_button.change_button(self.buttons["map_on"])
                    self.game.map_status = True

            if(self.game.game_started):
                self.play_button.change_text('large', 'Restart')
                if(self.back_button.render()):
                    self.game.menu_on = False

