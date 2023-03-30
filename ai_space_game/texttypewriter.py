import pygame

class TextTypewriter:
    def __init__(self, font, text, color, typing_speed):
        self.font = font
        self.text = text
        self.color = color
        self.typing_speed = typing_speed
        self.current_text = ""
        self.elapsed_time = 0
        self.current_index = 0

    def update(self, dt):
        self.elapsed_time += dt
        if self.elapsed_time >= 1000 / self.typing_speed:
            self.elapsed_time = 0
            if self.current_index < len(self.text):
                self.current_text += self.text[self.current_index]
                self.current_index += 1

    def draw(self, surface, x, y):
        rendered_text = self.font.render(self.current_text, True, self.color)
        surface.blit(rendered_text, (x, y))
