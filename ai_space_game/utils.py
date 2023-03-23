import pygame
from .settings import *

def toggle_fullscreen(screen, screen_width, screen_height):

    fullscreen = not fullscreen
    if fullscreen:
        screen = pygame.display.set_mode(
            (screen_width, screen_height), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((screen_width, screen_height))