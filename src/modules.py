# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                           #
#                     Python Raycasting                     #
#                     Developer: Carbon                     #
#                                                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

try:
    import pygame 
    import sys
    import math
    import os
    import random
    from collections import deque
    from pygame import mixer

except ImportError:
    raise ImportError("The Raycasting Engine couldn't import all of the necessary packages.")

# Pygame Initialization: #

pygame.init()

# Mixer Initialization: #

pygame.mixer.pre_init(44100, 16, 2, 4096)
mixer.init()