# coding=utf-8
from permutation import Permutation
from fractions import gcd


def lcm(values: list):
    if len(values) < 1:
        return 1
    result = values[0]
    for v in values[1:]:
        result = result * v // gcd(result, v)
    return result


class Matrix:
    def __init__(self, values):
        self.rows_count = len(values)
        if self.rows_count == 0:
            raise Exception("Я не поддерживаю матрицы нулевого размера")
        self.columns_count = len(values[0])
        if self.columns_count == 0:
            raise Exception("Я не поддерживаю матрицы нулевого размера")
        for row in values:
            if len(row) != self.columns_count:
                raise Exception("Количество элементов в строчках не равны")
        self.matrix = values

    def __add__(self, other):
        if self.columns_count != other.columns_count or self.rows_count != other.rows_count:
            raise Exception("Матрицы должны быть одного размера")
        values = [[0] * self.columns_count for _ in range(self.rows_count)]
        for i in range(self.rows_count):
            for j in range(self.columns_count):
                values[i][j] = self.matrix[i][j] + other.matrix[i][j]
        if self.columns_count == self.rows_count:
            return SquareMatrix(values)
        return Matrix(values)

    def __sub__(self, other):
        return self + other.multiply_on_number(-1)

    def __mul__(self, other):
        if self.columns_count != other.rows_count:
            raise Exception("Неправильный размер матриц для умножения")
        values = [[0] * other.columns_count for _ in range(self.rows_count)]
        for i in range(len(values)):
            for j in range(len(values[i])):
                for k in range(self.columns_count):
                    values[i][j] += self.matrix[i][k] * other.matrix[k][j]
        if other.columns_count == self.rows_count:
            return SquareMatrix(values)
        return Matrix(values)

    def multiply_on_number(self, x):
        values = [[0] * self.columns_count for _ in range(self.rows_count)]
        for i in range(self.rows_count):
            for j in range(self.columns_count):
                values[i][j] = x * self.matrix[i][j]
        if self.columns_count == self.rows_count:
            return SquareMatrix(values)
        return Matrix(values)

    def get_transposed(self):
        values = [[0] * self.rows_count for _ in range(self.columns_count)]
        for i in range(self.rows_count):
            for j in range(self.columns_count):
                values[j][i] = self.matrix[i][j]
        if self.rows_count == self.columns_count:
            return SquareMatrix(values)
        return Matrix(values)

    def __str__(self):
        sizes = [[0] * self.columns_count for _ in range(self.rows_count)]
        for i, row in enumerate(self.matrix):
            for j, el in enumerate(row):
                sizes[i][j] = max(sizes[i][j], len(str(el)))
        res = ""
        for i in range(self.rows_count):
            res += "|"
            for j in range(self.columns_count):
                el_len = len(str(self.matrix[i][j]))
                if j < self.columns_count - 1:
                    res += str(self.matrix[i][j]) + "  " + " " * (sizes[i][j] - el_len)
                else:
                    res += str(self.matrix[i][j])
            res += "|"
            if i < self.rows_count - 1:
                res += "\n"
        return res

    def rank(self):
        matrix = self.matrix
        start = 0
        for i in range(self.columns_count):
            this_column = [matrix[row][i] for row in range(start, self.rows_count)]
            this_column = list(filter(lambda x: x != 0, this_column))
            current_lcm = lcm(this_column)
            for j in range(start, self.rows_count):
                if matrix[j][i] == 0:
                    continue
                multiplier = current_lcm // matrix[j][i]
                for k in range(self.columns_count):
                    matrix[j][k] *= multiplier
            first_not_zero_row_index = -1
            for j in range(start, self.rows_count):
                if matrix[j][i] != 0:
                    first_not_zero_row_index = j
                    break
            if first_not_zero_row_index == -1:
                continue
            start = first_not_zero_row_index + 1
            for j in range(first_not_zero_row_index + 1, self.rows_count):
                if matrix[j][i] == 0:
                    continue
                for k in range(self.columns_count):
                    matrix[j][k] -= matrix[first_not_zero_row_index][k]
        all_zeros_rows_count = 0
        for i in range(self.rows_count):
            all_zeros = True
            for j in range(self.columns_count):
                all_zeros = all_zeros and (matrix[i][j] == 0)
            if all_zeros:
                all_zeros_rows_count += 1
        print(Matrix(matrix))
        return self.rows_count - all_zeros_rows_count


class SquareMatrix(Matrix):
    def __init__(self, values):
        Matrix.__init__(self, values)
        self.n = self.columns_count
        if self.n > 0:
            if len(values[0]) != self.n:
                raise Exception("Не квадратная матрица")
        self.is_det_computed = False
        self.det = -1
        self.is_adjugate_computed = False
        self.adjugate = None

    def compute_det(self):
        if self.is_det_computed:
            return self.det
        permutations = Permutation.get_permutations(self.n, list(range(self.n)))
        value = 0
        for permutation in permutations:
            x = 1
            for i in range(self.n):
                x *= self.matrix[i][permutation[i]]
            value += Permutation(permutation).get_permutation_sign() * x
        if self.n == 0:
            value = 1
        self.is_det_computed = True
        self.det = value
        return value

    def get_minor(self, i, j):
        values = [[0] * (self.n - 1) for _ in range(self.n - 1)]
        for i, row in enumerate(self.matrix[:i] + self.matrix[i + 1:]):
            values[i] = row[:j] + row[j + 1:]
        return SquareMatrix(values).compute_det()

    def get_r(self, arr_i):
        real_indexes = sorted(list(set(range(self.n)) - set(arr_i)))
        new_m = [[0] * len(real_indexes) for _ in range(len(real_indexes))]
        for i in range(len(real_indexes)):
            for j in range(len(real_indexes)):
                new_m[i][j] = self.matrix[real_indexes[i]][real_indexes[j]]
        return SquareMatrix(new_m)

    def get_characteristic_polynomial(self):
        ans = [1]
        multiplier = -1
        for i in range(1, self.n + 1):
            ans_i = 0
            subsets_i = Permutation.get_all_subsets(list(range(self.n)), self.n - i)
            for subset in subsets_i:
                ans_i += self.get_r(subset).compute_det()
            ans.append(multiplier * ans_i)
            multiplier *= -1
        return ans

    @staticmethod
    def get_e(n):
        values = [[0] * n for _ in range(n)]
        for i in range(n):
            values[i][i] = 1
        return SquareMatrix(values)

    def __pow__(self, power):
        if not isinstance(power, int):
            raise Exception("Не умеем возводить в нецелые степени:(")
        if power < 0:
            return self.get_inverse_matrix() ** abs(power)
        result = SquareMatrix.get_e(self.n)
        for i in range(power):
            result *= self
        return SquareMatrix(result.matrix)

    def get_cofactor_matrix(self):
        values = [[0] * self.n for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                values[i][j] = self.get_minor(i, j) * (-1) ** (i + j + 2)
        return SquareMatrix(values)

    def get_adjugate_matrix(self):
        if self.is_adjugate_computed:
            return self.adjugate
        self.adjugate = self.get_cofactor_matrix().get_transposed()
        self.is_adjugate_computed = True
        return self.adjugate

    def get_inverse_matrix(self):
        det = self.compute_det()
        if det == 0:
            raise Exception("Матрица необратима")
        adj_m = self.get_adjugate_matrix()
        adj_m = adj_m.multiply_on_number(1 / det)
        return SquareMatrix(adj_m.matrix)
