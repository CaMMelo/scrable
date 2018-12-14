import pickle

# state = (final?, {transitions})

class DFA:

    def __init__(self):
        dfa = [False, {}]
        
        self.states = [dfa, ]
    
    def insert(self, word):
        
        n = len(self.states) - 1

        state = self.states[0]

        for w in word:
            
            if w not in state[1]:
                new_state = [False, {}]
                n += 1
                state[1][w] = n
                
                self.states.append(new_state)
            
            state = state[1][w]
            state = self.states[state]
        
        state[0] = True
    
    def minimize(self):
        
        n = len(self.states)
        
        alfabeto = [chr(x) for x in range(ord('a'), ord('z')+1)]
        
        estados_accept = frozenset([x for x in filter(lambda x: self.states[x][0], range(n))])
        estados_reject = frozenset([x for x in filter(lambda x: not self.states[x][0], range(1,n))])
        
        P = set([estados_accept, estados_reject])
        Q = set([estados_accept])
        
        source = {}
        letter = {}
        
        for k in range(n):
            for c in self.states[k][1]:
                t = self.states[k][1][c]
                source[t] = k
                letter[t] = c
        
        it = 0
        while len(Q) > 0:
            it += 1
            print(f'ITERAÇÃO #{it}, {len(Q)}, {len(P)}, {n}')
            A = Q.pop()
            
            for c in alfabeto:
                
                X = set([source[x] for x in filter(lambda x: letter[x] == c, A)])
                pos = 0
                
                for Y in P.copy():
                    i = frozenset(X & Y)
                    
                    if len(i) > 0:
                        
                        d = frozenset(Y - X)
                        
                        P.discard(Y)
                        P.add(i)
                        P.add(d)
                        
                        if Y in Q:
                            Q.discard(Y)
                            Q.add(i)
                            Q.add(d)
                        else:
                            if len(i) < len(d):
                                Q.add(i)
                            else:
                                Q.add(d)
                
                        
        # end while
        
        with open('temp.bin', 'wb+') as f:
            pickle.dump(P, f)
        
        
    def from_set(self, P):
        
        n = len(self.states)
        P = list(P)
        P.remove(frozenset())
        
        equiv = {}
        for i, e in enumerate(P):
            for k in e:
                equiv[k] = i+1
        
        equiv[0] = 0
        
        states = [[False, {}] for x in range(len(P)+1) ]
        
        for k in range(n):
            source = equiv[k]
            for c in self.states[k][1]:
                target = equiv[self.states[k][1][c]]
                states[source][1][c] = target
            
            states[source][0] = self.states[k][0]

        self.states = states
    
    def save(self, filename):
        
        with open(filename, 'wb+') as f:
            pickle.dump(self.states, f)

class Dict:

    def __init__(self, filename):
        self.load(filename)
    
    def load(self, filename):

        with open(filename, 'rb') as f:
            self.dfa = pickle.load(f)

    def find(self, word):
        
        k = 0
        
        for c in word:
            
            if c in self.dfa[k][1]:
                k = self.dfa[k][1][c]
            else:
                return False
        
        return self.dfa[k][0]

if __name__ == '__main__':

    dfa = DFA()
    path = 'dicionario'

    with open(path, 'r') as in_file:

        for line in in_file:
            line = line.strip()
            dfa.insert(line)
    
    
    dfa.save('wordlist-big.bin')
    
    if True:
    
        #dfa.minimize()
        
        
        with open('temp.bin', 'rb') as f:
            
            p = pickle.load(f)
            dfa.from_set(p)
        
        dfa.save('wordlist-small.bin')
        
        
        dfa = Dict('wordlist-small.bin')
        
        with open(path, 'r') as in_file:

            for line in in_file:
                line = line.strip()
                if not dfa.find(line):
                    print(line)
