import numpy as np

for dim in [200, 400, 800, 1200, 1600, 2000]:
    with open(f'A{dim}.txt', 'r') as matrix:
        matr1 = np.matrix([list(map(int, x.split(' '))) for x in matrix.readlines()])

    with open(f'B{dim}.txt', 'r') as matrix:
        matr2 = np.matrix([list(map(int, x.split(' '))) for x in matrix.readlines()])

    matr_rez = matr1 * matr2

    with open(f'C{dim}.txt', 'r') as matrix:
        matr3 = np.matrix([list(map(int, x.split(' '))) for x in matrix.readlines()])

    print(f'Compare result for {dim} dimension:', np.array_equal(matr_rez, matr3))
