import numpy as np
from fractions import Fraction


def simplex_iteration(A, basis, b, z_b, r):
    entering_var = find_entering_var(r)
    r = np.array(r)
    while entering_var is not None:
        r = np.array(r)
        print(A)
        print('entering var is', entering_var)
        pivoting_row = find_pivoting_row(A[:, entering_var], b)
        print('pivoting_row', pivoting_row)
        pivoting_col = find_pivoting_col(A[:, basis][pivoting_row])
        print('pivoting_col', pivoting_col)
        pivoting(A, b, pivoting_row, pivoting_col)
        z_b += b[pivoting_row]
        entering_var = find_entering_var(r)
        update_zeta(A, entering_var, pivoting_row, r)
        entering_var = find_entering_var(r)
    return r


def update_zeta(A, entering_var, pivoted_row, r):
    row_to_add = A[pivoted_row, :] * r[entering_var]
    factor = r[entering_var]
    for i in range (0, len(row_to_add)):
        if i == entering_var:
            r[i] = 0
        else:
            r[i] -= A[pivoted_row, i]*factor


def pivoting(A, b, row, col):
    factors = find_factors(A[:, row], col)
    print("factors", factors)

    pivoting_col = A[:, col]
    print("pivoting_col", pivoting_col)

    for i in range(0, len(A[:, 0])):
        if i is not row:
            A[i, :] = A[i, :] - A[row, :] * factors[i]
            b[i] = b[i] - b[row] * factors[i]

    A[row, :] = A[row, :] * factors[row]
    b[row] = b[row] * factors[row]

    return None


def find_factors(pivoting_col, row):
    factors = list(map(lambda x: x / pivoting_col[row], pivoting_col))
    factors[row] = float(1 / pivoting_col[row])
    return factors


def find_entering_var(r):
    for i in range(0, len(r)):
        if r[i] > 0:
            return i
    return None


def find_pivoting_col(A_basis_pivoting_row):
    for j in range(0, len(A_basis_pivoting_row)):
        if A_basis_pivoting_row[j] == 1:
            return j
    return None


def find_pivoting_row(A_j, b):
    min = None
    min_index = -1

    for i in range(0, len(A_j)):
        if A_j[i] > 0:
            tmp_min = b[i] / A_j[i]
            if min is None:
                min = tmp_min
                min_index = i
            elif tmp_min < min:
                min = tmp_min
                min_index = i

    return min_index


@np.vectorize
def apply_vec(f, x):
    return f(x)


frac = lambda x: Fraction(x).limit_denominator(100000)
A = [[3.0, 5.0, 1.0, 0.0], [-1.0, 2.0, 0.0, 1.0]]
A = np.array(A)
print("A=\n",A)
basis = [2, 3]
b = [11.0, 3.0]
c = [1.0, 2.0, 0, 0]
z_b = 0
c = list(map(lambda x: frac(x), c))
print("c=", c)
c = simplex_iteration(A, basis, b, z_b, c)
A = apply_vec(lambda x: frac(x), A)
b = list(map(lambda x: frac(x), b))
c = list(map(lambda x: frac(x), c))
print("A=",A)
print("b=",b)
print("c=",c)
