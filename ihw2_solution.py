from matrix import Matrix, SquareMatrix
from permutation import Permutation

print("Задание 1.")
p1 = Permutation([4, 5, 6, 2, 3, 7, 0, 1])
p2 = Permutation([4, 1, 3, 7, 6, 5, 0, 2])
p3 = Permutation([5, 4, 0, 2, 3, 7, 6, 1])
all_permutations = Permutation.get_permutations(8, list(range(8)))
right = (p1.get_inverse_permutation() * (p2 ** 13)) ** 187
for permutation in all_permutations:
    p = Permutation(permutation)
    if (p * p3 * p).permutation == right.permutation:
        print("Результат:")
        print("(0 1 2 3 4 5 6 7)")
        print("(", " ".join(str(i) for i in p.permutation), ")", sep="")
print("Задание 2.")
a = SquareMatrix([
    [2, -2, 2, -3],
    [1, -3, 2, -1],
    [1, 1, -3, 3],
    [-2, -3, 3, 2]
])
b = SquareMatrix([
    [-9, 3, 9, -4],
    [-6, -2, 4, 9],
    [-9, 6, 10, -3],
    [6, -10, 9, 6]
])
c = SquareMatrix([
    [2, 2, 3, 1],
    [2, 1, 1, -2],
    [2, 1, -1, -1],
    [-1, 2, -1, 2]
])
d = SquareMatrix([
    [-1, -1, -1, -1],
    [-1, -2, -2, -2],
    [-1, -2, -3, -1],
    [1, 2, 3, 2]
])
left = (SquareMatrix.get_e(4).multiply_on_number(a.compute_det() * c.compute_det()) -
        (b * c.get_adjugate_matrix() * d * c.get_adjugate_matrix()))
left = left * c * d.get_adjugate_matrix() * a
print("Определителитель матрицы, на которую домножаем = ", (c * d.get_adjugate_matrix() * a).compute_det())
print(left.multiply_on_number(1/851))
print("Задание 3.")
print("Характеристичексий многочлен:")
a = SquareMatrix([
 [-5.55111512e-17, -3.17915329e-02,  3.66312778e-02,  6.16848637e-02],
 [ 6.73794700e-03, 1.53740961e-02,  1.15776919e-02,  9.67948978e-03],
 [-6.73794700e-03,  2.94154278e-03, -1.15776919e-02, -2.79951287e-02],
 [ 6.73794700e-03, -2.94154278e-03,  2.98933308e-02,  4.63107676e-02]])
for i, a_i in enumerate(a.get_characteristic_polynomial()[:4]):
    print("(" + str(a_i) + ")x^" + str(4 - i) + " + ", end="")
print("(" + str(a.get_characteristic_polynomial()[4]) + ")")
x = SquareMatrix((a ** 2 + a.multiply_on_number(3) + SquareMatrix.get_e(4).multiply_on_number(2)).matrix) ** 2
print("Определитель посчитаю на листочке из значений характеристического")
print("Задание 5")
A = Matrix([
    [3, -3],
    [1, -1],
    [-1, 1],
    [4, -4],
    [-3, 3]
])
B = Matrix([
    [-2, -1, 3, 2, 1],
    [3, 1, -2, -1, 2]
])
res = SquareMatrix((A * B).matrix)
for i, a_i in enumerate(res.get_characteristic_polynomial()[:5]):
    print("(" + str(a_i) + ")x^" + str(5 - i) + " + ", end="")
print("(" + str(res.get_characteristic_polynomial()[5]) + ")")
