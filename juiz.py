from random import randint
from bag import Bag
from board import Board
from dicionario import Dict
from key import Key
import copy


class Juiz:

    def __init__(self):

        # self.turn = bool(randint(0,1))
        self.turn = True
        self.jogada = 1
        self.bag = Bag()
        self.board = Board()
        self.dicionario = Dict('wordlist-small.bin')

    def troca_turno(self):
        self.turn = not self.turn

    def verifica_jogada(self, jogador, x, y, d, palavra):

        n = len(palavra)

        if n <= 2:
            raise Exception('A palavra deve ter mais de 2 caracteres.')

        if (d == 'v') and ((y < 0) or ((y+n) >= 15)):
            raise Exception('Palavra muito longa.')

        if (d == 'h') and ((x < 0) or ((x+n) >= 15)):
            raise Exception('Palavra muito longa.')

        if self.jogada == 1:
            if (d == 'v') and ((y > 7) or ((y + n) < 7)):
                raise Exception('Primeira jogada deve passar pelo centro! (S)')
            if (d == 'h') and ((x > 7) or ((x + n) < 7)):
                raise Exception('Primeira jogada deve passar pelo centro! (S)')

        if not self.dicionario.find(palavra):
            raise Exception(f'A palavra {palavra} não existe no dicionario.')

        hand_cp = copy.deepcopy(jogador.keys)

        if d == 'v':
            for i in range(y, y+n):
                if self.verifica_letra(hand_cp, x, i, palavra[i-y]):
                    print(palavra[i-y])
                    hand_cp.remove(Key(palavra[i-y]))

        if d == 'h':
            for i in range(x, x+n):
                if self.verifica_letra(hand_cp, i, y, palavra[i-x]):
                    hand_cp.remove(Key(palavra[i-x]))

        return True

    def verifica_letra(self, hand, x, y, l):

        if self.board.bloco_preenchido(x, y):
            return self.board[x][y] == l

        for k in hand:
            if k.key == l or k.key == ' ':
                return True

    def realiza_jogada(self, jogador, x, y, d, palavra):

        if self.verifica_jogada(jogador, x, y, d, palavra):
            self.board.coloca_palavra(jogador, x, y, d, palavra)
            # self.troca_turno()