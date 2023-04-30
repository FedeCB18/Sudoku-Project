import pygame as pg

class Button:
    def __init__(self, x, y, width, height, text=None, color=None, text_color=(0, 0, 0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.text_color = text_color

    def draw(self, screen):
        pg.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        if self.text:
            font = pg.font.Font(None, 32)
            text = font.render(self.text, True, self.text_color)
            screen.blit(text, (self.x + (self.width - text.get_width()) // 2, self.y + (self.height - text.get_height()) // 2))

    def is_clicked(self, pos):
        x, y = pos
        if self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
            return True
        return False
