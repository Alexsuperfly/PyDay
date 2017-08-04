import pygame
import os
import time
import random

"""Level for PyDay: Survive The Semester"""

#pygame

class Background(pygame.sprite.Sprite):

    def __init__(self, image_file, location):

        pygame.sprite.Sprite.__init__(self)  
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

def gpablip(gameDisplay, x,y):
    gameDisplay.blit(gpaIMG,(x,y))



# falling object funtions
def things(gameDisplay, thingx, thingy, thingw, thingh, color):
     gameDisplay.blit(color,(thingx,thingy))

def things2(gameDisplay, thingx, thingy, thingw, thingh, color):
     gameDisplay.blit(color,(thingx,thingy))     

def things3(gameDisplay, thingx, thingy, thingw, thingh, color):
    gameDisplay.blit(color,(thingx,thingy)) 

def things4(gameDisplay,thingx, thingy, thingw, thingh, color):
    gameDisplay.blit(color,(thingx,thingy))              
    
def things5(gameDisplay, thingx, thingy, thingw, thingh, color):
    gameDisplay.blit(color,(thingx,thingy))     

#Message Support
def text_objects(text, font):

    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(gameDisplay, text):
    largeText = pygame.font.Font('freesansbold.ttf',50)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((gameDisplay.get_width()/2),(gameDisplay.get_height()/2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    pygame.draw.rect(gameDisplay, black, [5, 10, 150, 25])
    scoretext = myfont.render("GRADE: "+str(score), 1, (0, 255, 17))
    gameDisplay.blit(scoretext, (5, 10))
    time.sleep(2)
    game_loop(display_width,display_height)


def win_display(gameDisplay, text):
    largeText = pygame.font.Font('freesansbold.ttf',50)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((gameDisplay.get_width()/2),(gameDisplay.get_height()/2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    pygame.draw.rect(gameDisplay, black, [5, 10, 150, 25])
    scoretext = myfont.render("GRADE: "+str(score), 1, (0, 255, 17))
    gameDisplay.blit(scoretext, (5, 10))
    time.sleep(1)

    
# Main Game functiona
def Fail(gameDisplay):
    message_display(gameDisplay, 'You Failed Python. ')


def win(gameDisplay):
    win_display(gameDisplay, 'You survived the semester!')   


    
def game_loop(gameDisplay):

    """
    pygame.init()
    pygame.mixer.pre_init(44100,16,2,4096)
    """
    
    #global display_width
    display_width = gameDisplay.get_width()
    #global display_height
    display_height = gameDisplay.get_height()
    

    #display settings

    global black
    black = (0,0,0)

    white = (255,255,255)
    red = (255,0,0)
    gpa_width = 73
    #global gameDisplay
    #gameDisplay = pygame.display.set_mode((display_width,display_height))

    pygame.display.set_caption('Pass Python')
    clock = pygame.time.Clock()

    #score
    global score
    score = 0


    # imported images
    global gpaIMG
    gpaIMG = pygame.image.load(os.path.join('data', 'gpa.png'))
    AImg = pygame.image.load(os.path.join('data', 'goodgrade.png'))
    BImg = pygame.image.load(os.path.join('data', 'badgrade.png'))
    StackImg = pygame.image.load(os.path.join('data', 'stack.png'))
    brimg = pygame.image.load(os.path.join('data', 'idk.png'))

    imagelst = []
    imagelst.append(AImg)      
    imagelst.append(BImg) 
    test = []
    test.append(AImg)      
    test.append(BImg) 
    test.append(StackImg)

    #music and sounds
    pygame.mixer.music.load(os.path.join('data', '3.wav'))
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    gotA = pygame.mixer.Sound(os.path.join('data', 'Pickup_04.wav'))
    gotF = pygame.mixer.Sound(os.path.join('data', 'Explosion_02.wav'))

    #basic graphic support
    global myfont
    myfont = pygame.font.SysFont("monospace", 35)


    score = 100
    x = (display_width * 0.45)
    y = (display_height * 0.8)

    #has an object fallen?
    drop1 = True
    drop2 = True
    drop3 = True
    drop4 = True
    drop5 = True

    x_change = 0

    #falling object settings
    thing_startx = random.randrange(0, display_width - 50)
    thing_starty = -600
    thing_speed = 12
    thing_width = 100
    thing_height = 100

    thing_startx2 = random.randrange(0, display_width - 50)
    thing_starty2 = -600
    thing_speed2 = 7
    thing_width2 = 100
    thing_height2 = 100

    thing_startx3 = random.randrange(0, display_width - 50)
    thing_starty3 = -600
    thing_speed3 = 9
    thing_width3 = 100
    thing_height3 = 100

    thing_startx4 = random.randrange(0, display_width - 50)
    thing_starty4 = -600
    thing_speed4 = 25
    thing_width4 = 100
    thing_height4 = 100

    thing_startx5 = random.randrange(0, display_width - 50)
    thing_starty5 = -600
    thing_speed5 = 20
    thing_width5 = 100
    thing_height5 = 100

    gameExit = False

    #What Grade to display?
    rnd = random.choice(imagelst)
    rnd2 = StackImg
    rnd3 = random.choice(imagelst)
    rnd4 = BImg
    rnd5 = BImg

    BackGround = Background(os.path.join('data', 'b.png'), [0,0])



    #game loop
    while not gameExit:

        #basic controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -30
                if event.key == pygame.K_RIGHT:
                    x_change = 30

        x += x_change
        gameDisplay.fill([255, 255, 255])
        gameDisplay.blit(BackGround.image, BackGround.rect)

        #Game logic
        things(gameDisplay, thing_startx, thing_starty, thing_width, thing_height, rnd)
        thing_starty += thing_speed
        things2(gameDisplay, thing_startx2, thing_starty2, thing_width2, thing_height2, rnd2)
        thing_starty2+= thing_speed2
        things3(gameDisplay, thing_startx3, thing_starty3, thing_width3, thing_height3, rnd3)
        thing_starty3+= thing_speed3
        things4(gameDisplay, thing_startx4, thing_starty4, thing_width4, thing_height4, rnd4)
        thing_starty4+= thing_speed4
        things5(gameDisplay, thing_startx5, thing_starty5, thing_width5, thing_height5, rnd5)
        thing_starty5+= thing_speed5

        gpablip(gameDisplay, x,y)

        #cant leave game borders
        if x > display_width - gpa_width :
            x  =  0 

        elif x < 0:
            x = display_width - gpa_width

        #drop objects
        if thing_starty > display_height:
            rnd = random.choice(imagelst)
            rnd2 = random.choice(imagelst)
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0,display_width-50)
            drop1 = True
 

        if thing_starty2 > display_height:
            rnd2 = StackImg
            thing_starty2 = 0 - thing_height2
            thing_startx2 = random.randrange(0,display_width-50)
            drop2 = True


        if thing_starty3 > display_height:
            rnd3 = random.choice(imagelst)
            thing_starty3 = 0 - thing_height3
            thing_startx3 = random.randrange(0,display_width-50)   
            drop3 = True 

        if thing_starty4 > display_height:
            thing_starty4 = 0 - thing_height4
            thing_startx4 = random.randrange(0,display_width-50)   
            drop4 = True     

        if thing_starty5 > display_height:
            thing_starty5 = 0 - thing_height5
            thing_startx5 = random.randrange(0,display_width-50)   
            drop5 = True 

        #collide logic
        if y < thing_starty+thing_height -75:

            if x  > thing_startx and x  < thing_startx + thing_width or x+gpa_width > thing_startx and x + gpa_width < thing_startx+thing_width:
               
                if drop1:
                    if rnd == BImg:
                        score-=75
                        gotF.play()
                    else:  
                        gotA.play()
                        score+=60
                    drop1 = False   

        if y < thing_starty2+thing_height2 -75:      

            if x  > thing_startx2 and x  < thing_startx2 + thing_width2 or x+gpa_width > thing_startx2 and x + gpa_width < thing_startx2+thing_width2:
                
                if drop2:
                    if rnd2 == BImg:
                        gotF.play()
                        score-=75
                    else:  
                        gotA.play()
                        score+=60
                    drop2 = False 
                               
        if y < thing_starty3+thing_height3 -75:

            if x  > thing_startx3 and x  < thing_startx3 + thing_width3 or x+gpa_width > thing_startx3 and x + gpa_width < thing_startx3+thing_width3:
  
                if drop3:
                    if rnd3 == BImg:
                        gotF.play()
                        score-=75
                    else:  
                        gotA.play()
                        score+=60 
                    drop3 = False 

        if y < thing_starty4+thing_height4 -75:
  
            if x  > thing_startx4 and x  < thing_startx4 + thing_width4 or x+gpa_width > thing_startx4 and x + gpa_width < thing_startx4+thing_width4:
          
                if drop4:
                    gotF.play()
                    score-=75
                    drop4 = False 
            


        if y < thing_starty5+thing_height5 -75:

            if x  > thing_startx5 and x  < thing_startx5 + thing_width5 or x+gpa_width > thing_startx5 and x + gpa_width < thing_startx5+thing_width5:

                if drop5:
                    gotF.play()
                    score-=75
                    drop5= False 
         

        #update score 
        pygame.draw.rect(gameDisplay, black, [5, 10, 150, 25])

        scoretext = myfont.render("GRADE: "+str(score), 1, (0, 255, 17))
        gameDisplay.blit(scoretext, (5, 10))
   

        if score < 0:
         
            Fail(gameDisplay)
        elif score >=500:
            #loses.play()
            win(gameDisplay)
            gameExit = True

                           
        pygame.display.update()
        clock.tick(120)


if __name__ == '__main__':
    game_loop(800,600)
    pygame.quit()
    quit()
