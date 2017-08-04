"""
Alexander Sumner
FSUID: acs14k
"""

import time
import pygame
import os
import random
from pygame.locals import *

#global SCREEN_WIDTH 
#SCREEN_WIDTH = 800

#global SCREEN_HEIGHT
#SCREEN_HEIGHT = 600

global ROW_COOLDOWN
ROW_COOLDOWN = 32

random.seed()


def load_png(name):
	fullname = os.path.join("data", name)
	image = pygame.image.load(fullname)
	if image.get_alpha() is None:
		image = image.convert()
	else:
		image = image.convert_alpha()
	return image, image.get_rect()

class Player(pygame.sprite.Sprite):
	"""A player object that the user will move across the screen"""

	def __init__(self, width, height):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_png("character.png")
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.speed = 12
		self.state = "falling"
		self.movepos = [0,5]
		self.rect.midtop = self.area.midtop
		self.rect.top = self.rect.top + 10
		self.screenwidth = width
		self.screenheight = height

	def update(self):
		newpos = self.rect.move(self.movepos)
		if self.area.contains(newpos):
			self.rect = newpos
		pygame.event.pump()

	def moveleft(self):
		self.movepos[0] = self.movepos[0] - self.speed
		self.state = "moveleft"

	def moveright(self):
		self.movepos[0] = self.movepos[0] + self.speed
		self.state = "moveright"

	def dead(self):
		if self.rect.top < 1:
			return 1
		else:
			return 0

	def win(self):
		if self.rect.bottom > (self.screenheight - 6):
			return 1
		else:
			return 0


class block(pygame.sprite.Sprite):
	def __init__(self, xpos, height):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_png("block.png")
		self.screenheight = height
		self.movepos = [0,-4]
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.rect.left = xpos
		self.rect.top = self.screenheight - 20

	def update(self):
		newpos = self.rect.move(self.movepos)
		if self.area.contains(newpos):
			self.rect = newpos
		pygame.event.pump()


class Row(object):
	def __init__(self, glocation, gsize, width, height):
		self.myblocks = pygame.sprite.Group()
		self.screenwidth = width
		self.screenheight = height
		self.speed = 4
		self.gaplocation = glocation
		self.gapsize = gsize
		self.yposition = self.screenheight - 20
		for x in range(0,self.screenwidth,20):
			if x < glocation or x > (glocation+gsize):
				self.myblocks.add(block(x, self.screenheight))

	def update(self):
		if (self.yposition > 0):
			self.myblocks.update()
			self.yposition = self.yposition - self.speed
			return 0
		else:
			self.myblocks.empty()
			return 1

	def draw(self,screen):
		self.myblocks.draw(screen)

	def clear(self, screen, background):
		self.myblocks.clear(screen,background)

def text_objects(text, font):
    textSurface = font.render(text, True, (255,255,255))
    return textSurface, textSurface.get_rect()

def message_display(text, screen, width, height):
    textsize = int(height / 10)
    largeText = pygame.font.Font('freesansbold.ttf',textsize)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((width/2),(height/2))
    screen.blit(TextSurf, TextRect)
    pygame.display.update()

def gen_random_gap(width):
	gaplocation = random.randint(50,(width-100))
	gapsize = random.randint(70,80)
	return (gaplocation,gapsize)

    
def main(width = 800, height = 600, screen = None):
	#Initialize system
	pygame.init()

	SCREEN_WIDTH = width
	SCREEN_HEIGHT = height

	if screen == None:
		screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
	pygame.display.set_caption("Level 1")
	clock = pygame.time.Clock()

	#Create background
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((0, 0, 0))

	#Create player
	global player
	player = Player(SCREEN_WIDTH, SCREEN_HEIGHT)

	global rows
	rows = []

	global rowcooldown
	rowcooldown = 10

	global failed
	failed = 0

	#Initialize sprites
	playersprite = pygame.sprite.RenderPlain(player)

	#Initial blit to screen
	screen.blit(background, (0,0))


	#The event loop
	while 1:
		#max the fps at 60
		clock.tick(60)

		#if they lost break out of the loop and set failed to 1 to indicate a restart
		if player.dead():
			message_display('You Failed, Try Again ',screen, SCREEN_WIDTH, SCREEN_HEIGHT)
			time.sleep(3)
			#pygame.event.clear()
			failed = 1
			break

		#if they won close the game
		if player.win():
			message_display('You Succeeded', screen, SCREEN_WIDTH, SCREEN_HEIGHT)
			time.sleep(3)
			pygame.event.clear()
			pygame.event.post(pygame.event.Event(QUIT))

		#how many frames to wait untill we make another row
		if rowcooldown:
			rowcooldown = rowcooldown -1
		else:
			gloc,gsize = gen_random_gap(SCREEN_WIDTH)
			rows.append(Row(gloc,gsize,SCREEN_WIDTH, SCREEN_HEIGHT))
			rowcooldown = ROW_COOLDOWN

		#the event queue
		for event in pygame.event.get():
			if event.type == QUIT:
				return
			elif event.type == KEYDOWN:
				if event.key == K_LEFT:
					player.moveleft()
				if event.key == K_RIGHT:
					player.moveright()
			elif event.type == KEYUP:
				if event.key == K_LEFT or event.key == K_RIGHT:
					player.movepos = [0,5]
					player.state = "falling"

		

		#fill old areas with background again
		screen.blit(background, player.rect, player.rect)
		for each in rows:
			each.clear(screen, background)
		
		#move the assets
		playersprite.update()
		for each in rows:
			if each.update():
				rows.remove(each)

		#collision detection
		for row in rows:
			for block in row.myblocks:
				if player.rect.colliderect(block.rect):
					if (block.rect.top + 11) >= player.rect.bottom:
						player.rect.bottom = block.rect.top


		#draw the assets
		playersprite.draw(screen)
		for each in rows:
			each.draw(screen)
		
		#re draw the whole board
		pygame.display.flip()

	#restart the game since they failed last time
	if failed == 1:
		main(SCREEN_WIDTH,SCREEN_HEIGHT,screen)


if __name__ == "__main__": main(1200,800)