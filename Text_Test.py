# Text_Test.py

import pygame

import constants
import game_objects
pygame.init()

output = input("Enter text to display: ")

size = [100,50]

# Screen variable, which solution is drawn to
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Text_Test")

game_objects.Console.draw_text(None, screen, output, (0,0))
pygame.display.flip()
input("Press Enter to continue: ")

game_objects.Console.draw_text_red(None, screen, output, (0,0))
pygame.display.flip()
input("Press Enter to continue: ")

game_objects.Console.draw_text_highlight(None, screen, output, (0,0))
pygame.display.flip()
input("Press Enter to Quit: ")
