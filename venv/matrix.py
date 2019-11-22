# coding=utf-8


class Permutation:
    def __init__(self, values):
        self.n = len(values)
        self.permutation = values

    # в качестве has нужно передавать список элементов,
    # все перестановки которых мы хотим получить, например, (0, 1, 2, 3, 4, 5)
    @staticmethod
    def get_permutations(n, has):
        if n == 0:
            return [[]]
        result = []
        for v in range(n):
            permutations = Permutation.get_permutations(n - 1, has[:v] + has[v + 1:])
            for permutation in permutations:
                result.append([has[v]] + permutation)
        return result

    @staticmethod
    def get_all_subsets(arr, new_size):
        if new_size == 0:
            return [[]]
        if new_size > len(arr):
            return []
        if new_size == len(arr):
            return [arr]
        res = []
        ss = get_all_subsets(arr[1:], new_size - 1)
        if len(ss) > 0:
            for el in ss:
                res.append([arr[0]] + el)
        res += get_all_subsets(arr[1:], new_size)
        return res

    def get_permutation_sign(self):
        cnt = 0
        for i in range(len(self.permutation)):
            for j in range(i + 1, len(self.permutation)):
                if self.permutation[i] > self.permutation[j]:
                    cnt += 1
        if cnt % 2 == 1:
            return -1
        return 1


class Matrix:
    def __init__(self, values):
        self.columns_count = len(values)
        self.rows_count = len(values[0])
        for row in values:
            if len(row) != self.rows_count:
                raise Exception
        self.matrix = values

    def __mul__(self, other):
        if self.columns_count != other.rows_count:
            raise Exception("Неправильный размер матриц для умножения")
        values = [[0] * other.columns_count for _ in range(self.rows_count)]
        for i in range(len(values)):
            for j in range(len(values[i])):
                for k in range(self.columns_count):
                    values[i][j] += self.matrix[i][k] * other.matrix[k][j]
        return Matrix(values)

    def multiply_on_number(self, x):
        for i in range(self.rows_count):
            for j in range(self.columns_count):
                self.matrix[i][j] *= x

    def get_transposed(self):
        values = [[0] * self.rows_count for _ in range(self.columns_count)]
        for i in range(self.rows_count):
            for j in range(self.columns_count):
                values[j][i] = self.matrix[i][j]
        return Matrix(values)


class SquareMatrix(Matrix):
    def __init__(self, values):
        Matrix.__init__(self, values)
        self.n = self.columns_count
        if self.n > 0:
            if len(values[0]) != self.n:
                raise Exception("Не квадратная матрица")
        self.is_det_computed = False
        self.det = -1

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
        x = 0
        y = 0
        for row_ind, row in enumerate(self.matrix):
            if row_ind != i:
                for col_ind, column in enumerate(row):
                    if col_ind != j:
                        values[y][x] = column
                        x += 1
                y += 1
                x = 0
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
            power = abs(power) - 1
        result = SquareMatrix.get_e(self.n)
        for i in range(power):
            result *= self
        return result

    def get_cofactor_matrix(self):
        values = [[0] * self.n for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                values[i][j] = self.get_minor(i, j) * (-1) ** (i + j)
        return SquareMatrix(values)

    def get_adjugate_matrix(self):
        return self.get_cofactor_matrix().get_transposed()

    def get_inverse_matrix(self):
        det = self.compute_det()
        if det == 0:
            raise Exception("Матрица необратима")
        adj_m = self.get_adjugate_matrix()
        adj_m.multiply_on_number(1 / det)
        return adj_m


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
