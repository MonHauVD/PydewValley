import pygame
import json
from settings import *
from support import *
from timer import Timer


class Player(pygame.sprite.Sprite):
	def __init__(self, pos, group, collision_sprites, tree_sprites, interaction, soil_layer, toggle_shop, inventory_show, menu_show, sfxVolume):
		super().__init__(group)

		self.import_assets()
		self.status = 'down_idle'
		self.frame_index = 0

		# general setup
		self.image = self.animations[self.status][self.frame_index]
		self.rect = self.image.get_rect(center=pos)
		self.z = LAYERS['main']

		# movement attributes
		self.direction = pygame.math.Vector2()
		self.pos = pygame.math.Vector2(self.rect.center)
		self.speed = 200

		# collision
		self.hitbox = self.rect.copy().inflate((-126, -70))
		self.collision_sprites = collision_sprites

		# timers
		self.timers = {
			'tool use': Timer(350, self.use_tool),
			'tool switch': Timer(200),
			'seed use': Timer(350, self.use_seed),
			'seed switch': Timer(200),
		}

		# tools
		self.tools = ['hoe', 'axe', 'water']
		self.tool_index = 0
		self.selected_tool = self.tools[self.tool_index]

		# seeds
		self.seeds = ['corn', 'tomato']
		self.seed_index = 0
		self.selected_seed = self.seeds[self.seed_index]

		# inventory
		self.item_inventory = {
			'wood':   20,
			'apple':  20,
			'corn':   20,
			'tomato': 20
		}
		self.seed_inventory = {
			'corn': 5,
			'tomato': 5
		}
		self.money = 200

		# interaction
		self.tree_sprites = tree_sprites
		self.interaction = interaction
		self.sleep = False
		self.soil_layer = soil_layer
		self.toggle_shop = toggle_shop
		self.inventory_show = inventory_show
		self.menu_show = menu_show

		# sound
		self.sfxVolume = sfxVolume
		self.watering = pygame.mixer.Sound('../audio/water.mp3')
		self.watering.set_volume(self.sfxVolume/100)

	def setSFXVolume(self, sfxVolume1):
		self.sfxVolume = sfxVolume1

	def use_tool(self):
		if self.selected_tool == 'hoe':
			self.soil_layer.get_hit(self.target_pos)

		if self.selected_tool == 'axe':
			for tree in self.tree_sprites.sprites():
				if tree.rect.collidepoint(self.target_pos):
					try:
						if (tree.health > 0):
							tree.damage()
							tree.setSFXVolume(self.sfxVolume)
					except:
						print("Loi 'Particle' object has no attribute 'damage'")

		if self.selected_tool == 'water':
			self.soil_layer.water(self.target_pos)
			self.watering.set_volume(self.sfxVolume/100)
			self.watering.play()

	def get_target_pos(self):

		self.target_pos = self.rect.center + \
			PLAYER_TOOL_OFFSET[self.status.split('_')[0]]

	def use_seed(self):
		if self.seed_inventory[self.selected_seed] > 0:
			seedAble = self.soil_layer.plant_seed(
				self.target_pos, self.selected_seed)
			if seedAble == True:
				self.seed_inventory[self.selected_seed] -= 1

	def import_assets(self):
		self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
						   'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
						   'right_hoe': [], 'left_hoe': [], 'up_hoe': [], 'down_hoe': [],
						   'right_axe': [], 'left_axe': [], 'up_axe': [], 'down_axe': [],
						   'right_water': [], 'left_water': [], 'up_water': [], 'down_water': []}

		for animation in self.animations.keys():
			full_path = '../graphics/character/' + animation
			self.animations[animation] = import_folder(full_path)

	def animate(self, dt):
		self.frame_index += 4 * dt
		if self.frame_index >= len(self.animations[self.status]):
			self.frame_index = 0

		self.image = self.animations[self.status][int(self.frame_index)]

	def input(self):
		keys = pygame.key.get_pressed()

		if not self.timers['tool use'].active and not self.sleep:
			# directions
			if keys[pygame.K_UP] or keys[pygame.K_w]:
				self.direction.y = -1
				self.status = 'up'
			elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
				self.direction.y = 1
				self.status = 'down'
			else:
				self.direction.y = 0

			if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
				self.direction.x = 1
				self.status = 'right'
			elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
				self.direction.x = -1
				self.status = 'left'
			else:
				self.direction.x = 0

			# tool use
			if keys[pygame.K_SPACE]:
				self.timers['tool use'].activate()
				self.direction = pygame.math.Vector2()
				self.frame_index = 0

			# change tool
			if keys[pygame.K_1] and not self.timers['tool switch'].active:
				self.timers['tool switch'].activate()
				self.tool_index += 1
				self.tool_index = self.tool_index if self.tool_index < len(
					self.tools) else 0
				self.selected_tool = self.tools[self.tool_index]

			# seed use
			if keys[pygame.K_q]:
				self.timers['seed use'].activate()
				self.direction = pygame.math.Vector2()
				self.frame_index = 0

			# change seed
			if keys[pygame.K_2] and not self.timers['seed switch'].active:
				self.timers['seed switch'].activate()
				self.seed_index += 1
				self.seed_index = self.seed_index if self.seed_index < len(
					self.seeds) else 0
				self.selected_seed = self.seeds[self.seed_index]

			# if keys[pygame.K_RETURN]:
			if keys[pygame.K_e]:
				collided_interaction_sprite = pygame.sprite.spritecollide(
					self, self.interaction, False)
				if collided_interaction_sprite:
					if collided_interaction_sprite[0].name == 'Trader':
						self.toggle_shop()
					else:
						self.status = 'left_idle'
						self.sleep = True
				else:
					self.timers['tool use'].activate()
					self.direction = pygame.math.Vector2()
					self.frame_index = 0

			if keys[pygame.K_i]:
				self.inventory_show()

			if keys[pygame.K_k]:
				self.saveGame()

			if keys[pygame.K_l]:
				self.loadGame()

			if keys[pygame.K_m]:
				self.menu_show()

	def get_status(self):

		# idle
		if self.direction.magnitude() == 0:
			self.status = self.status.split('_')[0] + '_idle'

		# tool use
		if self.timers['tool use'].active:
			self.status = self.status.split('_')[0] + '_' + self.selected_tool

	def update_timers(self):
		for timer in self.timers.values():
			timer.update()

	def collision(self, direction):
		for sprite in self.collision_sprites.sprites():
			if hasattr(sprite, 'hitbox'):
				if sprite.hitbox.colliderect(self.hitbox):
					if direction == 'horizontal':
						if self.direction.x > 0:  # moving right
							self.hitbox.right = sprite.hitbox.left
						if self.direction.x < 0:  # moving left
							self.hitbox.left = sprite.hitbox.right
						self.rect.centerx = self.hitbox.centerx
						self.pos.x = self.hitbox.centerx

					if direction == 'vertical':
						if self.direction.y > 0:  # moving down
							self.hitbox.bottom = sprite.hitbox.top
						if self.direction.y < 0:  # moving up
							self.hitbox.top = sprite.hitbox.bottom
						self.rect.centery = self.hitbox.centery
						self.pos.y = self.hitbox.centery

	def move(self, dt):

		# normalizing a vector
		if self.direction.magnitude() > 0:
			self.direction = self.direction.normalize()

		# horizontal movement
		self.pos.x += self.direction.x * self.speed * dt
		self.hitbox.centerx = round(self.pos.x)
		self.rect.centerx = self.hitbox.centerx
		self.collision('horizontal')

		# vertical movement
		self.pos.y += self.direction.y * self.speed * dt
		self.hitbox.centery = round(self.pos.y)
		self.rect.centery = self.hitbox.centery
		self.collision('vertical')

	def update(self, dt):
		self.input()
		self.get_status()
		self.update_timers()
		self.get_target_pos()

		self.move(dt)
		self.animate(dt)

	def saveGame(self):
		with open('../save/inventory_save.txt', 'w') as inventory_save:
			saved_inventory = {"item": self.item_inventory,
							   "seed": self.seed_inventory,
							   "money": self.money}
			json.dump(saved_inventory, inventory_save)
		self.soil_layer.save_soil_grid()

	def loadGame(self):
		with open('../save/inventory_save.txt') as inventory_save:
			saved_inventory = json.load(inventory_save)
			self.item_inventory = saved_inventory["item"]
			self.seed_inventory = saved_inventory["seed"]
			self.money = saved_inventory["money"]
		self.soil_layer.load_soil_grid()
