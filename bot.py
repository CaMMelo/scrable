from player import Player

class Bot(Player):

    def __init__(self):
        super().__init__()
        pass
    

    def choose_action(self, board):

        x, y = 7, 7
        rack = [k.__str__() for k in self.keys]
        words = []


        # todo ARRUMAR BOT
        """ TODO 
        
        1 - ARRUMAR JOGADA DO BOT, VISTO QUE A PALAVRA ESCOLHIDA PELO BOT DEVE
        POSSUIR A PRIMEIRA LETRA JA NO TABULEIRO (SE NÃO FOR A PRIMEIRA JOGADA)
        
        """
        if board.board[x][y] == 'ST':
          
            words = board.generate_valid_moves(x, y, rack, 7)
        
        else:

            x, y = 0, 0
            l = board.board[x][y]

            while ((len(l) != 1) or (l == '0')):
                print(x,y)
                if y < 14:
                    y += 1
                else:
                    y = 0
                    x += 1
                l = board.board[x][y]
            
            words = board.generate_valid_moves(x, y, rack, 7)
        
        if len(words) == 0:
            return None

        words.sort(key=len, reverse=True)

        return x, y, 'H', words[0]