import pygame as p
from input import InputNum, InputText, InputCheck
from button import Button


class Screen:

    def __init__(self):
        
        p.init()
        p.font.init()
        game_height = 600
        self.surface = p.display.set_mode((800, 512))
        self.font1 = p.font.SysFont('DejaVu Sans Mono', 26)
        self.font2 = p.font.SysFont('DejaVu Sans Mono', 23)
        self.font3 = p.font.SysFont('DejaVu Sans Mono', 16)
        self.font4 = p.font.SysFont('DejaVu Sans Mono', 20)

        self.color_inactive = p.Color('lightskyblue3')
        self.color_active = p.Color('dodgerblue2')

        self.x_input_box = InputNum(32*16+50, 32*10, 32, 32, label='X: ', value='8')
        self.y_input_box = InputNum(32*16+40*3.3, 32*10, 32, 32, 'Y: ', value='8')
        self.d_input_box = InputCheck(32*16+40*5.4, 32*10, 32, 32, ['V', 'H'], 'D: ')
        self.w_input_box = InputText(32*16+50, 32*11.4, 200, 32, 'W: ')
        self.play_button = Button(32*16+20, 32*14.5, 250, 32, 'JOGAR!', self.font4)

        self.play_b = p.Rect(32*16+20, 32*14.5, 250, 32)
    
    def draw_char(self, x, y, cor, char, type=None):
        square = (32*x,32*y,32,32)
        self.surface.fill(cor, square)

        if type == None or type == 1:
            text = self.font1.render(char, False, (230, 230, 230))
            self.surface.blit(text, (32 * x + 7, 32 * y + 1))
        elif type == 2:
            text = self.font2.render(char, False, (255, 255, 255))
            self.surface.blit(text, (32 * x + 3, 32 * y + 3))
    
    def draw_border(self):
        for i in range(1,16):
            if i % 2:
                cor = (33,33,33)
            else:
                cor = (26,26,26)

            if i < 10:
                self.draw_char(i, 0, cor, str(i))
                self.draw_char(0, i, cor, str(i))
            elif i == 10:
                self.draw_char(i, 0, cor, 'A')
                self.draw_char(0, i, cor, 'A')
            elif i == 11:
                self.draw_char(i, 0, cor, 'B')
                self.draw_char(0, i, cor, 'B')
            elif i == 12:
                self.draw_char(i, 0, cor, 'C')
                self.draw_char(0, i, cor, 'C')
            elif i == 13:
                self.draw_char(i, 0, cor, 'D')
                self.draw_char(0, i, cor, 'D')
            elif i == 14:
                self.draw_char(i, 0, cor, 'E')
                self.draw_char(0, i, cor, 'E')
            elif i == 15:
                self.draw_char(i, 0, cor, 'F')
                self.draw_char(0, i, cor, 'F')
    
    def draw_bg(self):
        self.surface.fill((22, 22, 22))
    
    def draw_inputs(self):
        
        self.x_input_box.draw(self.surface, self.font4)
        self.y_input_box.draw(self.surface, self.font4)
        self.d_input_box.draw(self.surface, self.font4)
        self.w_input_box.draw(self.surface, self.font4)
        self.play_button.draw(self.surface)
    
    def draw_hand(self, hand):
        y = 4
        text = self.font3.render("Sua mão: ", False, (230, 230, 230))
        self.surface.blit(text, (32 * 16 + 6,  (y+.25)*32))

        for i,k in enumerate(hand):
            self.draw_char((.25+(i*1.25))+16, y+1, (255, 255, 255), k.key)
    
    def draw_board(self, board):
        for i,row in enumerate(board):
            for j,c in enumerate(row):
                if c == '0':
                    if (j+i) % 2:
                        self.draw_char(i + 1, j + 1, (200, 200, 200), "")
                    else:
                        self.draw_char(i + 1, j + 1, (180, 180, 180), "")
                elif c == 'TP':
                    self.draw_char(i + 1, j + 1, (255,216,0), "TP", 2)
                elif c == 'DP':
                    self.draw_char(i + 1, j + 1, (255,0,51), "DP", 2)
                elif c == 'TL':
                    self.draw_char(i + 1, j + 1, (9,188,173), "TL", 2)
                elif c == 'DL':
                    self.draw_char(i + 1, j + 1, (0,106,255), "DL", 2)
                elif c == 'ST':
                    self.draw_char(i + 1, j + 1, (255, 72, 0), "S")
                else:
                    if (j+i) % 2:
                        self.draw_char(i + 1, j + 1, (112, 95, 42), c)
                    else:
                        self.draw_char(i + 1, j + 1, (132, 111, 43), c)
    
    def draw(self, hand, board):
        
        self.draw_bg()
        self.draw_border()
        self.draw_board(board)
        self.draw_hand(hand)

        self.draw_inputs()

        p.display.flip()