from key import Key
from dicionario import Dict

class Board:
    
    def __init__(self):

        self.board = [
            ['TP', '0', '0', 'DL', '0', '0', '0', 'TP', '0', '0', '0', 'DL', '0', '0', 'TP'],
            ['0', 'DP', '0', '0', '0', 'TL', '0', '0', '0', 'TL', '0', '0', '0', 'DP', '0'],
            ['0', '0', 'DP', '0', '0', '0', 'DL', '0', 'DL', '0', '0', '0', 'DP',  '0', '0'],
            ['DL', '0', '0', 'DP', '0', '0', '0', 'DL', '0', '0', '0', 'DP', '0', '0', 'DL'],
            ['0', '0', '0', '0', 'DP', '0', '0', '0', '0', '0', 'DP', '0', '0', '0', '0'],
            ['0', 'TL', '0', '0', '0', 'TL', '0', '0', '0', 'TL',  '0', '0', '0', 'TL', '0'],
            ['0', '0', 'DL', '0', '0', '0', 'DL', '0', 'DL', '0', '0', '0', 'DL', '0', '0'],

            ['TP', '0', '0', 'DL', '0', '0', '0', 'ST', '0', '0', '0', 'DL', '0', '0', 'TP'],

            ['0', '0', 'DL', '0', '0', '0', 'DL', '0', 'DL', '0', '0', '0', 'DL', '0', '0'],
            ['0', 'TL', '0', '0', '0', 'TL', '0', '0', '0', 'TL', '0', '0', '0', 'TL', '0'],
            ['0', '0', '0', '0', 'DP', '0', '0', '0', '0', '0', 'DP', '0', '0', '0', '0'],
            ['DL', '0', '0', 'DP', '0', '0', '0', 'DL', '0', '0', '0', 'DP', '0', '0', 'DL'],
            ['0', '0', 'DP', '0', '0', '0', 'DL', '0', 'DL', '0', '0', '0', 'DP', '0', '0'],
            ['0', 'DP', '0', '0', '0', 'TL', '0', '0', '0', 'TL', '0', '0', '0', 'DP', '0'],
            ['TP', '0', '0', 'DL', '0', '0', '0', 'TP', '0', '0', '0', 'DL', '0', '0', 'TP'],
        ]

        lista = [(x, y) for y in range(15) for x in range(15)]

        self.pont = {
            'DP': [
                x for x in filter(lambda x: self.board[x[0]][x[1]] == 'DP', lista )
            ] + [(7,7)],
            'DL': [
                x for x in filter(lambda x: self.board[x[0]][x[1]] == 'DL', lista )
            ],
            'TP': [
                x for x in filter(lambda x: self.board[x[0]][x[1]] == 'TP', lista )
            ],
            'TL': [
                x for x in filter(lambda x: self.board[x[0]][x[1]] == 'TL', lista )
            ],
        }

    def bloco_preenchido(self, x, y):

        if (x == 15) or (y == 15):
            return False

        if (self.board[x][y] == '0') or (self.board[x][y] == 'S') or (len(self.board[x][y]) == 2):
            return False

        return self.board[x][y]


    def calc_score(self, x, y, d, palavra):
        score = 0
        multiplicador_final = 1

        if d == 'v':
            i = y
            for c in palavra:
                sletra = Key(c).value
                if (x, i) in self.pont['TL']:
                    sletra *= 3
                elif (x, i) in self.pont['DL']:
                    sletra *= 2
                elif (x, i) in self.pont['DP']:
                    multiplicador_final *= 2
                elif (x, i) in self.pont['TP']:
                    multiplicador_final *= 3

                i += 1
                score += sletra 

        if d == 'h':
            i = x
            for c in palavra:
                sletra = Key(c).value
                if (i, y) in self.pont['TL']:
                    sletra *= 3
                elif (i, y) in self.pont['DL']:
                    sletra *= 2
                elif (i, y) in self.pont['DP']:
                    multiplicador_final *= 2
                elif (i, y) in self.pont['TP']:
                    multiplicador_final *= 3

                i += 1
                score += sletra 
        
        return score * multiplicador_final

    def no_tabuleiro(self, x, y, d, palavra):

        for c in palavra:
            if not self.bloco_preenchido(x, y):
                return False

            if d == 'v':
                y += 1
            elif d == 'h':
                x += 1

        return True

    def coloca_palavra(self, x, y, d, palavra):
        n = len(palavra)

        if d == 'v':
            i = y
            for c in palavra:                
                self.board[x][i] = c
                i += 1

        if d == 'h':
            i = x
            for c in palavra:
                self.board[i][y] = c
                i += 1