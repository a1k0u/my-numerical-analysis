"""
Interpolation is a type of estimation,
a method of constructing new data points
based on the range of a discrete
set of known data points.
"""

from typing import List, Union
from functools import reduce


class Interpolation:
    """
    Calculate new points by set of known points.

    In this class realised newton
    and lagrange methods, which
    calculate new points.

    Firstly, init instance of class.
    >> x_values = [1, 2, 3]
    >> y_values = [44, -10, 100]
    >> function = Interpolation(x_values, y_values)

    After that you are able to call
    any method (newton, lagrange) by
    some x point and get f(x).

    >> function.newton(3) # get some float result
    >> function.lagrange(5)

    >> y_values = [function.newton(x) for x in range(100)]
    """

    def __init__(self, x_values: List[float], y_values: List[float]) -> None:
        """
        Initialization your function
        with known data points.

        >> len(x_values) == len(y_values) # True
        Here's has to be bijection between X and Y.

        :param x_values: list of X values
        :param y_values: list of f(X) values
        """

        if len(y_values) != len(x_values):
            raise ValueError("Lengths of arrays must be equal!")

        self.__y: List = y_values
        self.__x: List = x_values

    def newton(self, point: Union[int, float]) -> float:
        """
        Calculate new point by Newton polynomial.
        Function gets x and returns f(x).

        :param point: find function result at point
        :return: f(point)
        """

        polynomial: float = self.__y[0]
        for k in range(len(self.__x) - 1):
            x_values_multiply: float = reduce(
                lambda a, b: a * b, (point - self.__x[n_i] for n_i in range(k + 1))
            )

            sep_differences: float = 0
            for j in range(k + 1):
                sep_differences += self.__y[j] / reduce(
                    lambda a, b: a * b,
                    (self.__x[j] - self.__x[l] for l in range(k + 1) if l != j),
                )

            polynomial += sep_differences * x_values_multiply
        return polynomial

    def lagrange(self, point: Union[int, float]) -> float:
        """
        Calculate new point by Lagrange polynomial.
        Function gets x and returns f(x).

        :param point: find function result at point
        :return: f(point)
        """

        def phi_func_calc(value: Union[int, float], index: int) -> float:
            """
            Calculate phi function
            in lagrange polynomial.

            :param index: index of loop in lagrange
            :param value: argument for phi
            :return: result of phi function
            """

            return reduce(
                lambda a, b: a * b,
                (value - x_j for x_j, j in enumerate(self.__x) if j != index),
            )

        polynomial: float = 0
        for y_i, i in enumerate(self.__y):
            polynomial += y_i * phi_func_calc(point, i) / phi_func_calc(self.__x[i], i)
        return polynomial
