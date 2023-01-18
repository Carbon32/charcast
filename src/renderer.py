# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                           #
#                     Python Raycasting                     #
#                     Developer: Carbon                     #
#                                                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Object Renderer: #

class ObjectRenderer():
	def __init__(self, game):

		# Game:

		self.game = game

		# Textures:

		self.wall_textures = self.assign_wall_textures()

		# Sky:

		self.roof_image = self.load_texture('assets/roof/roof.png', (self.game.screen_width, self.game.screen_height // 2))
		self.roof_offset = 0

	def render(self):
		self.render_floor((30, 30, 30))
		self.render_roof(self.roof_image)
		self.render_objects()

	def render_roof(self, image):
		self.roof_offset = (self.roof_offset + 4.0 * self.game.player.rel) % self.game.screen_width
		self.game.display.blit(image, (-self.roof_offset, 0))
		self.game.display.blit(image, (-self.roof_offset + self.game.screen_width, 0))

	def render_floor(self, color):
		pygame.draw.rect(self.game.display, color, (0, self.game.screen_height // 2, self.game.screen_width, self.game.screen_height))	
	
	def render_objects(self):
		list_objects = sorted(self.game.objects_to_render, key = lambda t: t[0], reverse = True)
		for depth, image, position in list_objects:
			self.game.display.blit(image, position)

	def load_texture(self, path, resolution):
		texture = pygame.image.load(path).convert_alpha()
		return pygame.transform.scale(texture, resolution)

	def assign_wall_textures(self):
		return {
			1: self.load_texture('assets/textures/1.png', (self.game.texture_size, self.game.texture_size)),
			2: self.load_texture('assets/textures/2.png', (self.game.texture_size, self.game.texture_size)),
		}
