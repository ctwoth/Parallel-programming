import numpy as np

print("Entire matrices paths: ", end='')
path1, path2 = input().split(" ")

with open(path1, 'r') as matrix:
    matr1 = np.matrix([list(map(int, x.split(' '))) for x in matrix.readlines()])

with open(path2, 'r') as matrix:
    matr2 = np.matrix([list(map(int, x.split(' '))) for x in matrix.readlines()])

print("matrix 1:\n", matr1,end='\n\n')
print("matrix 2:\n", matr2)

print("\nrez:\n", matr1*matr2)