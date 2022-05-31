"""
Numerical integration comprises a broad family
of algorithms for calculating the numerical
value of a definite integral.

Here you'll find Rectangle, Trapezium,
Simpson and Gauss methods.

See more about methods here:
https://en.wikipedia.org/wiki/Numerical_integration
"""

from typing import List, Union, Callable, Dict, Tuple, Generator
from math import exp


def lin_space(start: float, stop: float, n: int) -> Generator:
    """
    The equivalent of `linspace` in numpy (see docs).
    Divide numerical interval from start to stop by n parts.

    start ~ a, stop ~ b
    [a, b] / n, where a=1, b=5, n=5 -> [1, 2, 3, 4, 5]

    :param start: point, where we'll start
    :param stop: end of interval
    :param n: parts of interval
    :return: generator of points
    """

    if n == 1:
        yield stop
        return
    step = (stop - start) / (n - 1)
    for i in range(n):
        yield start + step * i


def integration(method: Callable, bounds: Tuple, steps: int = 10):
    """
    Decorator for function, which integrate your function.
    Get method(rectangle, trapezium, simpson, quad_gauss),
    bounds, where a < b, and accuracy.

    >> @integration(trapezium, (0, 1), steps=100)
    >> def foo(x: float) -> float:
    >>    return exp(x)
    >>
    >> foo() # 1.7 ...

    :param method: integrate func
    :param bounds: (a, b), a < b | int or float
    :param steps: int
    :return: calculating the numerical
             value of a definite integral
    """

    if bounds[0] > bounds[1]:
        raise Exception(
            f"Left(={bounds[0]}) bound have to be more than right(={bounds[1]})!"
        )

    def inner(function: Callable):
        def wrapper(arg: Union[int, float] = 0) -> float:
            """
            Divide interval in n(=step) points,
            then calculate length between two points
            and call function(=method).
            """

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
    return sum(func(x - length / 2) for x in points) * length


def trapezium(func: Callable, points: list, length: float) -> Union[float, int]:
    return (
        0.5 * func(points[0])
        + sum(func(x) for x in points[1:-1])
        + 0.5 * func(points[-1])
    ) * length


def simpson(func: Callable, points: list, length: float) -> Union[float, int]:
    return (
        (
            func(points[0])
            + sum(
                4 * func(points[i]) if i % 2 else 2 * func(points[i])
                for i in range(1, len(points) - 1)
            )
            + func(points[-1])
        )
        * length
        / 3
    )


def quad_gauss(func: Callable, points: list, length: float) -> Union[float, int]:
    left, right = points[0], points[-1]
    root_polynomial_legendre = [0.906180, -0.906180, 0.538469, -0.538469, 0]
    values: Dict[str, List] = {
        "c": [0.236927, 0.236927, 0.478629, 0.478629, 0.568889],
        "x": [x * (right - left) / 2 + (left + right) / 2 for x in root_polynomial_legendre],
    }

    return (
        (right - left) / 2 * sum(c * func(x) for c, x in zip(values["c"], values["x"]))
    )


@integration(trapezium, (0, 1), steps=100)
def foo(x: float) -> float:
    return exp(x)


if __name__ == "__main__":
    print(f"integrate exp from 0 to 1 = {foo()}")
