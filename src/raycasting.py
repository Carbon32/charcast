# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                           #
#                     Python Raycasting                     #
#                     Developer: Carbon                     #
#                                                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Raycasting: #

class Raycasting:
	def __init__(self, game, object_renderer):

		# Game:

		self.game = game

		# Object Renderer:

		self.object_renderer = object_renderer

		# Raycasting:

		self.raycasting = []
		self.textures = self.object_renderer.wall_textures

		# Properties:

		self.fov = math.pi / 3
		self.half_fov = self.fov / 2
		self.game.rays_number = self.game.screen_width // 2
		self.game.half_rays_number = self.game.rays_number // 2
		self.game.delta_angle = self.fov / self.game.rays_number
		self.game.max_depth = 20
		self.game.screen_dist = (self.game.screen_width // 2) / math.tan(self.half_fov)
		self.game.scale = self.game.screen_width // self.game.rays_number

	def get_objects_to_render(self):
		self.game.objects_to_render = []
		for ray, values in enumerate(self.raycasting):
			depth, projection_height, texture, offset = values
			if(projection_height < self.game.screen_height):
				wall_column = self.textures[texture].subsurface(
					offset * (self.game.texture_size - self.game.scale), 0, self.game.scale, self.game.texture_size
				)
				wall_column = pygame.transform.scale(wall_column, (self.game.scale, projection_height))
				wall_position = (ray * self.game.scale, (self.game.screen_height // 2) - projection_height // 2)
			else:
				texture_height = self.game.texture_size * self.game.screen_height / projection_height
				wall_column = self.textures[texture].subsurface(
					offset * (self.game.texture_size - self.game.scale), (self.game.texture_size // 2) - texture_height // 2,
					self.game.scale, texture_height
				)

				wall_column = pygame.transform.scale(wall_column, (self.game.scale, self.game.screen_height))
				wall_position = (ray * self.game.scale, 0)
			self.game.objects_to_render.append((depth, wall_column, wall_position))


	def raycast(self):
		self.raycasting = []
		ox, oy = self.game.player.position
		x_map, y_map = self.game.player.map_position
		ray_angle = self.game.player.player_angle - self.half_fov + 0.0001
		for ray in range(self.game.rays_number):
			sin_a = math.sin(ray_angle)
			cos_a = math.cos(ray_angle)

			# Horizontals: 

			y_horizontal, delta_y = (y_map + 1, 1) if(sin_a > 0) else (y_map - 1e-6, -1)
			depth_horizontal = (y_horizontal - oy) / sin_a
			x_horizontal = ox + depth_horizontal * cos_a
			delta_depth = delta_y / sin_a
			delta_x = delta_depth * cos_a

			for i in range(self.game.max_depth):
				tile_horizontal = int(x_horizontal), int(y_horizontal)
				if(tile_horizontal in self.game.world_map):
					texture_horizontal = self.game.world_map[tile_horizontal]
					break

				x_horizontal += delta_x
				y_horizontal += delta_y
				depth_horizontal += delta_depth

			# Verticals:

			x_vertical, delta_x = (x_map + 1, 1) if(cos_a > 0) else (x_map - 1e-6, -1)
			depth_vertical = (x_vertical - ox) / cos_a
			y_vertical = oy + depth_vertical * sin_a
			delta_depth = delta_x / cos_a
			delta_y = delta_depth * sin_a
			for i in range(self.game.max_depth):
				tile_vertical = int(x_vertical), int(y_vertical)
				if(tile_vertical in self.game.world_map):
					texture_vertical = self.game.world_map[tile_vertical]
					break

				x_vertical += delta_x
				y_vertical += delta_y
				depth_vertical += delta_depth

			# Depth: 
			if(depth_vertical < depth_horizontal):
				depth, texture = depth_vertical, texture_vertical
				y_vertical %= 1
				offset = y_vertical if(cos_a > 0) else (1 - y_vertical)
			else:
				depth, texture = depth_horizontal, texture_horizontal
				x_horizontal %= 1
				offset = (1 - x_horizontal) if(sin_a > 0) else x_horizontal

			# Fishbowl Effect:

			depth *= math.cos(self.game.player.player_angle - ray_angle)

			# 3D Projection:

			projection_height = self.game.screen_dist / (depth + 0.0001)
			
			# Raycasting:

			self.raycasting.append((depth, int(projection_height), texture, offset))

			# Update Angle:

			ray_angle += self.game.delta_angle 

	def update(self):
		self.raycast()
		self.get_objects_to_render()
