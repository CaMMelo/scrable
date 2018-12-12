import pickle

# state = (final?, {transitions})
class DFA:

    def __init__(self):
        self.dfa = [False, {}]
    
    def insert(self, word):

        state = self.dfa

        for w in word:
            
            if w not in state[1]:
                state[1][w] = [False, {}]
            
            state = state[1][w]
        
        state[0] = True
    
    def minimize(self):
        pass
    
    def save(self, filename):
        
        with open(filename, 'wb+') as f:
            pickle.dump(self.dfa, f)

class Dict:

    def __init__(self, filename):
        self.load(filename)
    
    def load(self, filename):

        with open(filename, 'rb') as f:
            self.dfa = pickle.load(f)

    def find(self, word):
        
        state = self.dfa

        for w in word:
            
            if w in state[1]:
                state = state[1][w]
            else:
                return False
        
        return state[0]

if __name__ == '__main__':

    dfa = DFA()

    with open('dicionario.txt', 'r') as in_file:

        for line in in_file:
            line = line.strip()
            dfa.insert(line)
    
    # dfa.save('wordlist-small.bin')
