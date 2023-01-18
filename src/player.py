# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                           #
#                     Python Raycasting                     #
#                     Developer: Carbon                     #
#                                                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Player: #

class Player():
    def __init__(self, game):

        # Game

        self.game = game

        # Player Properties:

        self.x, self.y = 1.5, 5
        self.player_angle = 0
        self.player_speed = 0.004
        self.player_rotation_speed = 0.002
        self.player_size = 60
        self.max_health = 100
        self.health = self.max_health
        self.rel = 0

        # Shooting:

        self.shot = False
        self.shooting_timer = pygame.time.get_ticks()
        self.shooting_cooldown = 1000

        # Mouse Movement:

        self.mouse_sensitivity = 0.0003
        self.mouse_max_rel = 40
        self.mouse_border_left = 100
        self.mouse_border_right = self.game.screen_width - self.mouse_border_left

    def check_shooting(self, weapon):
        if(pygame.time.get_ticks() - self.shooting_timer > self.shooting_cooldown and not weapon.reloading):
            if(pygame.mouse.get_pressed()[0] == 1 and self.shot == False and not weapon.reloading):
                self.shot = True
                self.shooting_timer = pygame.time.get_ticks()
                weapon.reloading = True

    def damage(self, damage):
        self.health -= damage

    def move(self):
        sin_a = math.sin(self.player_angle)
        cos_a = math.cos(self.player_angle)
        delta_x, delta_y = 0, 0
        speed = self.player_speed * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        if(pygame.key.get_pressed()[pygame.K_z]):
            delta_x += speed_cos
            delta_y += speed_sin

        if(pygame.key.get_pressed()[pygame.K_s]):
            delta_x += -speed_cos
            delta_y += -speed_sin

        if(pygame.key.get_pressed()[pygame.K_q]):
            delta_x += speed_sin
            delta_y += -speed_cos

        if(pygame.key.get_pressed()[pygame.K_d]):
            delta_x += -speed_sin
            delta_y += speed_cos

        self.check_wall_collision(delta_x, delta_y)
        self.player_angle %= math.tau

    def draw_player(self):
        pygame.draw.circle(self.game.display, (0, 0, 255), (self.x * 100, self.y * 100), 15)

    def detect_collision(self, x, y):
        return (x, y) not in self.game.world_map

    def check_wall_collision(self, delta_x, delta_y):
        scale = self.player_size / self.game.delta_time
        if(self.detect_collision(int(self.x + delta_x * scale), int(self.y))):
            self.x += delta_x

        if(self.detect_collision(int(self.x), int(self.y + delta_y * scale))):
            self.y += delta_y

    def mouse_control(self):
        mx, my = pygame.mouse.get_pos()
        if(mx < self.mouse_border_left or mx > self.mouse_border_right):
            pygame.mouse.set_pos([self.game.screen_width // 2, self.game.screen_height // 2])

        self.rel = pygame.mouse.get_rel()[0]
        self.rel = max(-self.mouse_max_rel, min(self.mouse_max_rel, self.rel))
        self.player_angle += self.rel * self.mouse_sensitivity * self.game.delta_time

    def show_health_bar(self):
        pygame.draw.rect(self.game.display, (250, 0, 0), (self.game.screen_width // 4, self.game.screen_height // 64, (self.game.screen_width // 5), self.game.screen_width // 80), border_radius = self.game.screen_width // 128)
        pygame.draw.rect(self.game.display, (0, 250, 0), (self.game.screen_width // 4, self.game.screen_height // 64, (self.game.screen_width // 5) * (self.health / self.max_health), self.game.screen_width // 80), border_radius = self.game.screen_width // 128)
        pygame.draw.rect(self.game.display, (0, 0, 0), (self.game.screen_width // 4, self.game.screen_height // 64, (self.game.screen_width // 5), self.game.screen_width // 80), self.game.screen_width // (self.game.screen_width // 4), border_radius = self.game.screen_width // 128)

    def show_map_dot(self):
        pygame.draw.circle(self.game.display, (135, 206, 235), (self.x * (self.game.screen_width // 80), self.y * (self.game.screen_width // 80)), (self.game.screen_width // (self.game.screen_width // 5)))

    def update(self, weapon):
        self.weapon = weapon
        self.move()
        self.check_shooting(weapon)
        self.mouse_control()
        self.show_health_bar()
        self.show_map_dot()

    @property
    def position(self):
        return self.x, self.y
    
    @property
    def map_position(self):
        return int(self.x), int(self.y)


