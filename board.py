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

    def bloco_preenchido(self, x, y):

        if (self.board[x][y] == '0') or (self.board[x][y] == 'S') or (len(self.board[x][y]) == 2):
            return False

        return self.board[x][y]

    def coloca_palavra(self, x, y, d, palavra):
        n = len(palavra)
        score = 0
        multiplicador_final = 1

        if d == 'v':
            i = y
            for c in palavra:
                sletra = Key(c).value
                if self.board[x][i] == 'TL':
                    sletra *= 3
                elif self.board[x][i] == 'DL':
                    sletra *= 2
                elif (self.board[x][i] == 'DP') or (self.board[x][i] == 'ST'):
                    multiplicador_final *= 2
                elif self.board[x][i] == 'TP':
                    multiplicador_final *= 3

                score += sletra 
                
                self.board[x][i] = c
                i += 1

        if d == 'h':
            i = x
            for c in palavra:
                sletra = Key(c).value
                if self.board[i][y] == 'TL':
                    sletra *= 3
                elif self.board[i][y] == 'DL':
                    sletra *= 2
                elif (self.board[i][y] == 'DP') or (self.board[x][i] == 'ST'):
                    multiplicador_final *= 2
                elif self.board[i][y] == 'TP':
                    multiplicador_final *= 3

                score += sletra 
                self.board[i][y] = c
                i += 1

        return score * multiplicador_final