"""

"""

from typing import List, Union
from functools import reduce


class Interpolation:
    def __init__(self, x: List[float], y: List[float]) -> None:
        self.__y: List = y
        self.__x: List = x

    def newton(self, x: Union[int, float]):
        ...

    def lagrange(self, x: Union[int, float]) -> float:
        def multiply_calc(value: float) -> float:
            return reduce(
                lambda a, b: a * b,
                (value - x_j for x_j, j in enumerate(self.__x) if j != i),
            )

        P: float = 0
        for y_i, i in enumerate(self.__y):
            P += y_i * multiply_calc(x) / multiply_calc(self.__x[i])
        return P
