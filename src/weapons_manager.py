# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                           #
#                     Python Raycasting                     #
#                     Developer: Carbon                     #
#                                                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Weapons Manager: #

class WeaponsManager():
    def __init__(self, game, weapons):

        # Game:

        self.game = game

        # Properties:

        self.weapons = weapons
        self.current_weapon_id = 0
        self.current_weapon = weapons[self.current_weapon_id]
        self.current_weapon.y = self.game.screen_height - self.current_weapon.images[0].get_height()

        # Animation:

        self.animation_time = -1
        self.change_time = 300
        self.hostler = False
        self.unhostler = False
        self.old_y = 0

        # Timer:

        self.scroll_cooldown = 500
        self.scroll_time = pygame.time.get_ticks()

    def render(self):
        self.current_weapon.draw()
        self.current_weapon.update()

    def check_weapon_change(self):
        if(self.current_weapon.reloading == False):
            if(pygame.key.get_pressed()[pygame.K_a]):
                if(pygame.time.get_ticks() - self.scroll_time > self.scroll_cooldown):
                    if(not self.current_weapon_id == 0):
                        if(not (self.hostler or self.unhostler)):
                            self.hostler = True
                            self.next_weapon = -1

            if(pygame.key.get_pressed()[pygame.K_e]):
                if(pygame.time.get_ticks() - self.scroll_time > self.scroll_cooldown):
                    if(not self.current_weapon_id == len(self.weapons) - 1):
                        if(not (self.hostler or self.unhostler)):
                            self.hostler = True
                            self.next_weapon = 1

            self.animate_change()

    def animate_change(self):
        if(self.hostler == True):
            self.current_weapon.y += self.game.screen_width // 32
            if(self.animation_time == -1):
                self.animation_time = pygame.time.get_ticks()

            if(pygame.time.get_ticks() - self.animation_time > self.change_time):
                self.old_y = self.current_weapon.y
                self.current_weapon_id += self.next_weapon
                self.current_weapon = self.weapons[self.current_weapon_id]
                self.current_weapon.y = self.old_y
                self.hostler = False
                self.unhostler = True
                self.animation_time = -1

        if(self.unhostler):
            if(not self.current_weapon.y < self.game.screen_height - self.current_weapon.images[0].get_height() + self.game.screen_width // 32):
                self.current_weapon.y -= self.game.screen_width // 32

            if(self.animation_time == -1):
                self.animation_time = pygame.time.get_ticks()

            if(pygame.time.get_ticks() - self.animation_time > self.change_time):
                self.animation_time = -1
                self.current_weapon.y = self.game.screen_height - self.current_weapon.images[0].get_height()
                self.scroll_time = pygame.time.get_ticks()
                self.unhostler = False


