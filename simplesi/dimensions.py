from typing import NamedTuple


class Dimensions(NamedTuple):
    kg: float
    m: float
    s: float
    A: float
    cd: float
    K: float
    mol: float

    @property
    def dimensionsless(self):
        return all(x == 0 for x in self)


if __name__ == '__main__':  # pragma: no cover
    dl = Dimensions(0, 0, 0, 0, 0, 0, 0)
    print(dl.dimensionsless)
    dl = Dimensions(0, 0, 0, 1, 0, 0, 0)
    print(dl.dimensionsless)
