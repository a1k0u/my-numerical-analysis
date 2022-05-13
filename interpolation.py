"""

"""

from typing import List, Union
from functools import reduce


class Interpolation:
    """ """

    def __init__(self, x_values: List[float], y_values: List[float]) -> None:
        """

        :param x_values:
        :param y_values:
        """
        self.__y: List = y_values
        self.__x: List = x_values

    def newton(self, x: Union[int, float]) -> float:
        """

        :param x:
        :return:
        """
        polynomial: float = self.__y[0]
        for k in range(len(self.__x) - 1):
            x_values_multiply: float = reduce(
                lambda a, b: a * b, (x - self.__x[n_i] for n_i in range(k + 1))
            )

            sep_differences: float = 0
            for j in range(k + 1):
                sep_differences += self.__y[j] / reduce(
                    lambda a, b: a * b,
                    (self.__x[j] - self.__x[l] for l in range(k + 1) if l != j),
                )

            polynomial += sep_differences * x_values_multiply
        return polynomial

    def lagrange(self, x_point: Union[int, float]) -> float:
        """

        :param x_point:
        :return:
        """

        def phi_func_calc(value: float) -> float:
            """

            :param value:
            :return:
            """
            return reduce(
                lambda a, b: a * b,
                (value - x_j for x_j, j in enumerate(self.__x) if j != i),
            )

        polynomial: float = 0
        for y_i, i in enumerate(self.__y):
            polynomial += y_i * phi_func_calc(x_point) / phi_func_calc(self.__x[i])
        return polynomial
