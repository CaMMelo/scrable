import pygame as p
from random import randint
from player import Player
from bot import Bot
from juiz import Juiz
from screen import Screen
from key import Key


def unicode_hex_to_int(unicode):
    return int(unicode, 16) - 1

def int_to_hex(str):
    if str == '10': return 'A'
    if str == '11': return 'B'
    if str == '12': return 'C'
    if str == '13': return 'D'
    if str == '14': return 'E'
    if str == '15': return 'F'
    return str


def direction_decode(unicode):
    return 'h'if unicode else 'v'

class Game:
    
    def __init__(self):
        
        p.init()
        p.font.init()
        self.screen = Screen()

        self.juiz = Juiz()

        self.turno = bool(randint(0,1))

        self.player1 = Bot(self.juiz, 'ROBOZONARO')
        self.player1.init_keys(self.juiz.bag)

        self.player2 = Bot(self.juiz, 'ROBOZONARA')
        self.player2.init_keys(self.juiz.bag)

        self.run = True

        self.passadas = 0
    
    def troca_turno(self):
        self.turno = not self.turno

    def reset_hand_inputs(self):
        for hand_input in self.screen.hand_inputs:
            hand_input.value = False
            hand_input.current_color = hand_input.color_f

    def game_loop(self):

        play_click = False
        switch_keys_click = False
        pass_click = False
        selection_click = False
        pos_sel_x = 0
        pos_sel_y = 0

        while self.run:

            player = self.player1 if self.turno else self.player2
            
            # Trata entrada
            for ev in p.event.get():
                if ev.type == p.MOUSEMOTION:
                    pos = p.mouse.get_pos()
                    if (pos[0] >= 32 and pos[1] >= 32) and (pos[0] <= 512 and pos[1] <=512):
                        pos_sel_x = pos[0] // 32
                        pos_sel_y = pos[1] // 32
                    else:
                        pos_sel_x = 0
                        pos_sel_y = 0

                if ev.type == p.QUIT:
                    self.run = False
                    continue
                
                if ev.type == p.MOUSEBUTTONDOWN:
                    self.screen.x_input_box.atualiza_ativo(ev.pos)
                    self.screen.y_input_box.atualiza_ativo(ev.pos)
                    self.screen.d_input_box.atualiza_ativo(ev.pos)
                    self.screen.w_input_box.atualiza_ativo(ev.pos)

                    for hand_input in self.screen.hand_inputs:
                        hand_input.atualiza_ativo(ev.pos)

                    play_click = self.screen.play_button.check_click(ev.pos)
                    switch_keys_click = self.screen.switch_keys_button.check_click(ev.pos)
                    pass_click = self.screen.pass_button.check_click(ev.pos)
                    
                    pos = p.mouse.get_pos()
                    if (pos[0] >= 32 and pos[1] >= 32) and (pos[0] <= 512 and pos[1] <=512) and ev.button == 1:
                        selection_click = True

                    if ev.button == 3:
                        self.screen.d_input_box.atualiza_ativo(None)

                if ev.type == p.KEYDOWN:
                    if ev.key == p.K_RETURN:
                        play_click = True
                    
                    self.screen.x_input_box.atualiza_valor(ev.key, ev.unicode)
                    self.screen.y_input_box.atualiza_valor(ev.key, ev.unicode)
                    self.screen.w_input_box.atualiza_valor(ev.key, ev.unicode)
            
            # selection click
            if selection_click:
                self.screen.x_input_box.value = int_to_hex(str(pos_sel_x))
                self.screen.y_input_box.value = int_to_hex(str(pos_sel_y))
                self.screen.w_input_box.active = True
                selection_click = False
            
            if (type(player).__name__ == 'Bot'):
                
                jogada = player.play()

                if play_click or True:

                    if jogada:
                        print(jogada)
                        x, y, d, palavra, _ = jogada
                        self.juiz.realiza_jogada(player, x, y, d, palavra)
                        self.player1.primeira_jogada = False
                        self.player2.primeira_jogada = False
                        self.passadas = 0
                    else:
                        self.juiz.troca_letras(player, [0,1,2,3,4,5,6])
                        self.passadas += 1
                    
                    play_click = False
            else:
                if play_click:
                    self.troca_turno()

                    jogada = player.play()

                    x = self.screen.x_input_box.value
                    y = self.screen.y_input_box.value
                    d = self.screen.d_input_box.value
                    palavra = self.screen.w_input_box.value

                    x = unicode_hex_to_int(x)
                    y = unicode_hex_to_int(y)
                    d = direction_decode(d)

                    self.screen.w_input_box.value = ''

                    play_click = False
                
                # Trocar palavras
                if switch_keys_click:
                    self.troca_turno()
                    vet_aux = []
                    for i in range(0,7):
                        if self.screen.hand_inputs[i].value: vet_aux.append(i)
                            
                    self.juiz.troca_letras(player, vet_aux)
                    switch_keys_click = False
                    self.reset_hand_inputs()
                
                # Passar turno
                if pass_click:
                    self.troca_turno()
                    pass_click = False
                    self.passadas += 1
                else:
                    self.passadas = 0
            
            if self.passadas >= 2:
                raise Exception(f'FIM DE JOGO!')

            # Imprimir tela
            self.screen.draw(player, self.juiz.board.board, pos_sel_x, pos_sel_y)

            p.display.flip()

        p.quit()


if __name__ == '__main__':
    game = Game()
    game.game_loop()