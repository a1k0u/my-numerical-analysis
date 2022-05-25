"""

"""

from typing import List, Union, Callable, Dict, Tuple
from math import exp, sin, cos, pi
import unittest


def lin_space(start: float, stop: float, n: int):
    """

    :param start:
    :param stop:
    :param n:
    :return:
    """

    if n == 1:
        yield stop
        return
    step = (stop - start) / (n - 1)
    for i in range(n):
        yield start + step * i


def integration(method: Callable, bounds: Tuple, steps: int = 10):
    """

    :param method:
    :param bounds:
    :param steps:
    :return:
    """

    def inner(function: Callable):
        def wrapper(arg: Union[int, float]) -> float:
            points = list(
                lin_space(
                    bounds[0],
                    bounds[1],
                    steps if method.__name__ != quad_gauss.__name__ else 5,
                )
            )
            length = abs(points[0] - points[1])
            return method(function, points, length)

        return wrapper

    return inner


def rectangle(func: Callable, points: list, length: float) -> Union[float, int]:
    """

    :param func:
    :param points:
    :param length:
    :return:
    """

    return sum(func(x - length / 2) for x in points) * length


def trapezium(func: Callable, points: list, length: float) -> Union[float, int]:
    """

    :param func:
    :param points:
    :param length:
    :return:
    """

    return (
        0.5 * func(points[0])
        + sum(func(x) for x in points[1:-1])
        + 0.5 * func(points[-1])
    ) * length


def simpson(func: Callable, points: list, length: float) -> Union[float, int]:
    """

    :param func:
    :param points:
    :param length:
    :return:
    """

    return (
        (
            func(points[0])
            + 4 * sum(points[1::2])
            + 2 * sum(points[2::2])
            + func(points[-1])
        )
        * length
        / 3
    )


def quad_gauss(func: Callable, points: list, length: float) -> Union[float, int]:
    """

    :param func:
    :param points:
    :param length:
    :return:
    """

    left, right = points[0], points[-1]
    values: Dict[str, List] = {
        "c": [0.236927, 0.236927, 0.478629, 0.478629, 0.568889],
        "x": [x * (right - left) / 2 + (left + right) / 2 for x in points],
    }

    return (
        (right - left) / 2 * sum(c * func(x) for c, x in zip(values["c"], values["x"]))
    )


class TestIntegration(unittest.TestCase):
    def test_integration(self) -> None:

        @integration(rectangle, (0, 1), steps=100)
        def foo(x: float) -> float:
            return exp(x)

        @integration(trapezium, (-pi/2, pi/2), steps=200)
        def bar(x: float) -> float:
            return sin(x)

        @integration(simpson, (-pi, pi), steps=300)
        def spam(x: float) -> float:
            return cos(x)

        @integration(quad_gauss, (3, 5), steps=5)
        def egg(x: float) -> float:
            return x ** 2 + 1

        print(trapezium(5))


if __name__ == "__main__":
    unittest.main()
