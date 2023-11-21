import pygame, sys
from settings import *
from level import Level
from level_load import Level_Load
from button import Button

# SCREEN = pygame.display.set_mode((1280, 720))
# pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
	return pygame.font.Font('../font/LycheeSoda.ttf', size)

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		pygame.display.set_caption('Pydew Valley - Nhom 8')
		self.musicVolume = 48
		self.sfxVolume = 20
		# self.level = Level()
		self.success = pygame.mixer.Sound('../audio/success.wav')
		self.success.set_volume(self.sfxVolume/100)
		self.music = pygame.mixer.Sound('../audio/menu_music.mp3')
		self.music.set_volume(self.musicVolume/100)
		self.music.play(loops=-1)

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			dt = self.clock.tick() / 1000
			self.level.run(dt)
			pygame.display.update()

	def options(self):
		
		def updateVolumeText():
			self.success.set_volume(self.sfxVolume/100)
			self.success.play()
			self.music.set_volume(self.musicVolume/100)
			Number_Volume_TEXT = get_font(45).render(str(self.musicVolume), True, "#835d43")
			Number_Volume_RECT = Number_Volume_TEXT.get_rect(center=(840, 250))
			self.screen.blit(Number_Volume_TEXT, Number_Volume_RECT)

			Number_SFXVolume_TEXT = get_font(45).render(str(self.sfxVolume), True, "#835d43")
			Number_SFXVolume_RECT = Number_SFXVolume_TEXT.get_rect(center=(840, 350))
			self.screen.blit(Number_SFXVolume_TEXT, Number_SFXVolume_RECT)

		while True:
			OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

			self.screen.blit(pygame.image.load("assets/Background - About.png"), (0, 0))

			OPTIONS_TEXT = get_font(75).render("OPTIONS", True, "#835d43")
			OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 100))
			self.screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

			Volume_TEXT = get_font(45).render("Volume", True, "#835d43")
			Volume_RECT = Volume_TEXT.get_rect(center=(500, 250))
			self.screen.blit(Volume_TEXT, Volume_RECT)

			Number_Volume_TEXT = get_font(45).render(str(self.musicVolume), True, "#835d43")
			Number_Volume_RECT = Number_Volume_TEXT.get_rect(center=(840, 250))
			self.screen.blit(Number_Volume_TEXT, Number_Volume_RECT)

			Volume_Inc = Button(image=None, pos=(880, 250), 
								text_input="+", font=get_font(60), base_color="Black", hovering_color="White")
			Volume_Inc.changeColor(OPTIONS_MOUSE_POS)
			Volume_Inc.update(self.screen)
			
			Volume_Dec = Button(image=None, pos=(800, 250), 
								text_input="-", font=get_font(60), base_color="Black", hovering_color="White")
			Volume_Dec.changeColor(OPTIONS_MOUSE_POS)
			Volume_Dec.update(self.screen)

			SFXVolume_TEXT = get_font(45).render("SFX Volume", True, "#835d43")
			SFXVolume_RECT = SFXVolume_TEXT.get_rect(center=(500, 350))
			self.screen.blit(SFXVolume_TEXT, SFXVolume_RECT)

			Number_SFXVolume_TEXT = get_font(45).render(str(self.sfxVolume), True, "#835d43")
			Number_SFXVolume_RECT = Number_SFXVolume_TEXT.get_rect(center=(840, 350))
			self.screen.blit(Number_SFXVolume_TEXT, Number_SFXVolume_RECT)

			SFXVolume_Inc = Button(image=None, pos=(880, 350), 
								text_input="+", font=get_font(60), base_color="Black", hovering_color="White")
			SFXVolume_Inc.changeColor(OPTIONS_MOUSE_POS)
			SFXVolume_Inc.update(self.screen)
			
			SFXVolume_Dec = Button(image=None, pos=(800, 350), 
								text_input="-", font=get_font(60), base_color="Black", hovering_color="White")
			SFXVolume_Dec.changeColor(OPTIONS_MOUSE_POS)
			SFXVolume_Dec.update(self.screen)

			OPTIONS_BACK = Button(image=None, pos=(640, 500), 
								text_input="BACK", font=get_font(75), base_color="Black", hovering_color="White")

			OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
			OPTIONS_BACK.update(self.screen)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
						Game.main_menu(self)
					if Volume_Dec.checkForInput(OPTIONS_MOUSE_POS):
						if (self.musicVolume > 0):
							self.musicVolume -= 4
						updateVolumeText()
					if Volume_Inc.checkForInput(OPTIONS_MOUSE_POS):
						if (self.musicVolume < 100):
							self.musicVolume += 4
						updateVolumeText()
					if SFXVolume_Dec.checkForInput(OPTIONS_MOUSE_POS):
						if(self.sfxVolume > 0):
							self.sfxVolume -= 4
						updateVolumeText()
					if SFXVolume_Inc.checkForInput(OPTIONS_MOUSE_POS):
						if(self.sfxVolume < 100):
							self.sfxVolume += 4
						updateVolumeText()

			pygame.display.update()
		

	def about(self):
		while True:
			About_MOUSE_POS = pygame.mouse.get_pos()

			# SCREEN.fill("white")
			self.screen.blit(pygame.image.load("assets/Background - About.png"), (0, 0))

			About_TEXT = get_font(75).render("ABOUT", True, "#835d43")
			About_RECT = About_TEXT.get_rect(center=(640, 100))
			self.screen.blit(About_TEXT, About_RECT)

			INFO_TEXT = get_font(30).render("This game is made by members of group 8", True, "#835d43")
			INFO_RECT = INFO_TEXT.get_rect(center=(640, 200))
			self.screen.blit(INFO_TEXT, INFO_RECT)

			TV1_TEXT = get_font(50).render("Tran Viet Dung", True, "#835d43")
			TV1_RECT = TV1_TEXT.get_rect(center=(640, 280))
			self.screen.blit(TV1_TEXT, TV1_RECT)

			TV2_TEXT = get_font(50).render("Nguyen Tung Duong", True, "#835d43")
			TV2_RECT = TV2_TEXT.get_rect(center=(640, 340))
			self.screen.blit(TV2_TEXT, TV2_RECT)

			TV3_TEXT = get_font(50).render("Lai Trung Lam", True, "#835d43")
			TV3_RECT = TV3_TEXT.get_rect(center=(640, 400))
			self.screen.blit(TV3_TEXT, TV3_RECT)

			TV4_TEXT = get_font(50).render("Ly Thanh Dat", True, "#835d43")
			TV4_RECT = TV4_TEXT.get_rect(center=(640, 460))
			self.screen.blit(TV4_TEXT, TV4_RECT)

			TV5_TEXT = get_font(50).render("Chu Tuan Nam", True, "#835d43")
			TV5_RECT = TV5_TEXT.get_rect(center=(640, 520))
			self.screen.blit(TV5_TEXT, TV5_RECT)

			About_BACK = Button(image=None, pos=(640, 600), 
								text_input="BACK", font=get_font(75), base_color="#cf936a", hovering_color="White")
			
			INFO2_TEXT = get_font(20).render("Referenced by CleanCode", True, "#91a155")
			INFO2_RECT = INFO2_TEXT.get_rect(center=(1160, 700))
			self.screen.blit(INFO2_TEXT, INFO2_RECT)

			About_BACK.changeColor(About_MOUSE_POS)
			About_BACK.update(self.screen)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if About_BACK.checkForInput(About_MOUSE_POS):
						Game.main_menu(self)

			pygame.display.update()


	def main_menu(self):
		is_in_game = False
		while True:
			if (is_in_game == False):
				self.screen.blit(BG, (0, 0))

				MENU_MOUSE_POS = pygame.mouse.get_pos()

				MENU_TEXT = get_font(60).render("MAIN MENU", True, "#aa7959")
				MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

				PLAY_NEW_BUTTON = Button(image=pygame.image.load("assets/BackgroundButton.png"), pos=(640, 200), 
									text_input="PLAY NEW GAME", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
				PLAY_LOAD_BUTTON = Button(image=pygame.image.load("assets/BackgroundButton.png"), pos=(640, 300), 
									text_input="LOAD SAVE GAME", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
				OPTIONS_BUTTON = Button(image=pygame.image.load("assets/BackgroundButton.png"), pos=(640, 400), 
									text_input="OPTIONS", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
				ABOUT_BUTTON = Button(image=pygame.image.load("assets/BackgroundButton.png"), pos=(640, 500), 
									text_input="ABOUT", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
				QUIT_BUTTON = Button(image=pygame.image.load("assets/BackgroundButton.png"), pos=(640, 600), 
									text_input="QUIT", font=get_font(40), base_color="#d7fcd4", hovering_color="White")

				self.screen.blit(MENU_TEXT, MENU_RECT)

				for button in [PLAY_NEW_BUTTON, PLAY_LOAD_BUTTON, OPTIONS_BUTTON, ABOUT_BUTTON, QUIT_BUTTON]:
					button.changeColor(MENU_MOUSE_POS)
					button.update(self.screen)
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if PLAY_NEW_BUTTON.checkForInput(MENU_MOUSE_POS):
						self.clock = pygame.time.Clock()
						self.music.stop()
						self.level = Level(self.musicVolume, self.sfxVolume)
						is_in_game = True
						while True:
							for event in pygame.event.get():
								if event.type == pygame.QUIT:
									pygame.quit()
									sys.exit()

							dt = self.clock.tick() / 1000
							self.level.run(dt)
							pygame.display.update()
					if PLAY_LOAD_BUTTON.checkForInput(MENU_MOUSE_POS):
						self.clock = pygame.time.Clock()
						self.music.stop()
						self.level = Level_Load(self.musicVolume, self.sfxVolume)
						is_in_game = True
						while True:
							for event in pygame.event.get():
								if event.type == pygame.QUIT:
									pygame.quit()
									sys.exit()

							dt = self.clock.tick() / 1000
							self.level.run(dt)
							pygame.display.update()
					if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
						Game.options(self)
					if ABOUT_BUTTON.checkForInput(MENU_MOUSE_POS):
						Game.about(self)
					if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
						pygame.quit()
						sys.exit()

			pygame.display.update()

if __name__ == '__main__':
	game = Game()
	game.main_menu()

