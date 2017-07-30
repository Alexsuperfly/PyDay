"""
Alexander Sumner
FSUID: acs14k
"""

import sys
import pygame
import os
from pygame.locals import *

global SCREEN_WIDTH 
SCREEN_WIDTH = 800

global SCREEN_HEIGHT
SCREEN_HEIGHT = 600

global ROW_COOLDOWN
ROW_COOLDOWN = 30


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

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_png("character.png")
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.speed = 10
		self.state = "still"
		self.movepos = [0,0]
		self.rect.midbottom = self.area.midbottom

	def update(self):
		newpos = self.rect.move(self.movepos)
		if self.area.contains(newpos):
			self.rect = newpos
		pygame.event.pump()

	def moveup(self):
		self.movepos[1] = self.movepos[1] - self.speed
		self.state = "moveup"

	def movedown(self):
		self.movepos[1] = self.movepos[1] + self.speed
		self.state = "movedown"

	def moveleft(self):
		self.movepos[0] = self.movepos[0] - self.speed
		self.state = "moveleft"

	def moveright(self):
		self.movepos[0] = self.movepos[0] + self.speed
		self.state = "moveright"


class block(pygame.sprite.Sprite):
	def __init__(self, xpos):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_png("block.png")
		self.movepos = [0,5]
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.rect.left = xpos
		self.rect.top = 0

	def update(self):
		newpos = self.rect.move(self.movepos)
		if self.area.contains(newpos):
			self.rect = newpos
		pygame.event.pump()


class Row(object):
	def __init__(self, glocation, gsize):
		self.myblocks = pygame.sprite.Group()
		self.speed = 5
		self.gaplocation = glocation
		self.gapsize = gsize
		self.yposition = 0
		for x in range(0,SCREEN_WIDTH,20):
			if x < glocation or x > (glocation+gsize):
				self.myblocks.add(block(x))

	def moverow(self):
		self.yposition = self.yposition + self.speed
		for each in self.myblocks:
			each.movedown(self.speed)

	def update(self):
		if (self.yposition + 20) < SCREEN_HEIGHT:
			self.myblocks.update()
			self.yposition = self.yposition + 5
			return 0
		else:
			self.myblocks.empty()
			return 1

	def draw(self,screen):
		self.myblocks.draw(screen)

	def clear(self, screen, background):
		self.myblocks.clear(screen,background)



def main():
	#Initialize system
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
	pygame.display.set_caption("Level 1")
	clock = pygame.time.Clock()

	#Create background
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((0, 0, 0))

	#Create player
	global player
	player = Player()

	global rows
	rows = []

	global NUMROWS
	NUMROWS = 5

	global rowcooldown
	rowcooldown = ROW_COOLDOWN

	#Initialize sprites
	playersprite = pygame.sprite.RenderPlain(player)

	#Initial blit to screen
	screen.blit(background, (0,0))


	#The event loop
	while 1:
		#max the fps at 60
		clock.tick(50)

		if rowcooldown:
			rowcooldown = rowcooldown -1
		else:
			rows.append(Row(400,60))
			rowcooldown = ROW_COOLDOWN

		for event in pygame.event.get():
			if event.type == QUIT:
				return
			elif event.type == KEYDOWN:
				if event.key == K_UP:
					player.moveup()
				if event.key == K_DOWN:
					player.movedown()
				if event.key == K_LEFT:
					player.moveleft()
				if event.key == K_RIGHT:
					player.moveright()
			elif event.type == KEYUP:
				if event.key == K_UP or event.key == K_DOWN or event.key == K_LEFT or event.key == K_RIGHT:
					player.movepos = [0,0]
					player.state = "still"

		#fill old areas with background again
		screen.blit(background, player.rect, player.rect)
		for each in rows:
			each.clear(screen, background)
		
		#move the assets
		playersprite.update()
		for each in rows:
			if each.update():
				rows.remove(each)

		#draw the assets
		playersprite.draw(screen)
		for each in rows:
			each.draw(screen)
		
		#re draw the whole board
		pygame.display.flip()


if __name__ == "__main__": main()