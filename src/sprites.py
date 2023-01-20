# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                           #
#                     Python Raycasting                     #
#                     Developer: Carbon                     #
#                                                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Static Sprites: #

class StaticSprite():
	def __init__(self, game, path, position = (0, 0), scale = 1.0, shift = 0.0):

		# Game: #

		self.game = game

		# Properties:

		self.x, self.y = position
		self.image = pygame.image.load(path).convert_alpha()
		self.image_width = self.image.get_width()
		self.image_ratio = self.image_width / self.image.get_height()
		self.delta_x, self.delta_y, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
		self.sprite_half_width = 0
		self.sprite_scale = scale
		self.sprite_height_shift = shift

	def get_projection(self):
		projection = self.game.screen_dist / self.norm_dist * self.sprite_scale
		projection_width, projection_height = projection * self.image_ratio, projection

		image = pygame.transform.scale(self.image, (int(projection_width), int(projection_height)))

		self.sprite_half_width = projection_width // 2
		height_shift = projection_height * self.sprite_height_shift
		position = self.screen_x - self.sprite_half_width, (self.game.screen_height // 2) - projection_height // 2 + height_shift
		self.game.objects_to_render.append((self.norm_dist, image, position))

	def update_sprite(self):
		delta_x = self.x - self.game.player.x
		delta_y = self.y - self.game.player.y
		self.delta_x, self.delta_y = delta_x, delta_y
		self.theta = math.atan2(delta_y, delta_x)

		delta = self.theta - self.game.player.player_angle
		if(delta_x > 0 and self.game.player.player_angle > math.pi) or (delta_x < 0 and delta_y < 0):
			delta += math.tau

		delta_rays = delta / self.game.delta_angle
		self.screen_x = (self.game.half_rays_number + delta_rays) * self.game.scale

		self.dist = math.hypot(delta_x, delta_y)
		self.norm_dist = self.dist * math.cos(delta)
		if(-(self.image_width // 2) < self.screen_x < (self.game.screen_width + (self.image_width // 2)) and self.norm_dist > 0.5):
			self.get_projection()

	def update(self):
		self.update_sprite()

# Animated Sprites: #

class AnimatedSprite(StaticSprite):
	def __init__(self, game, path, position = (0, 0), scale = 1.0, shift = 0.0, animation_time = 120):
		super().__init__(game, path, position, scale, shift)

		# Properties:

		self.animation_time = animation_time
		self.path = path.rsplit('/', 1)[0]
		self.images = self.load_images(self.path)
		self.animation_previous_time = pygame.time.get_ticks()
		self.animation_trigger = False

	def update(self):
		super().update()
		self.check_animation_time()
		self.animate(self.images)

	def animate(self, images):
		if(self.animation_trigger):
			images.rotate(-1)
			self.image = images[0]

	def check_animation_time(self):
		self.animation_trigger = False
		time_now = pygame.time.get_ticks()
		if(time_now - self.animation_previous_time > self.animation_time):
			self.animation_previous_time = time_now
			self.animation_trigger = True

	def load_images(self, path):
		images = deque()
		for file_name in os.listdir(path):
			if(os.path.isfile(os.path.join(path, file_name))):
				image = pygame.image.load(f'{path}/{file_name}').convert_alpha()
				images.append(image)
		return images

# NPC: #

class NPC(AnimatedSprite):
	def __init__(self, game, pathfinding, path, position = (0, 0), scale = 1.0, shift = 0.0, animation_time = 180):
		super().__init__(game, path, position, scale, shift, animation_time)

		# Images:

		self.attack_images = self.load_images(self.path + '/attack')
		self.death_images = self.load_images(self.path + '/death')
		self.idle_images = self.load_images(self.path + '/idle')
		self.pain_images = self.load_images(self.path + '/pain')
		self.walk_images = self.load_images(self.path + '/walk')

		# Properties:

		self.attack_dist = random.randint(3, 6)
		self.speed = 0.03
		self.size = 10
		self.health = 100
		self.attack_damage = 10
		self.accuracy = 0.15
		self.alive = True
		self.pain = False
		self.raycast_value = False
		self.frame_counter = 0
		self.search_for_player = False

		# Pathfinding:

		self.pathfinding = pathfinding

	def update(self):
		self.check_animation_time()
		self.update_sprite()
		self.update_ai()

	def detect_collision(self, x, y):
		return (x, y) not in self.game.world_map

	def check_wall_collision(self, delta_x, delta_y):
		if(self.detect_collision(int(self.x + delta_x * self.size), int(self.y))):
			self.x += delta_x

		if(self.detect_collision(int(self.x), int(self.y + delta_y * self.size))):
			self.y += delta_y

	def attack(self):
		if(self.animation_trigger):
			self.game.sounds.play_sound('enemy_shoot', 0.2)
			if(random.random() < self.accuracy):
				self.game.player.damage(self.attack_damage)

	def move(self):
		next_position = self.pathfinding.get_path(self.map_position, self.game.player.map_position)
		next_x, next_y = next_position
		if(next_position not in self.game.npc_positions):
			angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
			delta_x = math.cos(angle) * self.speed
			delta_y = math.sin(angle) * self.speed
			self.check_wall_collision(delta_x, delta_y)

	def animate_pain(self):
		self.animate(self.pain_images)
		if(self.animation_trigger):
			self.game.sounds.play_sound('enemy_pain', 0.2)
			self.pain = False

	def animate_death(self):
		if(not self.alive):
			if(self.game.global_trigger and self.frame_counter < len(self.death_images) - 1):
				self.death_images.rotate(-1)
				self.image = self.death_images[0]
				self.frame_counter += 1

	def check_if_shot(self):
		if(self.raycast_value and self.game.player.shot):
			if((self.game.screen_width // 2) - self.sprite_half_width < self.screen_x < (self.game.screen_width // 2) + self.sprite_half_width):
				self.game.player.shot = False
				self.pain = True
				self.health -= self.game.player.weapon.damage
				self.check_health()

	def check_health(self):
		if(self.health < 1):
			self.alive = False
			self.game.sounds.play_sound('enemy_death', 0.2)

	def update_ai(self):
		if(self.alive):
			self.raycast_value = self.raycast_player_npc()
			self.check_if_shot()
			if(self.pain):
				self.animate_pain()
			elif(self.raycast_value):
				self.search_for_player = True
				if(self.dist < self.attack_dist):
					self.animate(self.attack_images)
					self.attack()
				else:
					self.animate(self.walk_images)
					self.move()
			elif(self.search_for_player):
				self.animate(self.walk_images)
				self.move()
			else:
				self.animate(self.idle_images)
		else:
			self.animate_death()

	@property
	def map_position(self):
		return int(self.x), int(self.y)

	def raycast_player_npc(self):
		if(self.game.player.map_position == self.map_position):
			return True

		wall_distance_v, wall_distance_h = 0, 0
		player_distance_v, player_distance_h = 0, 0

		ox, oy = self.game.player.position
		x_map, y_map = self.game.player.map_position
		ray_angle = self.theta
		
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
			if(tile_horizontal == self.map_position):
				player_distance_h = depth_horizontal
				break

			if(tile_horizontal in self.game.world_map):
				wall_distance_h = depth_horizontal
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
			if(tile_vertical == self.map_position):
				player_distance_v = depth_vertical
				break

			if(tile_vertical in self.game.world_map):
				wall_distance_v = depth_vertical
				break

			x_vertical += delta_x
			y_vertical += delta_y
			depth_vertical += delta_depth

		player_distance = max(player_distance_v, player_distance_h)
		wall_distance = max(wall_distance_v, wall_distance_h)

		if(0 < player_distance < wall_distance or not wall_distance):
			return True
		return False

# Weapon: #

class Weapon(AnimatedSprite):
	def __init__(self, game, path, scale, animation_time, damage, reload_speed, sound):
		super().__init__(game = game, path = path, scale = scale, animation_time = animation_time)

		# Properties:

		self.images = deque(
			[pygame.transform.smoothscale(image, (int(self.image.get_width() * scale), int(self.image.get_height() * scale)))
			for image in self.images]
		)
		self.x = (self.game.screen_width // 2) - self.images[0].get_width() // 2
		self.y = self.game.screen_height - self.images[0].get_height()
		self.reloading = False
		self.reload_speed = reload_speed
		self.number_of_images = len(self.images)
		self.frame_counter = 0
		self.damage = damage
		self.sound = sound

	def animate_shot(self):
		if(self.reloading):
			self.game.player.shot = False
			if(self.animation_trigger):
				self.images.rotate(-1)
				self.image = self.images[0]
				self.frame_counter += 1
				if(self.frame_counter == self.number_of_images):
					self.reloading = False
					self.frame_counter = 0

	def draw(self):
		self.game.display.blit(self.images[0], (self.x, self.y))

	def update(self):
		self.check_animation_time()
		self.animate_shot()

# Sprites Handler: #

class SpritesHandler():
	def __init__(self, game, pathfinding):

		# Game:

		self.game = game

		# Sprite Properties:

		self.sprite_list = []
		self.static_sprites_path = 'assets/sprites/static'
		self.animated_sprites_path = 'assets/sprites/animated'
		add_sprite = self.add_sprite

		# NPC Properties:

		self.npc_list = []
		self.npc_sprite_path = 'assets/sprites/npc'
		self.game.npc_positions = {}
		add_npc = self.add_npc

		# Game Sprites:

		add_sprite(StaticSprite(game, 'assets/sprites/static/corpse/1.png', (5.5, 1.5), 0.7, -0.2))
		add_sprite(StaticSprite(game, 'assets/sprites/static/corpse_2/1.png', (5.5, 7.5), 1.0, 0.2))
		add_sprite(AnimatedSprite(game, 'assets/sprites/animated/barrel/0.png', (4.5, 1.5), 0.8, 0.15, 140))
		add_sprite(AnimatedSprite(game, 'assets/sprites/animated/barrel/0.png', (6.75, 1.5), 0.8, 0.15, 140))

		# Game NPCs:

		add_npc(NPC(game, pathfinding, 'assets/sprites/npc/soldier/0.png', (5.5, 2.0), 0.6, 0.38))
		add_npc(NPC(game, pathfinding, 'assets/sprites/npc/soldier/0.png', (5.0, 6.0), 0.6, 0.38))

	def update(self):
		self.game.npc_positions = {npc.map_position for npc in self.npc_list if npc.alive}
		[sprite.update() for sprite in self.sprite_list]
		[npc.update() for npc in self.npc_list]
		self.show_npc_dots()

	def show_npc_dots(self):
		for npc in self.npc_list:
			if(npc.alive):
				pygame.draw.circle(self.game.display, (255, 0, 0), (npc.x * (self.game.screen_width // 80), npc.y * (self.game.screen_width // 80)), (self.game.screen_width // (self.game.screen_width // 5)))
	
	def add_npc(self, npc):
		self.npc_list.append(npc)

	def add_sprite(self, sprite):
		self.sprite_list.append(sprite)