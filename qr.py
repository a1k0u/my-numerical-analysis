"""
QR decomposition.

Is a decomposition of a matrix A into
a product A = QR, where Q is orthogonal
matrix and R - upper triangular matrix.

https://en.wikipedia.org/wiki/QR_decomposition
"""

from dataclasses import dataclass
from typing import Union, Tuple
import numpy as np

Matrix = Union[np.array, np.matrix]
Complex = Union[float, complex]


@dataclass
class QR:
    """
    Named storage for some matrix A = QR
    """

    Q: Matrix = None
    R: Matrix = None


def __reshape(A: Matrix, start_pos: int, size: int) -> Matrix:
    """
    Transforms square H_k matrix
    into square with order=size

    Example: H -> E

    H = [[1, 2],
         [2, 3]]

    E = [[1, 0, 0],
         [0, 1, 2],
         [0, 2, 3]]
    """
    E = np.identity(size)
    for i in range(start_pos, size):
        for j in range(start_pos, size):
            E[i, j] = A[i - start_pos, j - start_pos]
    return E


def decompose_into_qr(A: Matrix) -> QR:
    """
    Algorithm which decompose A into QR,
    equivalent of np.linalg.qr
    """
    height, width = A.shape
    index = 0

    result = QR()
    result.Q = np.identity(height)
    result.R = A

    while index not in A.shape:
        x = result.R[index:, index]
        if x.shape[0] == 1:
            break

        e, e[0] = x * 0, 1

        u = x + np.linalg.norm(x) * e
        u /= np.linalg.norm(u)

        H = np.identity(x.shape[0]) - 2 * np.outer(u, u)
        H = __reshape(H, index, height)

        result.Q = result.Q @ H.T
        result.R = H @ result.R
        index += 1

    return result


def __process_matrix(A: Matrix, e: float = 1e-6) -> Tuple[Complex, ...]:
    """
    Returns non-multiplies real numbers,
    complex conjugate numbers, and real
    roots of multiplicity 2.
    """
    eigenvalues = set()
    index = 0
    while index < A.shape[0] - 1:
        if A[index + 1][index] < e:
            eigenvalues.add(A[index][index])
            index += 1
        else:
            i = index
            a, b = A[i, i], A[i, i + 1]
            c, d = A[i + 1, i], A[i + 1, i + 1]
            roots = np.roots([1, -a - d, a * d - b * c])
            for root in roots:
                eigenvalues.add(root)
            index += 2
    else:
        if index == A.shape[0] - 1:
            eigenvalues.add(A[index][index])

    return tuple(eigenvalues)


def find_eigenvalues(
    A: Matrix, e: float = 1e-6, iterations: int = 3000
) -> Tuple[Complex, ...]:
    """
    Finds the eigenvalues of a square matrix A with
    accuracy "e" and does ~n iterations to
    find it using QR decomposition.

    After that, __process the matrix to take
    the necessary values.
    """
    height, width = A.shape
    if height != width:
        raise Exception("Matrix isn't square!")

    _A, _B = np.copy(A), np.copy(A)
    difference, index = np.inf, 0

    while difference > e and iterations > index:
        _B = _A
        _B_QR = decompose_into_qr(_B)
        _A = _B_QR.R @ _B_QR.Q

        difference = np.abs(_A - _B).max()
        index += 1

    return __process_matrix(_A, e)


if __name__ == "__main__":
    my_matrix = np.matrix(
        [
            [1, 3, 4, 5, 3],
            [2, 1, 9, 3, 4],
            [7, 3, 2, 5, 8],
            [6, 3, 1, 0, 8],
            [1, 4, 2, 6, 9],
        ]
    )
    my_matrix_qr = decompose_into_qr(my_matrix)
    print(my_matrix_qr.Q @ my_matrix_qr.R)
    print(find_eigenvalues(my_matrix))
