import pygame
from ai_space_game.settings import *

class Sound:
    def __init__(self, sound_path, volume=1.0):
        self.sound = pygame.mixer.Sound(sound_path)
        self.sound.set_volume(volume)

    def play(self):
        self.sound.play()

    def set_volume(self, volume):
        self.sound.set_volume(volume)