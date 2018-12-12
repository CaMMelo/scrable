from bag import Bag
from board import Board
from dicionario import Dict
from key import Key
import copy


class Juiz:

    def __init__(self):

        self.jogada = 1
        self.bag = Bag()
        self.board = Board()
        self.dicionario = Dict('wordlist-small.bin')

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
        antes_palavra = ''
        depois_palavra = ''

        aux_x, aux_y = x, y
        aux2_x, aux2_y = x, y

        for c in palavra:
            if self.board.board[aux_x][aux_y] == c:
                if d == 'h':
                    aux_x += 1
                else:
                    aux_y += 1
                continue
            
            antes_palavra = ''
            depois_palavra = ''
            nova_palavra = ''

            if d == 'h':
                # parte cima
                aux2_x, aux2_y = aux_x, aux_y-1
                while(self.board.bloco_preenchido(aux2_x, aux2_y)):
                    antes_palavra += self.board.board[aux2_x][aux2_y]
                    aux2_y -= 1
                antes_palavra = antes_palavra[::-1]

                # parte baixo
                aux2_x, aux2_y = aux_x, aux_y+1
                while(self.board.bloco_preenchido(aux2_x, aux2_y)):
                    depois_palavra += self.board.board[aux2_x][aux2_y]
                    aux2_y += 1

                aux_x += 1

                if antes_palavra or depois_palavra:
                    nova_palavra = antes_palavra+c+depois_palavra

            if d == 'v':
                # parte cima
                aux2_x, aux2_y = aux_x-1, aux_y
                while(self.board.bloco_preenchido(aux2_x, aux2_y)):
                    antes_palavra += self.board.board[aux2_x][aux2_y]
                    aux2_x -= 1
                antes_palavra = antes_palavra[::-1]

                # parte baixo
                aux2_x, aux2_y = aux_x+1, aux_y
                while(self.board.bloco_preenchido(aux2_x, aux2_y)):
                    depois_palavra += self.board.board[aux2_x][aux2_y]
                    aux2_x += 1

                aux_y += 1

                if antes_palavra or depois_palavra:
                    nova_palavra = antes_palavra+c+depois_palavra

            if not self.dicionario.find(nova_palavra) and (nova_palavra != ''):
                return False
        
        return True


    def verifica_jogada(self, jogador, x, y, d, palavra):

        n = len(palavra)

        if n == 0:
            raise Exception(f'Forneça uma palavra.')

        if not self.dicionario.find(palavra):
            raise Exception(f'A palavra {palavra} não existe no dicionario.')

        if (d == 'v') and ((y < 0) or ((y+n) > 15)):
            raise Exception(f'Palavra {palavra} muito longa ({x}, {y}, {d}).')

        if (d == 'h') and ((x < 0) or ((x+n) > 15)):
            raise Exception(f'Palavra {palavra} muito longa ({x}, {y}, {d}).')

        if self.jogada == 1:
            if (d == 'v') and ((y > 7) or ((y + n) <= 7) or (x != 7)):
                raise Exception('Primeira jogada deve passar pelo centro! (S)')
            if (d == 'h') and ((x > 7) or ((x + n) <= 7) or (y != 7)):
                raise Exception('Primeira jogada deve passar pelo centro! (S)')
        else:
            xx, yy = x, y
            b = False
            for c in palavra:
                b = self.board.bloco_preenchido(xx, yy)
                
                if b:
                    break
                
                if d == 'h':
                    xx += 1
                if d == 'v':
                    yy += 1 

            if not b:
                raise Exception(f'{palavra} deve estar conectada à uma outra palavra.')                       


        # confere 
        if not self.verifica_adjacencia(x,y,d,palavra):
            raise Exception(f'Palavra {palavra} não encaixa no tabuleiro.')

        hand_cp = copy.deepcopy(jogador.keys)

        if d == 'v':
            for i in range(y, y+n):

                l = palavra[i-y]
                
                if self.board.board[x][i] == l:
                    continue 

                for k in hand_cp:
                    if k.key == l:
                        hand_cp.remove(Key(l))
                        break
                    
                    elif k.key == ' ':
                        hand_cp.remove(Key(' '))
                        palavra = list(palavra)
                        palavra[i-y] = '?'
                        palavra = ''.join(palavra)
                        break

        if d == 'h':
            for i in range(x, x+n):
                l = palavra[i-x]
                
                if self.board.board[i][y] == l:
                    continue 

                for k in hand_cp:
                    if k.key == l:
                        hand_cp.remove(Key(l))
                        break
                    
                    elif k.key == ' ':
                        hand_cp.remove(Key(' '))
                        palavra = list(palavra)
                        palavra[i-x] = '?'
                        palavra = ''.join(palavra)
                        break

        jogador.keys = hand_cp
        return True

    def verifica_letra(self, hand, x, y, l):

        if self.board.bloco_preenchido(x, y):
            return self.board.board[x][y] == l

        for k in hand:
            if k.key == l or k.key == ' ':
                return True

    def realiza_jogada(self, jogador, x, y, d, palavra):

        if self.verifica_jogada(jogador, x, y, d, palavra):
            self.board.coloca_palavra(x, y, d, palavra)
            jogador.score += self.board.calc_score(x,y,d,palavra)
            jogador.renew_keys(self.bag)
            self.jogada += 1