import pygame
from settings import *
from timer import Timer
import sys

menu_list = ['Volume', 'Save and Exit']


class MainMenu:
    def __init__(self, player, toggle_menu):

        # general setup
        self.player = player
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../font/LycheeSoda.ttf', 30)

        # options
        self.width = 400
        self.space = 10
        self.padding = 8

        # volume
        self.volume = 100

        # entries
        self.optionsItem = list(self.player.item_inventory.keys())
        self.optionsSeed = list(self.player.seed_inventory.keys())
        self.options = list(self.player.item_inventory.keys()) + \
            list(self.player.seed_inventory.keys())
        self.sell_border = len(self.player.item_inventory) - 1
        self.setup()

        # movement
        self.index = 0
        self.timer = Timer(50)

    def setup(self):

        # create the text surfaces
        self.text_surfs = []
        self.total_height = 0

        for item in menu_list:
            text_surf = self.font.render(item, False, 'Black')
            self.text_surfs.append(text_surf)
            self.total_height += text_surf.get_height() + (self.padding * 2)

        self.total_height += (len(self.text_surfs) - 1) * self.space
        self.menu_top = SCREEN_HEIGHT / 2 - self.total_height / 2
        self.main_rect = pygame.Rect(
            SCREEN_WIDTH / 2 - self.width / 2, self.menu_top, self.width, self.total_height)

        # volume text surface
        self.volume_text = self.font.render(f'{self.volume}%', False, 'Black')

    def input(self):
        self.timer.update()
        for event in pygame.event.get():
            if not self.timer.active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.toggle_menu()
                    elif event.key == pygame.K_DOWN:
                        self.index += 1
                        self.timer.activate()
                    elif event.key == pygame.K_UP:
                        self.index -= 1
                        self.timer.activate()

                if self.index == 0:
                    if event.key == pygame.K_LEFT:
                        self.volume -= 4
                        self.timer.activate()
                    if event.key == pygame.K_RIGHT:
                        self.volume += 4
                        self.timer.activate()
                
                if self.index == 1:
                    if event.key == pygame.K_SPACE:
                        pygame.quit()
                        sys.exit()

                if event.type == pygame.KEYUP:
                    pass
        if self.index >= len(menu_list):
            self.index -= 1
        if self.index < 0:
            self.index += 1

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
            if self.index == 0:
                pos_rect = self.volume_text.get_rect(
                    midleft=(self.main_rect.right - 75, bg_rect.centery))
                self.display_surface.blit(self.volume_text, pos_rect)

    def update(self):
        self.input()

        for text_index, text_surf in enumerate(self.text_surfs):
            top = self.main_rect.top + text_index * \
                (text_surf.get_height() + (self.padding * 2) + self.space)
            amount_list = list(self.player.item_inventory.values()) + \
                list(self.player.seed_inventory.values())
            amount = amount_list[text_index]
            self.show_entry(text_surf, amount, top, self.index == text_index)
