from matrix import Matrix, SquareMatrix

m1 = SquareMatrix([
    [1, 1, 1, 1],
    [1, 1, 1, 1],
    [1, 1, 1, 1],
    [1, 1, 1, 1]
])
m2 = SquareMatrix.get_e(4)
print((m1 ** 2).matrix)
print((m2.get_inverse_matrix()).matrix)
print("\n".join(map(str, (m1.get_adjugate_matrix()).matrix)))
