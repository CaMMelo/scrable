from bag import Bag
from board import Board
from dicionario import Dict
from key import Key
import copy

class MacacoException(Exception):

    def __init__(self, msg):
        super().__init__(msg)


class Juiz:

    def __init__(self):

        self.jogada = 1
        self.bag = Bag()
        self.board = Board()
        self.dic = Dict('wordlist-small.bin')

    def troca_letras(self, player, vet):
        keys = []
        for i in vet:
            keys.append(player.keys[i])
        for k in keys:
            if k != None:
                player.keys.remove(k)
                self.bag.add_key(k.key)
        player.renew_keys(self.bag) 

    def verifica_adjacencia(self, x, y, d, palavra):

        for c in palavra:
            w = ''
            
            if d == 'v':
                xx = x - 1
                l = self.board.bloco_preenchido(xx, y)
                if (x > 0) and l:
                    w = l + w
                    xx -= 1
                    while (xx >= 0) and l:
                        l = self.board.bloco_preenchido(xx, y)
                        xx -= 1
                        if l:
                            w = l + w

                w += c
                
                xx = x + 1
                l = self.board.bloco_preenchido(xx, y)
                if (x < 14) and l:
                    w = l + w
                    xx += 1
                    while (xx <= 14) and l:
                        l = self.board.bloco_preenchido(xx, y)
                        xx += 1
                        if l:
                            w += l
                y += 1
            elif d == 'h':
                yy = y - 1
                l = self.board.bloco_preenchido(x, yy)
                if (y > 0) and l:
                    w = l + w
                    yy -= 1
                    while (yy >= 0) and l:
                        l = self.board.bloco_preenchido(x, yy)
                        yy -= 1
                        if l:
                            w = l + w

                w += c
                
                yy = y + 1
                l = self.board.bloco_preenchido(x, yy)
                if (y < 14) and l:
                    w = l + w
                    yy += 1
                    while (yy <= 14) and l:
                        l = self.board.bloco_preenchido(x, yy)
                        yy += 1
                        if l:
                            w += l
                x += 1

            if not self.dic.find(w):
                return False
        
        return True


    def verifica_jogada(self, jogador, x, y, d, palavra):

        n = len(palavra)

        if n == 0:
            raise MacacoException(f'Forneça uma palavra.')

        if not self.dic.find(palavra):
            raise MacacoException(f'A palavra {palavra} não existe no dicionario.')

        if d == 'v':
            if (y + n - 1) > 14:
                raise MacacoException(f'Palavra muito longa.')
            elif ((y + n) <= 14) and self.board.bloco_preenchido(x, y+n):
                raise MacacoException(f'Palavra muito curta.')
        elif d == 'h':
            if (x + n - 1) > 14:
                raise MacacoException(f'Palavra muito longa.')
            elif ((x + n) <= 14) and self.board.bloco_preenchido(x+n, y):
                raise MacacoException(f'Palavra muito curta.')

        xx, yy = x, y
        if self.jogada == 1:
            if d == 'v':
                yy += n - 1
            elif d == 'h':
                xx += n - 1
            if not ((x <= 7 <= xx) or (y <= 7 <= yy)):
                raise MacacoException(f'A primeira jogada deve utilizar o bloco do centro.')
        else:
            usa_letra_do_tabuleiro = 0
            for c in palavra:
                if not self.board.bloco_preenchido(xx, yy):
                    if d == 'v':
                        yy += 1
                    elif d == 'h':
                        xx += 1
                else:
                    usa_letra_do_tabuleiro = True
                    break
            if not usa_letra_do_tabuleiro:
                raise MacacoException(f'Utilize ao menos uma letra do tabuleiro.')

            if not self.verifica_adjacencia(x, y, d, palavra):
                raise MacacoException(f'Todas as palavras formadas devem estar no dicionario.')

        return True

    def verifica_letra(self, hand, x, y, l):

        if self.board.bloco_preenchido(x, y):
            return self.board.board[x][y] == l

        for k in hand:
            if k.key == l or k.key == ' ':
                return k

        return False

    def realiza_jogada(self, jogador, x, y, d, palavra):

        xx, yy = x, y
        keys = []
        for c in palavra:
            key = self.verifica_letra(jogador.keys, xx, yy, c)

            if key and (type(key).__name__ == 'Key'):
                keys.append(key)
            else:
                raise MacacoException(f'Não é possivel formar a palavra {palavra}.')

        for key in keys:
            jogador.keys.remove(key)

        if self.verifica_jogada(jogador, x, y, d, palavra):
            jogador.score += self.board.calc_score(x,y,d,palavra)
            self.board.coloca_palavra(x, y, d, palavra)
            jogador.renew_keys(self.bag)
            self.jogada += 1
