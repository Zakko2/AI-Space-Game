import pygame
from ai_space_game.settings import *

def toggle_fullscreen(screen, windowed_width, windowed_height):
    # Get the current screen flags and toggle the fullscreen flag
    flags = screen.get_flags()
    fullscreen_flag = pygame.FULLSCREEN
    new_flags = flags ^ fullscreen_flag

    # Check if the new screen mode is fullscreen or windowed
    is_fullscreen = new_flags & fullscreen_flag

    # Set the new screen dimensions based on the new mode
    if is_fullscreen:
        info = pygame.display.Info()
        new_width, new_height = info.current_w, info.current_h
    else:
        new_width, new_height = windowed_width, windowed_height

    # Create a new screen with the new flags and dimensions
    new_screen = pygame.display.set_mode((new_width, new_height), new_flags)

    return new_screen