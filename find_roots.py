"""
    Iterative methods that compute
    approximate solution of a system of equations:

    f1(x0, x1, ..., xn) = 0,
    ...
    fn(x0, x1, ..., xn) = 0.
"""

from typing import Dict, Union
from collections import namedtuple
import unittest
import sympy


def newton(
    variables: sympy.symbols,
    funcs: sympy.sympify,
    start_value: Union[int, float] = 0.5,
    epsilon: float = 1e-12,
) -> Dict[sympy.Symbol, sympy.Float]:

    """
    Newton's Method is an iterative method that computes
    an approximate solution to the system of equations.

    P.S. read sympy documentation.

    :param variables: Names of variables in sympy format;
    :param funcs: System of equations in sympy format;
    :param start_value: A floating point number or an integer that
                        will become the initial value in the iterative
                        method, initially it starts with 0.5;
    :param epsilon: Accuracy of approximation of the result
              of the system of equations. Must be more than zero;
    :return: Dictionary - variable and result of algorithm;
    """
    Properties: namedtuple = namedtuple(
        "Properties", ["amount_vars", "amount_func", "accuracy"]
    )
    _property = Properties(
        len(variables), len(funcs), int(str(epsilon).replace(".", "-").split("-")[1])
    )

    if not epsilon or not _property.amount_vars * _property.amount_func:
        raise ValueError

    jacobi: sympy.Matrix = sympy.zeros(_property.amount_func, _property.amount_vars)
    for i, func in enumerate(funcs):
        for j, var in enumerate(variables):
            jacobi[i, j] = sympy.diff(func, var)

    jacobi_reversed: sympy.Matrix = jacobi.inv()
    x_solution: sympy.Matrix = sympy.Matrix(
        [start_value for _ in range(_property.amount_vars)]
    )
    while ...:
        values = dict(zip(variables, x_solution))
        jacobi_reversed = jacobi_reversed.subs(values)
        funcs_x_result: sympy.Matrix = sympy.Matrix(
            [funcs[i].subs(values) for i in range(_property.amount_func)]
        )

        x_solution = x_solution - jacobi_reversed * funcs_x_result
        if all(
            (abs(funcs_x_result[i]) < epsilon for i in range(_property.amount_vars))
        ):
            break

    return {
        var: round(value, _property.accuracy)
        for var, value in zip(variables, x_solution)
    }


class NewtonTestCase(unittest.TestCase):
    """
    Tests for newton iterative method.
    """

    def test_newton(self) -> None:
        """
        Test function for newton method by unittest.
        :return: None
        """
        function_result: Dict[sympy.Symbol, sympy.Float] = newton(
            sympy.symbols(f"x:{2}"),
            sympy.sympify(["x0**2 + x1**2 - 1", "x0**2 - x1"]),
            epsilon=1e-8,
        )
        my_result: Dict[sympy.Symbol, sympy.Float] = {
            sympy.Symbol("x0"): round(sympy.Float(0.78615137), 8),
            sympy.Symbol("x1"): round(sympy.Float(0.61803399), 8),
        }

        self.assertDictEqual(function_result, my_result)


if __name__ == "__main__":
    unittest.main()
