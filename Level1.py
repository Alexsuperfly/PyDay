"""
Alexander Sumner
FSUID: acs14k
"""

import sys
import pygame
import os

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
		self.reinit()
		self.movepos = [0,0]
		self.rect.midbottom = self.area.midbottom

	def update(self):
		newpos = self.rect.move(self.movepos)
		if self.area.contains(newpos):
			self.rect = newpos
		pygame.event.pump()

	def moveup(self):
        self.movepos[1] = self.movepos[1] - (self.speed)
        self.state = "moveup"

    def movedown(self):
    	self.movepos[1] = self.movepos[1] + (self.speed)
        self.state = "movedown"

	def moveleft(self):
		self.movepos[0] = self.movepos[0] - (self.speed)
        self.state = "moveleft"

	def moveright(self):
		self.movepos[0] = self.movepos[0] + (self.speed)
        self.state = "moveright"





#class Row(object):


def main():
	#Initialize screen
	pygame.init()
	screen = pygame.display.set_mode((800,600))
	pygame.display.set_caption("Level 1")

	#Create background
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((0, 0, 0))

	#Create player
	global player
	player = Player()

	#Initialize sprites
	playersprite = pygame.sprite.RenderPlain(player)

	#Initial blit to screen
	screen.blit(background, (0,0))
	pygame.display.flip()

	#Initialize clock
	clock = pygame.time.Clock()

	#The event loop
	while 1:
		#max the fps at 60
		clock.tick(60)

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
		playersprite.update()
		playersprite.draw(screen)
		pygame.display.flip()


if __name__ == "__main__": main()