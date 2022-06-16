from dataclasses import dataclass
from typing import NamedTuple

import matplotlib.pyplot as plt
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

_time = Time(start=0, end=2.5, step=0.01)

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

    print(X_values, _vars.Ay, _vars.Vy)

    e1 = patches.Arc(
        (X_values[0], X_values[2]),
        X_values[2] * 2,
        X_values[2] * 2,
        angle=0,
        theta1=(3 * np.pi / 2 - X_values[3]) * (180 / np.pi),
        theta2=270,
        linewidth=2,
    )

    e2 = patches.Arc(
        (X_values[1], X_values[2]),
        X_values[2] * 2,
        X_values[2] * 2,
        angle=0,
        theta1=270,
        theta2=(3 * np.pi / 2 + X_values[4]) * 180 / np.pi,
        linewidth=2,
    )

    _time.start += _time.step

    pyplot.text(-0.55, 0.365, "time = %.2f s" % _time.start, size="large")
    pyplot.text(X_values[0] + 0.025, X_values[2] + 0.025, "x1")
    pyplot.text(X_values[1] + 0.025, X_values[2] + 0.025, "x2")
    pyplot.plot(X_values[0], X_values[2], "bo")
    pyplot.plot(X_values[1], X_values[2], "bo")
    figure.suptitle(
        "Simulation of the movement of a pneumatic balloon",
        fontsize=14,
        fontweight="bold",
    )
    axis.set_title(
        f"pressure={_data.pressure} Pa, mass={_data.mass} kg, gravity={_data.gravity} m/s",
        style="italic",
    )

    F = _data.pressure * _vars.length - _data.mass * _data.gravity
    direction = 1 if F > 0 else -1
    pyplot.annotate(
        "F=%.2f H" % (F * direction),
        xy=((_vars.Ax + _vars.Bx) / 2, _vars.Ay + 0.05 * direction),
        xytext=((_vars.Ax + _vars.Bx) / 2 - 0.1, _vars.Ay),
        arrowprops=dict(facecolor="orange", shrink=0.0005, width=3, headwidth=9),
    )

    pyplot.xlim([-0.6, 0.6])
    pyplot.ylim([0, 0.4])

    axis.add_patch(e1)
    axis.add_patch(e2)
    camera.snap()

animation = camera.animate()
animation.save("animation.gif", fps=10)
