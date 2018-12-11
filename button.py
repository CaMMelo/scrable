import pygame as p


class Button:

    def __init__(self, x, y, w, h, text, font, color=(255, 255, 255)):
        self.rect = p.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.font = font
    
    def draw(self, surface):
        text = self.font.render(self.text, True, (250,250,250))

        x = self.rect.x + self.rect.w // 2 - text.get_width()//2
        y = self.rect.y + self.rect.h // 2 - text.get_height()//2

        p.draw.rect(surface, self.color, self.rect)
        surface.blit(text, (x, y))
        
    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            return True
        else:
            return False
        