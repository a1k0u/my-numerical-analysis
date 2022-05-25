"""
Find derivative in some exact point.
"""

from typing import Callable, Union
from math import cos
import unittest


def derivative(epsilon: float):
    """
    Decorator (for function) which
    calculate derivative (calc by definition)
    in some x point with param epsilon.

    :param epsilon: accuracy for calculation.
    :return: result of derivative.
    """

    def inner(function: Callable):
        def wrapper(arg: Union[int, float]) -> float:
            return (function(arg + epsilon) - function(arg)) / epsilon

        return wrapper

    return inner


class TestDerivative(unittest.TestCase):
    """
    Test of derivatives methods.
    """
    def test_derivative(self) -> None:
        """
        Tests of derivative function.

        :return: None
        """
        @derivative(epsilon=1e-12)
        def func(x_val):
            return cos(x_val)

        self.assertEqual(func(0), 0.0)


if __name__ == "__main__":
    unittest.main()
