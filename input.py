import pygame as p
import re

color_inactive = (190,190,190)
color_active = (250,250,250)


class Input:
	
    def __init__(self, x, y, w, h, label='', color=color_inactive):

        self.rect = p.Rect(x, y, w, h)
        self.active = False
        self.value = ''
        self.color = color
        self.label = label
    
    def atualiza_ativo(self, pos):
        if self.rect.collidepoint(pos):
            self.active = not self.active
            self.color = color_active if self.active else color_inactive
        else:
            self.active = False
            self.color = color_inactive
    
    def draw(self, surface, font):
        
        txt = font.render(self.value, True, self.color)
        surface.blit(txt, (self.rect.x + 10, self.rect.y + 5))

        txt = font.render(self.label, True, self.color)
        surface.blit(txt, (self.rect.x - 30, self.rect.y + 5))

        p.draw.rect(surface, self.color, self.rect, 2)
    
    def atualiza_valor(self, key, unicode):
    	pass


class InputNum(Input):
	
    def __init__(self, x, y, w, h, label='', value=''):
        super().__init__(x, y, w, h, label)
        self.value = value

    def atualiza_valor(self, key, unicode):
        if self.active:
            if unicode.lower() in ['1', '2', '3', '4', '5', '6', '7', '8', '9',
            'a', 'b', 'c', 'd', 'e', 'f']:
                self.value = unicode.upper()


class InputText(Input):
  
    def __init__(self, x, y, w, h, label=''):
        super().__init__(x, y, w, h, label)

    def atualiza_valor(self, key, unicode):
        if self.active:
            if key == p.K_BACKSPACE:
                if len(self.value) >= 1:
                    self.value = self.value[:-1]
            else:
                if re.match(r'[a-z]', unicode):
                    self.value += unicode

class InputCheck(Input):
    def __init__(self, x, y, w, h, options=[], label=''):
        super().__init__(x, y, w, h, label)
        self.options = options
        self.value = False

    def draw(self, surface, font):
        txt = font.render(self.options[int(self.value)], True, self.color)
        surface.blit(txt, (self.rect.x + 10, self.rect.y + 5))

        txt = font.render(self.label, True, self.color)
        surface.blit(txt, (self.rect.x - 30, self.rect.y + 5))

        p.draw.rect(surface, self.color, self.rect, 2)
    
    def atualiza_ativo(self, pos):
        if pos == None or self.rect.collidepoint(pos):
            self.value = not self.value

class InputSelect(Input):
    def __init__(self, x, y, w, h, label, color_t, color_f):
        super().__init__(x, y, w, h, label)
        self.value = False
        self.label = label
        self.current_color = color_f
        self.color_t = color_t
        self.color_f = color_f

    def draw(self, surface, font):
        if self.label == ' ':
            txt = font.render("?", True, self.color)
        else:
            txt = font.render(self.label, True, self.color)
        surface.blit(txt, (self.rect.x + 10, self.rect.y + 5))

        p.draw.rect(surface, self.current_color, self.rect, 2)
    
    def atualiza_ativo(self, pos):
        if self.rect.collidepoint(pos):
            self.value = not self.value
        self.current_color = self.color_t if self.value else self.color_f

