class Key:
    def __init__(self, key):
        self.key = key.lower()

        if key in ['a', 'e', 'i', 'o', 's', 'u', 'm', 'r', 't']:
            self.value = 1

        elif key in ['d', 'l', 'c', 'p']:
            self.value = 2

        elif key in ['n', 'b']:
            self.value = 3

        elif key in ['f', 'g', 'h', 'v']:
            self.value = 4

        elif key in ['j']:
            self.value = 5

        elif key in ['q']:
            self.value = 6

        elif key in ['x', 'z']:
            self.value = 8

        else:
            self.value = 0

    def __str__(self):
        return self.key

    def __repr__(self):
        return self.key
    
    def __eq__(self, other):
        return self.value == other.value

if __name__ == "__main__":
    a = Key('a')
    b = Key('a')

    vet = [Key('a'), Key('b')]
    vet.remove(Key('a'))

    for k in vet:
        print(k)
