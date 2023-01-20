# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                           #
#                     Python Raycasting                     #
#                     Developer: Carbon                     #
#                                                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Sounds: #

class Sounds():
    def __init__(self):

        # Music:

        self.music_status = True

        # Sounds: 

        self.sound_status = True

        # Available Sounds: 

        self.sounds = {
            'handgun' : pygame.mixer.Sound('sounds/handgun.ogg'),
            'shotgun' : pygame.mixer.Sound('sounds/shotgun.ogg'),
            'enemy_shoot' : pygame.mixer.Sound('sounds/enemy_shoot.ogg'),
            'enemy_pain' : pygame.mixer.Sound('sounds/enemy_pain.ogg'),
            'enemy_death' : pygame.mixer.Sound('sounds/enemy_death.ogg'),
            'pain' : pygame.mixer.Sound('sounds/pain.ogg')
        }

    def  play_sound(self, sound, volume):
        if(self.sound_status):
            self.sounds[sound].set_volume(volume)
            pygame.mixer.Sound.play(self.sounds[sound])

    def stop_sound(self, sound):
        pygame.mixer.Sound.stop(self.sounds[sound])

    def play_music(self, music, volume):
        if(self.music_status):
            pygame.mixer.music.load(music)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1, 0.0, 5000)

    def stop_music(self):
        pygame.mixer.music.stop()
