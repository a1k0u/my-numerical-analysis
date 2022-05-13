from typing import Callable
from math import cos


def derivative(epsilon: float):
    def inner(function: Callable):
        def wrapper(x) -> float:
            return (function(x + epsilon) - function(x)) / epsilon
        return wrapper
    return inner


@derivative(epsilon=1e-12)
def f(x):
    return cos(x)


print(f(0))
