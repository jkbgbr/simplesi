"""
The SI Units: "For all people, for all time"

A module to model four SI base units needed in structural engineering: kg, m, s, K.

"""

from __future__ import annotations

__version__ = "0.1"

from typing import Union, Optional
from simplesi.dimensions import Dimensions
import math
from simplesi import physical_helper_functions as phf

RE_TOL = 1e-9
ABS_TOL = 1e-12

NUMBER = int, float
PRECISION = 1


class Physical:
    """
    A class that defines any physical quantity that can be described
    within the BIPM SI unit system.
    """

    __slots__ = ("value", "dimensions", "precision", "prefixed")

    def __init__(
        self,
        value: float,
        dimensions: Dimensions,
        precision: int = PRECISION,
        prefixed: Optional[str] = None
    ):

        # use a scalar if you have no dimensions
        if dimensions.dimensionsless:
            raise ValueError("Dimensions must be non-zero. Use a scalar instead.")

        """Constructor"""
        super(Physical, self).__setattr__("value", float(value))
        super(Physical, self).__setattr__("dimensions", dimensions)
        super(Physical, self).__setattr__("precision", precision)
        super(Physical, self).__setattr__("prefixed", prefixed)

    ### "Magic" Methods ###

    # def __float__(self):
    #     value = self.value
    #
    #     kg_bool = False
    #     dims = self.dimensions
    #     env_dims = environment.units_by_dimension or dict()
    #     power, _ = phf._powers_of_derived(dims, env_dims)
    #     dim_components = phf._get_unit_components_from_dims(dims)
    #     if len(dim_components) == 1 and dim_components[0][0] == "kg":
    #         kg_bool = True
    #     if self.prefixed:
    #         prefix = self.prefixed
    #     else:
    #         prefix = phf._auto_prefix(value, power, kg_bool)
    #     float_value = phf._auto_prefix_value(value, power, prefix, kg_bool)
    #     return float_value

    # def __int__(self):
    #     return int(float(self))

    def __neg__(self):
        return self * -1

    def __abs__(self):
        if self.value < 0:
            return self * -1
        return self

    def __bool__(self):
        return True

    def __hash__(self):
        return hash(
            (self.value, self.dimensions, self.precision, self.prefixed)
        )

    def __round__(self, n=0):
        return Physical(round(self.value, n), self.dimensions, n, self.prefixed)

    def __contains__(self, other):
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):

        # comparison between Physical and a zero
        if isinstance(other, NUMBER) and other == 0:
            return math.isclose(self.value, 0, rel_tol=RE_TOL)

        # otherwise only compare between Physical instances
        if not isinstance(other, Physical):
            raise ValueError('Can only compare between Physical instances, these are {} = {} and {} = {}.'.format(type(other), other, type(self), self))

        # comparable dimensions
        if self.dimensions == other.dimensions:
            return math.isclose(self.value, other.value)

        else:
            raise ValueError(
                "Can only compare between Physical instances of equal dimension."
            )

    def __gt__(self, other):

        # comparison between Physical and a zero
        if isinstance(other, NUMBER) and other == 0:
            return self.value.__gt__(other)

        # otherwise only compare between Physical instances
        if not isinstance(other, Physical):
            raise ValueError('Can only compare between Physical instances, these are {} = {} and {} = {}.'.format(type(other), other, type(self), self))

        elif self.dimensions == other.dimensions:
            return self.value > other.value

        else:
            raise ValueError(
                "Can only compare between Physical instances of equal dimension or zero."
            )

    def __ge__(self, other):

        # comparison between Physical and a zero
        if isinstance(other, NUMBER) and other == 0:
            return self.value.__ge__(other)

        # otherwise only compare between Physical instances
        if not isinstance(other, Physical):
            raise ValueError('Can only compare between Physical instances, these are {} = {} and {} = {}.'.format(type(other), other, type(self), self))

        if self.dimensions == other.dimensions:
            return self.value >= other.value
        else:
            raise ValueError(
                "Can only compare between Physical instances of equal dimension."
            )

    def __lt__(self, other):

        # comparison between Physical and a zero
        if isinstance(other, NUMBER) and other == 0:
            return self.value.__lt__(other)

        # otherwise only compare between Physical instances
        if not isinstance(other, Physical):
            raise ValueError('Can only compare between Physical instances, these are {} = {} and {} = {}.'.format(type(other), other, type(self), self))

        if self.dimensions == other.dimensions:
            return self.value < other.value
        else:
            raise ValueError(
                "Can only compare between Physical instances of equal dimension."
            )

    def __le__(self, other):

        # comparison between Physical and a zero
        if isinstance(other, NUMBER) and other == 0:
            return self.value.__le__(other)

        # otherwise only compare between Physical instances
        if not isinstance(other, Physical):
            raise ValueError('Can only compare between Physical instances, these are {} = {} and {} = {}.'.format(type(other), other, type(self), self))

        if self.dimensions == other.dimensions:
            return self.value <= other.value
        else:
            raise ValueError(
                "Can only compare between Physical instances of equal dimension."
            )

    def __add__(self, other):

        # addition to 0 is allowed.
        # this will not cause any issues (e.g. no value change)
        # and allows using the sub() method.
        if isinstance(other, NUMBER) and other == 0:
            return self

        # only between Physical instances
        if not isinstance(other, Physical):
            raise ValueError('Can only add between Physical instances, these are {} = {} and {} = {}.'.format(type(other), other, type(self), self))

        # check if dimensions are compatible. If so, add them
        if self.dimensions == other.dimensions:
            return Physical(
                self.value + other.value,
                self.dimensions,
                min(self.precision, other.precision),  # the lower precision is kept
                self.prefixed,
            )
        # dimensions are not compatible
        else:
            raise ValueError(
                f"Cannot add between {self} and {other}: "
                + ".dimensions attributes are incompatible (not equal)"
            )

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        raise ValueError(
            "Cannot incrementally add Physical instances because they are immutable."
            + " Use 'a = a + b', to make the operation explicit."
        )

    def __sub__(self, other):

        # subtracting 0 is allowed.
        if isinstance(other, NUMBER) and other == 0:
            return self

        if not isinstance(other, Physical):
            raise ValueError('Can only subtract between Physical instances, these are {} = {} and {} = {}.'.format(type(other), other, type(self), self))

        if self.dimensions == other.dimensions:

            return Physical(
                self.value - other.value,
                self.dimensions,
                min(self.precision, other.precision),  # the lower precision is kept
                self.prefixed,
            )
        else:
            raise ValueError(
                f"Cannot subtract between {self} and {other}: "
                + ".dimensions attributes are incompatible (not equal)"
            )

    def __rsub__(self, other):

        # only subtracting from 0 is allowed.
        if isinstance(other, NUMBER):
            if other == 0:
                return Physical(
                    -self.value,
                    self.dimensions,
                    self.precision,  # the lower precision is kept
                    self.prefixed,
                )
            else:
                raise ValueError('Can subtract a Physical instance only from zero.')

        else:

            if not isinstance(other, Physical):
                raise ValueError(
                    'Can only subtract between Physical instances, these are {} = {} and {} = {}.'.format(type(other),
                                                                                                          other,
                                                                                                          type(self),
                                                                                                          self))
            return other.__sub__(self)

    def __isub__(self, other):
        raise ValueError(
            "Cannot incrementally subtract Physical instances because they are immutable."
            + " Use 'a = a - b', to make the operation explicit."
        )

    def __mul__(self, other):

        # multiplying by a number e.g. 2 * si.m
        if isinstance(other, NUMBER):
            return Physical(
                self.value * other,
                self.dimensions,
                self.precision,
                self.prefixed,
            )

        # multiplying by another Physical instance, e.g. si.N * si.m
        elif isinstance(other, Physical):
            new_dims = Dimensions(*[x + y for x, y in zip(self.dimensions, other.dimensions)])

            try:
                new_value = self.value * other.value
            except:
                raise ValueError(
                    f"Cannot multiply between {self} and {other}: "
                    + ".value attributes are incompatible."
                )

            # if the result is dimensionless, the value is returned
            if new_dims == Dimensions(0, 0, 0, 0):
                return new_value

            else:
                return Physical(new_value, new_dims, self.precision)
        else:
            raise ValueError(
                f"Cannot multiply between {self} and {other}: "
                + ". Only multiplication by a scalar or a Physical is allowed."
            )

    def __imul__(self, other):
        raise ValueError(
            "Cannot incrementally multiply Physical instances because they are immutable."
            + " Use 'a = a * b' to make the operation explicit."
        )

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):

        if other == 0:
            raise ValueError("Cannot divide by zero.")

        # division by a number e.g. 5 * si.m / 2 = 2.5 * si.m
        if isinstance(other, NUMBER):
            return Physical(
                self.value / other,
                self.dimensions,
                self.precision,
                self.prefixed,
            )

        # division by a Physical instance e.g. 5 * si.m / 2 * si.m = 2.5
        elif isinstance(other, Physical):
            new_dims = Dimensions(*[x - y for x, y in zip(self.dimensions, other.dimensions)])
            try:
                new_value = self.value / other.value
            except:
                raise ValueError(
                    f"Cannot divide between {self} and {other}: "
                    + ".value attributes are incompatible."
                )

            # the result is dimensionless
            if new_dims == Dimensions(0, 0, 0, 0):
                return new_value
            else:
                return Physical(new_value, new_dims, self.precision)
        else:
            raise ValueError(
                f"Cannot divide between {self} and {other}: "
                + ".Only division by a scalar or another Physical is allowed."
            )

    def __rtruediv__(self, other):

        if isinstance(other, NUMBER):
            new_value = other / self.value
            new_dimensions = Dimensions(*[-x for x in self.dimensions])

            return Physical(
                new_value,
                new_dimensions,
                self.precision,
            )
        else:
            try:
                return Physical(
                    other / self.value,
                    Dimensions(*[-x for x in self.dimensions]),
                    self.precision,
                )
            except:
                raise ValueError(
                    f"Cannot divide between {other} and {self}: "
                    + ".value attributes are incompatible."
                )

    def __itruediv__(self, other):
        raise ValueError(
            "Cannot incrementally divide Physical instances because they are immutable."
            + " Use 'a = a / b' to make the operation explicit."
        )

    def __pow__(self, other):

        if isinstance(other, NUMBER):
            if self.prefixed:
                return float(self) ** other
            new_value = self.value**other
            new_dimensions = Dimensions(*[x * other for x in self.dimensions])
            return Physical(new_value, new_dimensions, self.precision)
        else:
            raise ValueError(
                "Cannot raise a Physical to the power of another Physical -> ({}**{})".format(self, other)
            )


# The four SI base units kept
_the_si_base_units = {
    "kg": Physical(1, Dimensions(1, 0, 0, 0), PRECISION),
    "m": Physical(1, Dimensions(0, 1, 0, 0), PRECISION),
    "s": Physical(1, Dimensions(0, 0, 1, 0), PRECISION),
    "K": Physical(1, Dimensions(0, 0, 0, 1), PRECISION),
}
