# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                           #
#                     Python Raycasting                     #
#                     Developer: Carbon                     #
#                                                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Game: #

class Game():
    def __init__(self, sounds):

        # Display:

        self.screen_width = 1920
        self.screen_height = 1080
        self.fps_handler = pygame.time.Clock()
        self.delta_time = 1
        self.enigne_running = False

        # Sounds:

        self.sounds = sounds

        # Textures:

        self.texture_size = 256

        # World Map:

        self.map_status = True
        self.world_map = {}

        # Objects:

        self.objects_to_render = []

        # Event Timer:

        self.global_trigger = False
        self.global_event = pygame.USEREVENT + 0
        pygame.time.set_timer(self.global_event, 40)

        # Game State:

        self.game_started = False

        # Menu:

        self.menu_on = True

        # Damage Properties:

        self.damage_list = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]

    def start_window(self):
        self.display = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN | pygame.DOUBLEBUF)
        pygame.display.set_caption('Python Raycasting: ')
        self.engine_running = True
        self.fonts = {
            'huge' : pygame.font.Font(os.getcwd() + '/game_font.ttf', self.screen_width // 14),
            'large' : pygame.font.Font(os.getcwd() + '/game_font.ttf', self.screen_width // 20),
            'small' : pygame.font.Font(os.getcwd() + '/game_font.ttf', self.screen_width // 48)
        }

    def toggle_mouse(self):
        pygame.mouse.set_visible(False)

    def set_game_started(self):
        self.game_started = True

    def draw_custom_text(self, font, text, color, x, y):
        image = font.render(text, True, color)
        self.display.blit(image, (x, y))

    def show_damage(self):
        if(self.player.damaged):
            effect = min(255, max(0, round(255 * (1 - self.damage_list[self.player.health // 10]))))
            self.display.fill((255, effect, effect), special_flags = pygame.BLEND_MULT)

    def update_display(self, fps):
        self.delta_time = self.fps_handler.tick(fps)
        self.global_trigger = False
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                self.engine_running = False
            elif(event.type == self.global_event):
                self.global_trigger = True
            elif(event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.menu_on = True

        pygame.display.update()


