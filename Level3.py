import pygame
import os
import tmx
import time

class Game(object):
    def main(self, screen):
        clock = pygame.time.Clock()
        
        background = pygame.image.load(os.path.join('data', 'Level3bg.png'))
        
        self.tilemap = tmx.load(os.path.join('data', 'tilemaps', 'platforms.tmx'), screen.get_size())
        
        self.sprites = tmx.SpriteLayer()
        start_cell = self.tilemap.layers['triggers'].find('player')[0]
        self.player = Player((start_cell.px, start_cell.py), self.sprites)
        self.tilemap.layers.append(self.sprites)
        
        while 1:
            dt = clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return False

            #screen.fill((200, 200, 200))
            self.tilemap.update(dt / 1000., self)
            screen.blit(background, (0, 0))
            self.tilemap.draw(screen)
            pygame.display.flip()
            
            if self.player.win:
                message_display('You did it!', screen)
                time.sleep(4)
                return True
            
class Player(pygame.sprite.Sprite):
    def __init__(self, location, *groups):
        super(Player, self).__init__(*groups)
        self.image = pygame.image.load(os.path.join('data', 'python-right.png'))
        self.image_right = self.image
        self.image_left = pygame.image.load(os.path.join('data', 'python-left.png'))
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.resting = False
        self.dy = 0
        self.facing = 1
        self.win = False
        
    def update(self, dt, game):
        last = self.rect.copy()
        
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rect.x -= 300 * dt
            self.facing = 0
        if key[pygame.K_RIGHT]:
            self.rect.x += 300 * dt
            self.facing = 1
        
        if self.facing == 0:
            self.image = self.image_left
        else:
            self.image = self.image_right
        
        if self.resting and key[pygame.K_SPACE]:
            self.dy = -750
        self.dy = min(400, self.dy + 40)
        
        self.rect.y += self.dy * dt
        
        new = self.rect
        self.resting = False
        for cell in game.tilemap.layers['triggers'].collide(new, 'blockers'):
            if last.right <= cell.left and new.right > cell.left:
                new.right = cell.left
            if last.left >= cell.right and new.left < cell.right:
                new.left = cell.right
            if last.bottom <= cell.top and new.bottom > cell.top:
                self.resting = True
                self.dy = 0
                new.bottom = cell.top
            if last.top >= cell.bottom and new.top < cell.bottom:
                self.dy = 0
                new.top = cell.bottom
        
        if 174 < new.x < 217 and 1205 < new.y < 1248:
            self.win = True
        
        game.tilemap.set_focus(new.x, new.y)
        #print('x:{}, y:{}'.format(new.x, new.y))

def text_objects(text, font):
    textSurface = font.render(text, True, (255,255,255))
    return textSurface, textSurface.get_rect()

def message_display(text, screen):
    largeText = pygame.font.Font('freesansbold.ttf',50)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((screen.get_width() / 2),\
                       (screen.get_height() / 2))
    screen.blit(TextSurf, TextRect)
    pygame.display.update()

def main(screen):
    Game().main(screen)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    Game().main(screen)
