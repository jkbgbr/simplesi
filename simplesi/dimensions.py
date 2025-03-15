from typing import NamedTuple


class Dimensions(NamedTuple):
    kg: float
    m: float
    s: float
    K: float

    @property
    def dimensionsless(self):
        return all(x == 0 for x in self)


class DimensionError(Exception):
    pass


if __name__ == '__main__':  # pragma: no cover
    dl = Dimensions(0, 0, 0, 0)
    print(dl.dimensionsless)
    dl = Dimensions(0, 0, 0, 1)
    print(dl.dimensionsless)
