import pygame

class Cell:
    def __init__(self, value, row, col, screen, locked):
        self.value = value
        self.sketched_value = 0
        self.row = row
        self.col = col
        self.screen = screen
        self.selected = False
        self.locked = locked

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        x = self.col * 70  # Replace 50 with the desired cell width
        y = self.row * 70  # Replace 50 with the desired cell height

        # Draw cell outline
        if self.selected:
            outline_color = (255, 0, 0)
        else:
            outline_color = (0, 0, 0)
        pygame.draw.rect(self.screen, outline_color, (x, y, 70, 70), 2)

        # Draw cell value
        font = pygame.font.Font(None, 40)
        if self.value != 0:
            text = font.render(str(self.value), True, (0, 0, 0))
            text_rect = text.get_rect(center=(x + 35, y + 35))  # Adjust center according to cell width and height
            self.screen.blit(text, text_rect)
        elif self.sketched_value != 0:
            text = font.render(str(self.sketched_value), True, (128, 128, 128))
            text_rect = text.get_rect(center=(x + 25, y + 25))  # Adjust center according to cell width and height
            self.screen.blit(text, text_rect)
