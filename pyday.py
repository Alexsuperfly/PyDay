"""
    PyDay Main Module
    Module launches main menu, then handles transitions between levels.
"""
import pygame
import Level1
import Level2
import Level3

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    
    print("LAUNCHING ULTRA ADVANCED MAIN MENU LEVEL 5 v.03")
    
    Level1.main(800, 600, screen)
    Level2.game_loop(screen)
    Level3.Game().main(screen)
    
    print("Thanks for playing :)")

