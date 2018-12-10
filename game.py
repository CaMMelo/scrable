import pygame as p
from player import Player
from bot import Bot
from juiz import Juiz
from screen import Screen


def unicode_hex_to_int(unicode):
    return int(unicode, 16)

def direction_decode(unicode):
    return 'h'if unicode else 'v'

class Game:
    
    def __init__(self):
        
        p.init()
        p.font.init()
        self.screen = Screen()

        self.juiz = Juiz()

        self.player1 = Player()
        self.player1.init_keys(self.juiz.bag)

        self.player2 = Bot()
        self.player2.init_keys(self.juiz.bag)

        self.run = True

    def game_loop(self):

        play_click = False

        while self.run:
            # Trata entrada
            for ev in p.event.get():
                
                if ev.type == p.QUIT:
                    self.run = False
                
                if ev.type == p.MOUSEBUTTONDOWN:
                    self.screen.x_input_box.atualiza_ativo(ev.pos)
                    self.screen.y_input_box.atualiza_ativo(ev.pos)
                    self.screen.d_input_box.atualiza_ativo(ev.pos)
                    self.screen.w_input_box.atualiza_ativo(ev.pos)

                    play_click = self.screen.play_button.check_click(ev.pos)

                if ev.type == p.KEYDOWN:
                    
                    self.screen.x_input_box.atualiza_valor(ev.key, ev.unicode)
                    self.screen.y_input_box.atualiza_valor(ev.key, ev.unicode)
                    self.screen.w_input_box.atualiza_valor(ev.key, ev.unicode)

            # Realiza jogada
            if play_click:
                x = self.screen.x_input_box.value
                y = self.screen.y_input_box.value
                d = self.screen.d_input_box.value
                palavra = self.screen.w_input_box.value

                x = unicode_hex_to_int(x)
                y = unicode_hex_to_int(y)
                d = direction_decode(d)

                self.juiz.realiza_jogada(self.player1, x, y, d, palavra)

                play_click = False


            # Imprimir tela
            self.screen.draw(self.player1.keys, self.juiz.board.board)

            p.display.flip()

        p.quit()


if __name__ == '__main__':
    game = Game()
    game.game_loop()