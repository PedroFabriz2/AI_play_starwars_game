from pygame.locals import *
import pygame
import random
import os

#pre-sets
pygame.font.init()
WIN_WIDTH = 800
WIN_HEIGHT = 490
STAT_FONT = pygame.font.SysFont("comicsans", 50)
#ROCKET = rocket_pos_x, rocket_pos_y, rocket_width, rocket_height = 50, 50, 50, 20
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
bb8_img = pygame.image.load(os.path.join("imgs","bb8.png")).convert_alpha()
bb8_evil_img = pygame.image.load(os.path.join("imgs","bb8_evil.png")).convert_alpha()
falcon_img = pygame.image.load(os.path.join("imgs","falcon_maior.png")).convert_alpha()

pygame.display.set_caption("Save bb8!")

class Falcon:
	IMG = falcon_img
	def __init__(self, x_pos, y_pos):
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.velocity = 5
		self.img = self.IMG

	def move(self, keys):
		if keys[pygame.K_UP]:
			if self.y_pos <= -35:
				self.y_pos = self.y_pos
			else:
				self.y_pos -= self.velocity

		if keys[pygame.K_DOWN]:
			if self.y_pos >= 465:
				self.y_pos = self.y_pos
			else:
				self.y_pos += self.velocity
		   		
	def draw(self, screen):
		screen.blit(self.IMG, (self.x_pos, self.y_pos))

	def get_mask(self):
		return pygame.mask.from_surface(self.img)

class BB8:
	IMG = bb8_img
	def __init__(self, x_pos):
		self.x_pos = x_pos
		self.height = 0
		self.velocityX = 3
		self.img = self.IMG

		self.update_height()

	def update_height(self):
		self.height = random.randrange(20, 450)

	def draw(self, screen):
		screen.blit(self.IMG, (self.x_pos, self.height))
		
	def move(self):
		self.x_pos -= self.velocityX

	def collide(self, falcon):
		falcon_mask = falcon.get_mask()
		bb8_mask = pygame.mask.from_surface(self.img)

		good_offset = (self.x_pos - falcon.x_pos, self.height - round(falcon.y_pos))

		f_point = falcon_mask.overlap(bb8_mask, good_offset)

		if f_point:
			return True

		return False

class evil_BB8:
	IMG = bb8_evil_img
	def __init__(self, x_pos):
		self.x_pos = x_pos
		self.height = 0
		self.velocityX = 5
		self.img = self.IMG

		self.update_height()

	def update_height(self):
		self.height = random.randrange(20, 450)

	def draw(self, screen):
		screen.blit(self.IMG, (self.x_pos, self.height))
		
	def move(self):
		self.x_pos -= self.velocityX

	def collide(self, falcon):
		falcon_mask = falcon.get_mask()
		bb8_evil_mask = pygame.mask.from_surface(self.img)

		bad_offset = (self.x_pos - falcon.x_pos, self.height - round(falcon.y_pos))

		f_point = falcon_mask.overlap(bb8_evil_mask, bad_offset)

		if f_point:
			return True

		return False

def Screen(screen, falcon, bb8, evil_bb8, score, die):
	screen.fill((0,0,0))
	keys = pygame.key.get_pressed()
	score_label = STAT_FONT.render("Score: " + str(score),1,(255,255,255))
	die_label = STAT_FONT.render("Die: " + str(die),1,(255,255,255))
	
	screen.blit(score_label, (WIN_WIDTH - score_label.get_width() - 10, 10))
	screen.blit(die_label, (10, 10))

	for bb8 in bb8:
		bb8.draw(screen)

	for evil in evil_bb8:
			evil.draw(screen)	
		
	falcon.draw(screen)
	falcon.move(keys)
	pygame.display.update()

def main(screen):
	falcon = Falcon(70, 50)

	evil_bb8 = []
	bb8 = []

	bb8.append(BB8(WIN_WIDTH))
	evil_bb8.append(evil_BB8(WIN_WIDTH))

	die = 0
	score = 0
	run = True
	while(run):

		for event in pygame.event.get():
		    if event.type==QUIT:
		        run = False

		if bb8[-1].x_pos <= WIN_WIDTH/2:
			bb8.append(BB8(WIN_WIDTH))

		if evil_bb8[-1].x_pos <= WIN_WIDTH/3:
			evil_bb8.append(evil_BB8(WIN_WIDTH))

		for bb8s in bb8:
			if bb8s.collide(falcon):
				bb8.remove(bb8s)
				score += 1
			if bb8s.x_pos <= 0:
				bb8.remove(bb8s)

			bb8s.move()

		for evil in evil_bb8:
			if evil.collide(falcon):
				evil_bb8.remove(evil)
				die += 1
			if evil.x_pos <= 0:
				evil_bb8.remove(evil)

			evil.move()

		print(len(bb8), len(evil_bb8))
		Screen(screen, falcon, bb8, evil_bb8, score, die) 	
	pygame.quit()

main(screen)

