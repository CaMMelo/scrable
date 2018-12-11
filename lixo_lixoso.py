def generate_valid_moves(self, x, y, rack, limit):
        
        moves = []
        
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