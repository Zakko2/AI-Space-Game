import pygame.mixer


class Music:
    def __init__(self, music_file, volume=1.0):
        pygame.mixer.init()
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.set_volume(volume)

    def play(self, loop=-1):
        pygame.mixer.music.play(loop)

    def stop(self):
        pygame.mixer.music.stop()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def get_volume(self):
        return pygame.mixer.music.get_volume()

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()

    def fadeout(self, milliseconds):
        pygame.mixer.music.fadeout(milliseconds)

    @staticmethod
    def quit():
        pygame.mixer.quit()