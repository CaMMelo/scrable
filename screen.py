import pygame as p
from input import InputNum, InputText, InputCheck, InputSelect
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

        self.x_input_box = InputNum(32*17+18, 32*9.25, 32, 32, label='X ', value='8')
        self.y_input_box = InputNum(32*20+12, 32*9.25, 32, 32, 'Y ', value='8')
        self.d_input_box = InputCheck(32*23+12, 32*9.25, 32, 32, ['V', 'H'], 'D ')
        self.w_input_box = InputText(32*16+50, 32*10.7, 219, 32, 'W ')

        self.hand_inputs = []

        for i in range(0,7):
            aux = InputSelect(((.25+(i*1.25))+16)*32, (7+.5)*32, 32, 32, '', (200,0,20), (120,120,120) )
            self.hand_inputs.append(aux)
        
        self.switch_keys_button = Button(32*16+20, 32*12.25, 250, 32, 'TROCAR LETRAS', self.font4, color=(200,00,80))

        self.pass_button = Button(32*16+20, 32*13.50, 250, 32, 'PASSAR TURNO', self.font4, color=(200,80,00))

        self.play_button = Button(32*16+20, 32*14.75, 250, 32, 'JOGAR!', self.font4, color=(0,200,20))

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
    
    def draw_player_info(self, player):
        y = 1.2

        text = self.font3.render("Nome: "+player.name, False, (250, 250, 250))
        self.surface.blit(text, (32 * 16 + 9,  (y+.25)*32))

        text = self.font3.render("Score: "+str(player.score), False, (250, 250, 250))
        self.surface.blit(text, (32 * 16 + 9,  (y+.25+.75)*32))

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

        buttons_section = (32*16,32*12,32*9,32*4)
        self.surface.fill((40,40,40), buttons_section)

        hand_section = (32*16,32*6,32*9,32*3)
        self.surface.fill((40,40,40), hand_section)
    
    def draw_inputs(self):
        
        self.x_input_box.draw(self.surface, self.font4)
        self.y_input_box.draw(self.surface, self.font4)
        self.d_input_box.draw(self.surface, self.font4)
        self.w_input_box.draw(self.surface, self.font4)
        self.switch_keys_button.draw(self.surface)
        self.play_button.draw(self.surface)
        self.pass_button.draw(self.surface)
    
    def draw_hand(self, hand):
        text = self.font3.render("Sua mão: ", False, (250, 250, 250))
        self.surface.blit(text, (32 * 16 + 9,  (6.3+.25)*32))

        for i,k in enumerate(hand):
            self.hand_inputs[i].label = k.key
            self.hand_inputs[i].draw(self.surface, self.font4)

    def draw_border_box(self, x, y, color, blind_t=0):
        square = (32*x,32*y,32,32)
        self.surface.fill(color, square, blind_t)

    def draw_selection(self, x, y):
        if x > 0 and y > 0:
            self.draw_border_box(x, 0, (200,0,30), blind_t=1)
            self.draw_border_box(0, y, (200,0,30), blind_t=1)
            self.draw_border_box(x, y, (100,100,100), blind_t=4)
    
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
    
    def draw(self, player, board, pos_sel_x, pos_sel_y):
        
        self.draw_bg()
        self.draw_border()
        self.draw_board(board)
        self.draw_selection(pos_sel_x, pos_sel_y)
        self.draw_player_info(player)

        self.draw_hand(player.keys)
        self.draw_inputs()

        p.display.flip()