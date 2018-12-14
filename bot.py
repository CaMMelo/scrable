from player import Player
from key import Key
from juiz import Juiz
from random import shuffle

class Bot(Player):

    def __init__(self, juiz, name='BOT'):
        super().__init__(name)
        self.board = juiz.board
        self.dic = juiz.dicionario

        self.juiz = juiz
    
    def palavra_nao_existe(self, x, y, d, palavra):
        
        if d == 'v':

            for c in palavra:
                if not self.board.bloco_preenchido(x, y):
                    return True
                y += 1
        
        if d == 'h':
            for c in palavra:
                if not self.board.bloco_preenchido(x, y):
                    return True
                x += 1
        
        return False
    
    def calc_limite(self, x, y, d):

        limite = 0

        if d == 'v':
            y -= 1
            while (not self.board.bloco_preenchido(x, y)) and (y >= 0):
                y -= 1
                limite += 1
        
        if d == 'h':
            x -= 1
            while (not self.board.bloco_preenchido(x, y)) and (x >= 0):
                x -= 1
                limite += 1
        
        if self.board.bloco_preenchido(x, y):
            limite -= 1

        return limite
    
    def get_ancoras(self):

        if self.board.board[7][7] == 'ST':
            l = [(7, 7, 7,'h'), (7, 7, 7,'v'),]
            shuffle(l)
            return l

        n = len(self.board.board)
        m = len(self.board.board[0])

        ancoras = []

        for x in range(n):
            for y in range(m):
                
                if self.board.bloco_preenchido(x, y):

                    if not self.board.bloco_preenchido(x-1, y):
                        ancoras.append((x, y, self.calc_limite(x, y, 'h'), 'h'))
                    
                    if not self.board.bloco_preenchido(x, y-1):
                        ancoras.append((x, y, self.calc_limite(x, y, 'v'), 'v'))
        
        return ancoras
    
    def cross_check(self, x, y, d):
        
        letters = list('abcdefghijklmnopqrstuvwxyz')
        w = ''

        if d == 'h':

            if x > 0:
                xx = x-1
                l = self.board.board[xx][y]
                while (xx > 0) and self.board.bloco_preenchido(xx, y):
                    w = l + w
                    xx -= 1
                    l = self.board.board[xx][y]
            
            w += '*'
            
            if x < 14:
                xx = x+1
                l  = self.board.board[xx][y]
                while (xx < 14) and self.board.bloco_preenchido(xx, y):
                    w += l
                    xx += 1
                    l  = self.board.board[xx][y]
        if d == 'v':

            if y > 0:
                yy = y-1
                l = self.board.board[x][yy]
                while (yy > 0) and self.board.bloco_preenchido(x, yy):
                    w = l + w
                    yy -= 1
                    l = self.board.board[x][yy]
            
            w += '*'
            
            if y < 14:
                yy = y+1
                l  = self.board.board[x][yy]
                while (yy < 14) and self.board.bloco_preenchido(x, yy):
                    w += l
                    yy += 1
                    l  = self.board.board[x][yy]
        
        if w == '':
            return letters

        p = w.find('*')

        for c in 'abcdefghijklmnopqrstuvwxyz':
            w = list(w)
            w[p] = c
            w = ''.join(w)
            if not self.dic.find(w):
                letters.remove(c)

        return letters
    
    def extend_right(self, partial_word, node, x, y, rack, d):

        if x == 15 or y == 15:
            l = '0'
        elif x < 15 and y < 15:
            l = self.board.board[x][y]
        else:
            return

        if not self.board.bloco_preenchido(x, y):

            # salva a melhor jogada
            if node[0]:
                
                xx, yy = x, y

                if not self.primeira_jogada:
                    if d == 'v':
                        yy = y - len(partial_word)
                    if d == 'h':
                        xx = x - len(partial_word)

                score = self.board.calc_score(xx, yy, d, partial_word)
                ok = self.juiz.verifica_adjacencia(xx, yy, d, partial_word)
                ok = ok and self.palavra_nao_existe(xx, yy, d, partial_word)
                if ok and ((not self.move) or (self.move[4] < score)):
                    self.move = (xx, yy, d, partial_word, score)
            
            cross = self.cross_check(x, y, d)
            for e in node[1]:
                b = e in cross
                new_node = self.dic.dfa[node[1][e]]
                if (e in rack) and b:
                    rack.remove(e)
                    
                    if d == 'v':
                        self.extend_right(partial_word+e, new_node, x, y+1, rack, d)
                    
                    if d == 'h':
                        self.extend_right(partial_word+e, new_node, x+1, y, rack, d)
                    
                    rack.append(e)
                
                
                elif (' ' in rack) and b:
                    rack.remove(' ')
                    if d == 'v':
                        self.extend_right(partial_word+e, new_node, x, y+1, rack, d)
                    if d == 'h':
                        self.extend_right(partial_word+e, new_node, x+1, y, rack, d)
                    rack.append(' ')
                
        elif l in node[1]:
            new_node = self.dic.dfa[node[1][l]]

            if d == 'v':
                self.extend_right(partial_word+l, new_node, x, y+1, rack, d)
            
            if d == 'h':
                self.extend_right(partial_word+l, new_node, x+1, y, rack, d)
    
    def left_part(self, partial_word, node, limit, x, y, rack, d):
        self.extend_right(partial_word, node, x, y, rack, d)

        if limit > 0:
            for l in node[1]:
                new_node = self.dic.dfa[node[1][l]]
                if l in rack:
                    rack.remove(l)
                    self.left_part(partial_word+l, new_node, limit-1, x, y, rack, d)
                    rack.append(l)
                elif ' ' in rack:
                    rack.remove(' ')
                    self.left_part(partial_word+l, new_node, limit-1, x, y, rack, d)
                    rack.append(' ')

    def escolhe_trocas(self):
        
        vetor = [x for x in range(len(self.keys))]

        return vetor
    
    def play(self):
        
        ancoras = self.get_ancoras()
        self.move = None
        
        rack = [x.key for x in filter(lambda x: x != None, self.keys)]

        for ancora in ancoras:
            x, y, l, d = ancora
            self.left_part('', self.dic.dfa[0], l, x, y, rack, d)
        
        return self.move
    
    def __str__(self):
        return self.name
