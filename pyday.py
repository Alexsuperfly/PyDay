"""
    PyDay Main Module
    Module launches main menu, then handles transitions between levels.
"""
import pygame
import Level1
import Level2
import Level3
import os

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    pygame.mixer.music.load(os.path.join('data', '3.wav'))
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    
    print("LAUNCHING ULTRA ADVANCED MAIN MENU LEVEL 5 v.03")
    
    Level1.main(800, 600, screen)
    Level2.game_loop(screen)
    Level3.Game().main(screen)
    
    print("Thanks for playing :)")

