import pygame
from settings import *
from timer import Timer
import sys
import settings


class MainMenu:
	def __init__(self, player, toggle_menu, mainMusic, musicVolume, sfxVolume, soil_layer, mainLevel):

		# general setup
		self.player = player
		self.toggle_menu = toggle_menu
		self.display_surface = pygame.display.get_surface()
		self.font = pygame.font.Font('../font/LycheeSoda.ttf', 30)

		self.soil_layer = soil_layer
		self.mainLevel = mainLevel

		# options
		self.width = 400
		self.space = 10
		self.padding = 8
		self.mainMusic = mainMusic

		# volume
		self.musicVolume = musicVolume
		self.sfxVolume = sfxVolume
		# entries
		self.menu_list = ['Volume', 'SFX Volume', 'Save game', 'Load game', 'Exit', 'Exit and Save']
		self.setup()

		# movement
		self.index = 0
		self.timer = Timer(200)

	def setup(self):

		# create the text surfaces
		self.text_surfs = []
		self.total_height = 0

		for item in self.menu_list:
			text_surf = self.font.render(item, False, 'Black')
			self.text_surfs.append(text_surf)
			self.total_height += text_surf.get_height() + (self.padding * 2)

		self.total_height += (len(self.text_surfs) - 1) * self.space
		self.menu_top = SCREEN_HEIGHT / 2 - self.total_height / 2
		self.main_rect = pygame.Rect(
			SCREEN_WIDTH / 2 - self.width / 2, self.menu_top, self.width, self.total_height)

		# volume text surface
		
		self.musicVolume_plus = self.font.render(f'+', False, 'Black')
		self.musicVolume_minus = self.font.render(f'-', False, 'Black')

	def input(self):
		keys = pygame.key.get_pressed()
		self.timer.update()

		if keys[pygame.K_ESCAPE]:
			self.toggle_menu()

		if not self.timer.active:
			if keys[pygame.K_UP] or keys[pygame.K_w]:
				if (self.index > 0):
					self.index -= 1
				else:
					self.index = len(self.menu_list) - 1
				self.timer.activate()

			if keys[pygame.K_DOWN] or keys[pygame.K_s]:
				if (self.index < len(self.menu_list) - 1):
					self.index += 1
				else:
					self.index = 0
				self.timer.activate()
# ['Volume', 'Save game', 'Load game', 'Exit', 'Exit and Save']
			#  Volume
			if self.index == 0:
				if keys[pygame.K_LEFT] or keys[pygame.K_a]:
					if (self.musicVolume > 0):
						self.musicVolume -= 4
					else:
						self.musicVolume = 0
					self.setVolume()
					self.timer.activate()
				if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
					if (self.musicVolume < 100):
						self.musicVolume += 4
					else:
						self.musicVolume = 100
					self.setVolume()
					self.timer.activate()

			#  SFX Volume
			if self.index == 1:
				if keys[pygame.K_LEFT] or keys[pygame.K_a]:
					if (self.sfxVolume > 0):
						self.sfxVolume -= 4
					else:
						self.sfxVolume = 0
					self.setVolume()
					self.timer.activate()
				if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
					if (self.sfxVolume < 100):
						self.sfxVolume += 4
					else:
						self.sfxVolume = 100
					self.setVolume()
					self.timer.activate()

			# Save game
			if self.index == 2:
				if keys[pygame.K_ESCAPE] or keys[pygame.K_e]:
					self.player.saveGame()
					self.toggle_menu()

			# Load game
			if self.index == 3:
				if keys[pygame.K_ESCAPE] or keys[pygame.K_e]:
						# self.player.levelSetup()
						self.player.loadGame()
						self.toggle_menu()

			# Exit
			if self.index == 4:
				if keys[pygame.K_ESCAPE] or keys[pygame.K_e]:
						pygame.quit()
						sys.exit()

			# Exit and Save
			if self.index == 5:
				if keys[pygame.K_ESCAPE] or keys[pygame.K_e]:
					self.player.saveGame()
					self.toggle_menu()
					pygame.quit()
					sys.exit()
		

	def setVolume(self):
		self.mainMusic.set_volume(self.musicVolume/100)
		self.soil_layer.setSFXVolume(self.sfxVolume)
		self.player.setSFXVolume(self.sfxVolume)
		self.mainLevel.setSFXVolume(self.sfxVolume)
		self.updateShowVolume()

	def show_entry(self, text_surf, amount, top, selected):

		# background
		bg_rect = pygame.Rect(self.main_rect.left, top, self.width,
							  text_surf.get_height() + (self.padding * 2))
		pygame.draw.rect(self.display_surface, 'White', bg_rect, 0, 4)

		# text
		text_rect = text_surf.get_rect(
			midleft=(self.main_rect.left + 20, bg_rect.centery))
		self.display_surface.blit(text_surf, text_rect)
		
		# selected
		if selected:
			pygame.draw.rect(self.display_surface, 'black', bg_rect, 4, 4)
			if self.index == 0 or self.index == 1 :
				pos_rect_right = self.musicVolume_plus.get_rect(
					midleft=(self.main_rect.right - 75 + 56, bg_rect.centery))
				self.display_surface.blit(self.musicVolume_plus, pos_rect_right)
				pos_rect_left = self.musicVolume_minus.get_rect(
					midleft=(self.main_rect.right - 75 - 20, bg_rect.centery))
				self.display_surface.blit(self.musicVolume_minus, pos_rect_left)

	def update(self):
		self.input()

		for text_index, text_surf in enumerate(self.text_surfs):
			top = self.main_rect.top + text_index * \
				(text_surf.get_height() + (self.padding * 2) + self.space)
			amount_list = self.menu_list
			amount = amount_list[text_index]
			self.show_entry(text_surf, amount, top, self.index == text_index)
			self.updateShowVolume()

	def updateShowVolume(self):	
		# Volume
		self.musicVolume_text = self.font.render(f'{self.musicVolume}%', False, 'Black')
		bg_rect = pygame.Rect(self.main_rect.left, self.main_rect.top, self.width,
							  30 + (self.padding * 2))
		pos_rect = self.musicVolume_text.get_rect(
					midleft=(self.main_rect.right - 75, bg_rect.centery))
		self.display_surface.blit(self.musicVolume_text, pos_rect)

		self.sfxVolume_text = self.font.render(f'{self.sfxVolume}%', False, 'Black')
		sfx_bg_rect = pygame.Rect(self.main_rect.left, self.main_rect.top, self.width,
							  130 + (self.padding * 2))
		sfx_pos_rect = self.sfxVolume_text.get_rect(
					midleft=(self.main_rect.right - 75, sfx_bg_rect.centery))
		self.display_surface.blit(self.sfxVolume_text, sfx_pos_rect)

