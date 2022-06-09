"""Validates all data which input in create-spline."""

from sys import argv


def check_number(source: str) -> bool:
    """Checks the ability to convert from string to float"""
    source = source[1:] if source[0] == "-" else source
    return source.replace(".", "", 1).isnumeric()


def validator() -> int:
    """
    Validates input data in spline file,
    where first is number of points and
    after that coordinates
    """
    try:
        with open(argv[1], "r", encoding="utf-8") as file:
            counter = 0
            for line in file.readlines():
                line = line.rstrip()
                data = line.split()

                if not counter and len(data) == 1 and data[0].isnumeric():
                    counter = int(data[0])
                elif (
                    counter
                    and len(data) == 2
                    and all([check_number(el) for el in data])
                ):
                    counter -= 1
                else:
                    return -1
    except FileNotFoundError:
        return -1

    if counter:
        return -1
    return 0


if __name__ == "__main__":
    exit(validator())
