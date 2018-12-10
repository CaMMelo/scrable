from key import Key
from random import randrange

class Bag:

    def __init__(self):
        self.bag = []

        self.add_key(" ", 3)
        self.add_key("A", 14)
        self.add_key("E", 11)
        self.add_key("I", 10)
        self.add_key("O", 10)
        self.add_key("S", 8)
        self.add_key("U", 7)
        self.add_key("M", 6)
        self.add_key("R", 6)
        self.add_key("T", 5)

        self.add_key("D", 5)
        self.add_key("L", 5)
        self.add_key("C", 6)
        self.add_key("P", 4)

        self.add_key("N", 4)
        self.add_key("B", 3)

        self.add_key("F", 2)
        self.add_key("G", 2)
        self.add_key("H", 2)
        self.add_key("V", 2)

        self.add_key("J", 2)

        self.add_key("Q", 1)

        self.add_key("X", 1)
        self.add_key("Z", 1)

    def add_key(self, key, qtd=0):
        k = Key(key)

        if qtd == 0:
            self.bag.append(k)
        else:
            for i in range(0,qtd):
                self.bag.append(k)

    def sort_key(self):
        index = randrange(len(self.bag))
        aux = self.bag[index]
        del self.bag[index]

        return aux

    def __str__(self):
        aux = "["

        for k in self.bag:
            aux += str(k)+","
        aux += "]"
        return aux
