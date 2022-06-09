"""Takes all the spline files and draws them."""

from sys import argv
from matplotlib import pyplot as plt


def separate_data(point: str) -> tuple:
    """Separates the text of points with a space"""
    return tuple(map(float, point.split()))


def read_file(file: str, points: list) -> None:
    """Reads points and inserts it in array"""
    with open(file, "r", encoding="utf-8") as graph:
        for point in graph.readlines():
            points.append(separate_data(point.rstrip()))


def draw_data(points: list, label: str) -> None:
    """Using plt.plot to draw graph"""
    marker = "o" if len(points) == 1 else "."

    plt.plot(
        *zip(*points),
        marker=marker,
        linestyle="dashed",
        linewidth=2,
        markersize=10,
        label=label
    )


def main() -> None:
    if len(argv) == 1:
        exit(-1)
    graphics = argv[-1].split("\n")

    for graphic in graphics:
        points = []
        read_file(graphic, points)
        draw_data(points, label=graphic)

    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
