from player import Player
from key import Key
from juiz import Juiz

class Bot(Player):

    def __init__(self, juiz, name='ROBOZONARO'):
        super().__init__(name)
        self.board = juiz.board
        self.dic = juiz.dicionario

        self.primeira_jogada = True

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
            while (not self.board.bloco_preenchido(x, y)) and (y > 0):
                y -= 1
                limite += 1
        
        if d == 'h':
            x -= 1
            while (not self.board.bloco_preenchido(x, y)) and (x > 0):
                x -= 1
                limite += 1

        return limite if limite == 0 else limite + 1
    
    def get_ancoras(self):

        if self.board.board[7][7] == 'ST':
            return [(7, 7, 7,'v'), (7, 7, 7,'h'),]

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
                while (xx < 15) and self.board.bloco_preenchido(xx, y):
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
                while (yy < 15) and self.board.bloco_preenchido(x, yy):
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

        if(x == 15 or y == 15):
            return

        l = self.board.board[x][y]

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
            
            for e in node[1]:
                if (e in rack) and (e in self.cross_check(x, y, d)):
                    rack.remove(e)

                    if d == 'v':
                        self.extend_right(partial_word+e, node[1][e], x, y+1, rack, d)
                    
                    if d == 'h':
                        self.extend_right(partial_word+e, node[1][e], x+1, y, rack, d)
                    
                    rack.append(e)
        elif l in node[1]:

            if d == 'v':
                self.extend_right(partial_word+l, node[1][l], x, y+1, rack, d)
            
            if d == 'h':
                self.extend_right(partial_word+l, node[1][l], x+1, y, rack, d)
    
    def left_part(self, partial_word, node, limit, x, y, rack, d):
        self.extend_right(partial_word, node, x, y, rack, d)

        if limit > 0:
            for l in node[1]:
                if l in rack:
                    rack.remove(l)
                    self.left_part(partial_word+l, node[1][l], limit-1, x, y, rack, d)
                    rack.append(l)
    
    def play(self):
        
        ancoras = self.get_ancoras()
        self.move = None
        
        rack = [x.key for x in self.keys]

        for ancora in ancoras:
            x, y, l, d = ancora
            self.left_part('', self.dic.dfa, l, x, y, rack, d)
        
        return self.move
    
    def __str__(self):
        return self.name
