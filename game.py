from pygame.locals import *
import pygame
import random
import os

#pre-sets
pygame.font.init()
WIN_WIDTH = 800
WIN_HEIGHT = 450
STAT_FONT = pygame.font.SysFont("comicsans", 50)
#ROCKET = rocket_pos_x, rocket_pos_y, rocket_width, rocket_height = 50, 50, 50, 20
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
bb8_img = pygame.image.load(os.path.join("imgs","bb8.png")).convert_alpha()
falcon_img = pygame.image.load(os.path.join("imgs","falcon_maior.png")).convert_alpha()

pygame.display.set_caption("Save bb8!")

class Falcon:
	IMG = falcon_img
	def __init__(self, x_pos, y_pos):
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.velocity = 4

	def move(self, keys):
		if keys[pygame.K_UP]:
   			self.y_pos -= self.velocity
		if keys[pygame.K_DOWN]:
		   	self.y_pos += self.velocity
		   		
	
	def draw(self, screen):
		screen.blit(self.IMG, (self.x_pos, self.y_pos))

class BB8:
	IMG = bb8_img
	def __init__(self, x_pos):
		self.x_pos = x_pos
		self.height = 0
		self.velocityX = 3

		self.update_height()

	def update_height(self):
		self.height = random.randrange(20, 330)

	def draw(self, screen):
		screen.blit(self.IMG, (self.x_pos, self.height))

	def move(self):
		self.x_pos -= self.velocityX

def Screen(screen, falcon, bb8, score):
	screen.fill((0,0,0))
	keys = pygame.key.get_pressed()

	score_label = STAT_FONT.render("Score: " + str(score),1,(255,255,255))
	screen.blit(score_label, (WIN_WIDTH - score_label.get_width() - 10, 10))

	for bb8 in bb8:
		bb8.draw(screen)
		

	falcon.draw(screen)
	falcon.move(keys)
	pygame.display.update()

def main(screen):
	falcon = Falcon(70, 50)
	
	bb8 = []
	bb8.append(BB8(WIN_WIDTH))
	score = 0

	run = True
	while(run):

		for event in pygame.event.get():
		    if event.type==QUIT:
		        run = False

		if bb8[-1].x_pos <= WIN_WIDTH/2:
			bb8.append(BB8(WIN_WIDTH))

		for bb8s in bb8:
			bb8s.move()

			if bb8s.x_pos <= 90:
				bb8.remove(bb8s)
				score += 1

		Screen(screen, falcon, bb8, score)
	   
	pygame.quit()


main(screen)




