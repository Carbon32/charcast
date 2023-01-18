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
    def __init__(self):

        # Display:

        self.screen_width = 1920
        self.screen_height = 1080
        self.fps_handler = pygame.time.Clock()
        self.delta_time = 1
        self.enigne_running = False

        # Textures:

        self.texture_size = 256

        # World Map:

        self.world_map = {}

        # Objects:

        self.objects_to_render = []

        # Event Timer:

        self.global_trigger = False
        self.global_event = pygame.USEREVENT + 0
        pygame.time.set_timer(self.global_event, 40)

    def start_window(self):
        self.display = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Python Raycasting: ')
        self.engine_running = True

        # TEMPORARY:
        pygame.mouse.set_visible(False)

    def update_display(self, fps):
        self.delta_time = self.fps_handler.tick(fps)
        self.global_trigger = False
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                self.engine_running = False
            elif(event.type == self.global_event):
                self.global_trigger = True

        pygame.display.update()


