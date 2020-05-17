from pygame.locals import *
import pygame
import random
import os
import neat

#pre-sets
pygame.font.init()
WIN_WIDTH = 800
WIN_HEIGHT = 490
STAT_FONT = pygame.font.SysFont("comicsans", 50)
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
gen = 0
bb8_img = pygame.image.load(os.path.join("imgs","bb8.png")).convert_alpha()
falcon_img = pygame.image.load(os.path.join("imgs","falcon_maior.png")).convert_alpha()

pygame.display.set_caption("Save bb8!")

class Falcon:
	IMG = falcon_img
	def __init__(self, x_pos, y_pos):
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.velocity = 5
		self.img = self.IMG

	def move(self, move_to):
		if move_to == 1:
			if self.y_pos <= -35:
				self.y_pos = self.y_pos
			else:
				self.y_pos -= self.velocity
		elif move_to == 0:
			if self.y_pos >= 465:
				self.y_pos = self.y_pos
			else:
				self.y_pos += self.velocity
		else:
			self.y_pos = self.y_pos

		   		
	def draw(self, screen):
		screen.blit(self.IMG, (self.x_pos, self.y_pos))

	def get_mask(self):
		return pygame.mask.from_surface(self.img)

class BB8:
	IMG = bb8_img
	def __init__(self, x_pos):
		self.x_pos = x_pos
		self.height = 0
		self.velocityX = 4
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

def Screen(screen, falcons, bb8, gen, score):
	screen.fill((0,0,0))
	keys = pygame.key.get_pressed()
	score_label = STAT_FONT.render("Generation: " + str(gen),1,(255,255,255))
	hm_label = STAT_FONT.render("Alive: " + str(len(falcons)),1,(255,255,255))
	
	screen.blit(score_label, (WIN_WIDTH - score_label.get_width() - 10, 10))
	screen.blit(hm_label, (10, 10))
	
	
	win_label = STAT_FONT.render("Score: " + str(score),1,(255,255,255))
	screen.blit(win_label, (10, 50))

	
	for bb8s in bb8:
		bb8s.draw(screen)	

	for falcon in falcons:
		falcon.draw(screen)
		#falcon.move(keys)
	pygame.display.update()


def main(genomes, config):
	nets = []
	ge = []
	falcons = [] #Falcon(70, 50)
	score = 0

	global WIN, gen
	screen = WIN
	gen += 1

	for _, g in genomes:
		net = neat.nn.FeedForwardNetwork.create(g, config)
		nets.append(net)
		falcons.append(Falcon(70, 50))
		g.fitness = 0
		ge.append(g)

	bb8 = []

	bb8.append(BB8(WIN_WIDTH))

	run = True
	while(run):

		for event in pygame.event.get():
		    if event.type==QUIT:
		        run = False
		        pygame.quit()
		        quit()

		bb8_ind = 0
		if len(falcons) > 0:
			if len(bb8) > 1 and bb8[0].x_pos < falcons[0].x_pos:
				bb8_ind = 1
		else:
			run = False
			break

		for x, falcon in enumerate(falcons):
			falcon.move(-1)
			
			output = nets[x].activate((abs(falcon.x_pos - bb8[bb8_ind].x_pos), abs(falcon.y_pos - bb8[bb8_ind].height)))
			if output[0] >= 0:
				falcon.move(1)
			else:
				falcon.move(0)


		if bb8[-1].x_pos <= WIN_WIDTH/2:
			bb8.append(BB8(WIN_WIDTH))

		add_score = False
		rem = []
		for bb8s in bb8:

			bb8s.move()
			for x, falcon in enumerate(falcons):
				if bb8s.collide(falcon):
					ge[x].fitness += 2
					bb8.remove(bb8s)
					add_score = True
					break
					
			if bb8s.x_pos < falcon.x_pos:
				add_score = False
				rem.append(bb8s)
			
			for x, falcon in enumerate(falcons):
				if falcon.y_pos <= -35 or falcon.y_pos >= 465:
					falcons.pop(x)
					nets.pop(x)
					ge[x].fitness -= 1
					ge.pop(x)

			for r in rem:
				bb8.remove(r)

			if add_score:
				score += 1

		Screen(WIN, falcons, bb8, gen, score) 	
	

def run(config):
	config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config)
	#this sets our population as our config file tells to
	p = neat.Population(config)

	#add some reporters to report data
	p.add_reporter(neat.StdOutReporter(True))
	stats = neat.StatisticsReporter()
	p.add_reporter(stats)

	winner = p.run(main, 50)#total of 50 generations of species
	print('\nBest genome:\n{!s}'.format(winner))

if __name__ == '__main__':

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config_file.txt')
    run(config_path)

