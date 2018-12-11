



class Medo:

    mat = [
        [1,2,3,4],
        [1,2,3,4],
        [1,2,3,4],
        [1,2,3,4],
    ]


class Fear:

    def __init__(self, mat):
        self.mat = mat


if __name__ == '__main__':

    m = Medo()
    f = Fear(m.mat)

    m.mat[0][0] = 70

    print(f.mat)