import pygame

pygame.init()

#game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Health Bar')

class HealthBar():
  def __init__(self, x, y, w, h, hp):
    self.x = x
    self.y = y
    self.w = w
    self.h = h
    self.hp = hp
    self.max_hp = 100

  def draw(self, surface):
    #calculate health ratio
    ratio = self.hp / self.max_hp
    pygame.draw.rect(surface, "red", (self.x, self.y, self.w, self.h))
    pygame.draw.rect(surface, "green", (self.x, self.y, self.w * ratio, self.h))

health_bar = HealthBar(250, 200, 30, 4, 70)

run = True
while run:

  screen.fill("indigo")

  #draw health bar
  health_bar.draw(screen)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  pygame.display.flip()

pygame.quit()