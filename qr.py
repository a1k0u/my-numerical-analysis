"""
QR decomposition.

Is a decomposition of a matrix A into
a product A = QR, where Q is orthogonal
matrix and R - upper triangular matrix.

https://en.wikipedia.org/wiki/QR_decomposition
"""

from dataclasses import dataclass
from typing import Union
import numpy as np

Matrix = Union[np.array, np.matrix]


@dataclass
class QR:
    """
    Named storage for some matrix A = QR
    """

    Q: Matrix = None
    R: Matrix = None


def __reshape(A: Matrix, index: int, size: int) -> Matrix:
    """
    Transforms square H_k matrix
    into square with order=size
    """
    E = np.identity(size)
    for i in range(index, size):
        for j in range(index, size):
            E[i, j] = A[i - index, j - index]
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


if __name__ == "__main__":
    my_matrix = np.matrix([[1, 1, 4], [2, 1, 4]])
    my_matrix_qr = decompose_into_qr(my_matrix)
    print(my_matrix_qr.Q @ my_matrix_qr.R)
