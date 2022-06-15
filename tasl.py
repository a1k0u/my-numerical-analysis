from dataclasses import dataclass
from typing import NamedTuple

import numpy as np
from matplotlib import patches, pyplot
from celluloid import Camera


class PhysicProperties(NamedTuple):
    pressure: float
    gravity: float
    mass: float
    tau: float
    epsilon: float


@dataclass
class Time:
    start: float
    end: float
    step: float


@dataclass
class Variables:
    length: float
    start_x: float
    funcs: int
    Ax: float
    Bx: float
    Ay: float
    By: float
    Vy: float
    C: float


def functions(arguments: np.array, consts: Variables) -> np.array:
    x1, x2, y, f1, f2 = arguments
    return np.array(
        [
            x1 + y * np.cos(3 * np.pi / 2 - f1) - consts.Ax,
            x2 + y * np.cos(3 * np.pi / 2 + f2) - consts.Bx,
            y + y * np.sin(3 * np.pi / 2 - f1) - consts.Ay,
            (f1 + f2) * y + (x2 - x1) - consts.C,
            y + y * np.sin(3 * np.pi / 2 + f2) - consts.By,
        ]
    )


_data = PhysicProperties(pressure=2000, gravity=9.8, mass=100, tau=0.005, epsilon=0.001)

_time = Time(start=0, end=1, step=0.01)

_vars = Variables(
    length=0,
    start_x=0.5,
    funcs=5,
    Ax=-0.353,
    Bx=0.353,
    Ay=0.3,
    By=0.3,
    C=3 * np.pi / 8,
    Vy=0.5,
)

X_values = np.array([_vars.start_x for _ in range(_vars.funcs)])

figure, axis = pyplot.subplots()
camera = Camera(figure)

while _time.start < _time.end:

    _vars.Ay = _vars.Ay + _vars.Vy * _time.step
    _vars.By = _vars.Ay

    while ...:
        F_values = functions(X_values, _vars)
        X_values = X_values - F_values * _data.tau

        if all([abs(el) < _data.epsilon for el in F_values]):
            break

    _vars.length = X_values[1] - X_values[0]

    _vars.Vy = (
        _vars.Vy
        + (1 / _data.mass)
        * (_data.pressure * _vars.length - _data.mass * _data.gravity)
        * _time.step
    )

    print(X_values)

    e1 = patches.Arc(
        (_vars.length / 2, _vars.Ay / 2),
        _vars.length,
        _vars.Ay,
        theta1=X_values[3],
        theta2=X_values[4],
    )

    axis.add_patch(e1)
    _time.start += _time.step
    camera.snap()


animation = camera.animate()
animation.save("animation.gif", writer="Pillow", fps=10)
