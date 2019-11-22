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
print("Характеристичексий многочлен:")
a = SquareMatrix([
    [-3, -4, -1, 4],
    [1, -4, -3, 3],
    [-5, -2, 2, 2],
    [0, 0, 2, -2],
])
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
