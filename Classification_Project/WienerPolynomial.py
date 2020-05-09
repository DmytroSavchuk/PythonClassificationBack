import pandas as pd


class WienerPolynomial:
    def __init__(self, degree=2):
        self.degree = degree

    def e(self, res, f, t, n, d=[]):
        for i in range(f, t):
            if (len(d) < n - 1):
                a = d.copy()
                a.append(i)
                self.e(res, i, t, n, a)
            else:
                a = d.copy()
                a.append(i)
                res.append(a)

    def calculate(self, res, l, n):
        for i in range(1, n + 1):
            self.e(res, 0, l, i)

    def calc_row(self, calc_x, x):
        res = []
        for i in range(len(calc_x)):
            item = 1
            for j in range(len(calc_x[i])):
                item *= x[calc_x[i][j]]
            res.append(item)
        return res

    def create_table(self, table):
        res = []
        row = []
        self.calculate(row, len(table[0]) - 1, self.degree)
        for i in range(len(table)):
            new_row = self.calc_row(row, table[i][:len(table[0]) - 1])
            new_row.append(table[i][-1])
            res.append(new_row)
        return res

    def fit_transform(self, data):
        return pd.DataFrame(self.create_table(data.values.tolist()))
