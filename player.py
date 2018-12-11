class Player:

    def __init__(self, name):
        self.keys = []
        self.score = 0
        self.name = name

    def init_keys(self, bag):
        for i in range(0,7):
            self.keys.append(bag.sort_key())

    def add_key(self, key):
        self.keys.append(key)

    def renew_keys(self, bag):
        while len(self.keys) < 7:
            self.keys.append(bag.sort_key())