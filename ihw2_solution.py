from matrix import Matrix, SquareMatrix

m1 = SquareMatrix([
    [1, 1, 1, 1],
    [1, 1, 1, 1],
    [1, 1, 1, 1],
    [1, 1, 1, 1]
])
m2 = SquareMatrix.get_e(4)
print(str(m2 ** -4))
print()
