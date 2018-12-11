

def generate_valid_moves(self, x, y, rack, limit):
        
        moves = []

        def cross_check(x, y):

            letters = list('abcdefghijklmnopqrstuvwxyz')

            yy = y-1
            l  = self.board[x][yy]
            w = ''
            while (yy > 0) and ((len(l) == 1) and (l != '0')):
                w = l + w
                yy-=1
                l  = self.board[x][yy]
            w + '*'
            
            yy = y+1
            l  = self.board[x][yy]
            while (yy < 15) and ((len(l) == 1) and (l != '0')):
                w += l
                yy += 1
                l  = self.board[x][yy]
            
            p = w.find('*')

            if w == '':
                return letters

            for c in 'abcdefghijklmnopqrstuvwxyz':
                w = list(w)
                w[p] = c
                w = ''.join(w)
                if not self.dic.find(w):
                    letters.remove(c)

            return letters

        def extend_right(partial_word, node, x, y, rack):
            
            l = self.board[x][y]

            if (len(l) != 1) or (l == '0'):
                
                if node[0] and (partial_word not in moves):
                    moves.append(partial_word)
                
                for e in node[1]:
                    if (e in rack) and (e in cross_check(x, y)):
                        rack.remove(e)
                        extend_right(partial_word+e, node[1][e], x, y+1, rack)
                        rack.append(e)
            elif l in node[1]:
                extend_right(partial_word+l, node[1][l], x, y+1, rack)
        
        def left_part(partial_word, node, limit, x, y, rack):
            extend_right(partial_word, node, x, y, rack)

            if limit > 0:
                for l in node[1]:
                    if l in rack:
                        rack.remove(l)
                        left_part(partial_word+l, node[1][l], limit-1, x, y, rack)
                        rack.append(l)
        
        left_part('', self.dic.dfa, limit, x, y, rack)

        return moves



class Bot:

    def __init__(self):
        pass
    
