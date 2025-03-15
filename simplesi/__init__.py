"""
The SI Units: "For all people, for all time"

A module to model four SI base units needed in structural engineering: kg, m, s, K.

"""

from __future__ import annotations

__version__ = "0.1"

import math
import pprint
from typing import Optional
from simplesi.dimensions import Dimensions
from simplesi import physical_helper_functions as phf

RE_TOL = 1e-9
ABS_TOL = 1e-12

NUMBER = int, float
PRECISION = 3


class Physical:
    """
    An SI class for representing structural physical quantities.
    """

    __slots__ = ("value", "dimensions", "precision", "prefixed")

    def __init__(
            self,
            value: float,
            dimensions: Dimensions,
            precision: int = PRECISION,
            prefixed: Optional[str] = False
    ):

        # being strict about the input makes life easier later
        if not isinstance(value, NUMBER):
            raise ValueError("Value must be a number.")

        if not isinstance(precision, int):
            raise ValueError("Precision must be an integer.")

        # use a scalar if you have no dimensions
        if dimensions.dimensionsless:
            raise ValueError("Dimensions must be non-zero. Use a scalar instead.")

        self.value = value
        self.dimensions = dimensions
        self.precision = precision
        self.prefixed = prefixed

    def __str__(self):
        """a pretty print of the Physical instance"""
        unit = environment.preferred_units.get(self.dimensions, None)

        if unit is None:
            return '{} {}'.format(self.value, self.dimensions)
        else:
            return self.to(unit)

    def __repr__(self):
        """
        Returns a traditional Python string representation of the Physical instance.
        """
        return "Physical(value={}, dimensions={}, precision={}, prefixed={})".format(self.value,
                                                                                     self.dimensions,
                                                                                     self.precision,
                                                                                     self.prefixed)

    def to(self, unit: str = None):
        """
        Prints the Physical instance to the specified unit.
        DOES NOT CHANGE ANYTHING, just prints.

        Does multiple checks to ensure the result is correct:
        - the requested unit is compatible with the dimensions of the Physical instance
        - the requested unit is available in the environment
        - the requested unit has a Value defined
        Latter two tests check the environment definition.

        """
        value = self.value

        # looking for the symbol in the environment
        env = environment.environment
        possible_units = {k: v for k, v in env.items() if v['Dimension'] == self.dimensions}

        # if the requested unit is not compatible with the dimensions defined in the environment,
        # the requested unit does not show up in the possible_units dictionary
        # raise an error
        if unit is not None:
            if unit not in possible_units.keys():
                raise ValueError('The requested unit is not compatible with the dimensions of the Physical instance.')

        # if nothing was found - it is not possible as self must have a unit from the environment but still
        # check for it
        if not possible_units:
            raise ValueError('No units found for the given dimensions. This should not be possible!')

        # finding the requested unit
        available = {k: v for k, v in possible_units.items() if v.get('Symbol') == unit}

        # is the requested unit available? If not, give the possible alternatives
        if not available:
            _list = ', '.join([v.get('Symbol', k) for k, v in possible_units.items()])
            print('No units found for the given unit "{}". Possible units are: {}'.format(unit, _list))
            return

        if len(available) > 1:
            raise ValueError('More than one unit found for the given dimensions.')

        else:
            # last check: if the unit is found, but the value is missing, raise an error
            try:
                new_value = round(value / available[unit].get('Value', 0), self.precision)
            except ZeroDivisionError as e:
                raise ValueError('Incorrect unit definition: "Value" missing!')
            return '{} {}'.format(new_value, available[unit].get('Symbol', ''))

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

    def _check_other(self, other, operation: str):

        if not isinstance(other, Physical):
            raise ValueError(
                f"Can only {operation} between Physical instances, these are {type(other)} = {other} and {type(self)} = {self}"
            )

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
        self._check_other(other, "__eq__")

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

        # compare only between Physical instances
        self._check_other(other, "__gt__")

        if self.dimensions == other.dimensions:
            return self.value > other.value

        else:
            raise ValueError(
                "Can only compare between Physical instances of equal dimension or zero."
            )

    def __ge__(self, other):

        # comparison between Physical and a zero
        if isinstance(other, NUMBER) and other == 0:
            return self.value.__ge__(other)

        # compare only between Physical instances
        self._check_other(other, "__ge__")

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

        # compare only between Physical instances
        self._check_other(other, "__lt__")

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

        # compare only between Physical instances
        self._check_other(other, "__le__")

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

        # compare only between Physical instances
        self._check_other(other, "__add__")

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
                + "dimensions are incompatible"
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

        # compare only between Physical instances
        self._check_other(other, "__sub__")

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
                + ".dimensions are incompatible"
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
            # compare only between Physical instances
            self._check_other(other, "__rsub__")
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

        # compare only between Physical instances
        self._check_other(other, "__mul__")

        # multiplying by another Physical instance, e.g. si.N * si.m
        new_dims = Dimensions(*[x + y for x, y in zip(self.dimensions, other.dimensions)])
        new_value = self.value * other.value
        new_precision = min(self.precision, other.precision)

        # if the result is dimensionless, the value is returned
        if new_dims.dimensionsless:
            return new_value
        else:
            return Physical(new_value, new_dims, new_precision)

    def __imul__(self, other):
        raise ValueError(
            "Cannot incrementally multiply Physical instances because they are immutable."
            + " Use 'a = a * b' to make the operation explicit."
        )

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):

        if isinstance(other, NUMBER):
            if other == 0:
                raise ZeroDivisionError("Cannot divide by zero.")

            # division by a number e.g. 5 * si.m / 2 = 2.5 * si.m
            return Physical(
                self.value / other,
                self.dimensions,
                self.precision,
                self.prefixed,
            )

        # compare only between Physical instances
        self._check_other(other, "__truediv__")

        # division by a Physical instance e.g. 5 * si.m / 2 * si.m = 2.5
        new_dims = Dimensions(*[x - y for x, y in zip(self.dimensions, other.dimensions)])
        try:
            new_value = self.value / other.value
        except ZeroDivisionError:
            raise ZeroDivisionError("Cannot divide by zero.")

        # the result is dimensionless
        if new_dims.dimensionsless:
            return new_value
        else:
            return Physical(new_value, new_dims, self.precision)

    def __rtruediv__(self, other):

        # only zero can be divided by a Physical.
        if isinstance(other, NUMBER):
            if other == 0:
                return Physical(
                    0,
                    self.dimensions,
                    self.precision,  # the lower precision is kept
                    self.prefixed,
                )
            else:
                raise ValueError('Can divide with a Physical only zero.')

        else:
            # compare only between Physical instances
            self._check_other(other, "__rtruediv__")
            return other.__truediv__(self)

    def __itruediv__(self, other):
        raise ValueError(
            "Cannot incrementally divide Physical instances because they are immutable."
            + " Use 'a = a / b' to make the operation explicit."
        )

    def __pow__(self, other):

        if isinstance(other, NUMBER):
            # if self.prefixed:
            #     return float(self) ** other
            new_value = self.value ** other

            new_dimensions = Dimensions(*[x * other for x in self.dimensions])
            if new_dimensions.dimensionsless:
                return new_value

            return Physical(new_value, new_dimensions, self.precision)

        else:
            raise ValueError(
                "Cannot raise a Physical to the power of another Physical -> ({}**{})".format(other, self)
            )

    def __rpow__(self, other):
        raise ValueError(
            "Cannot raise a Physical to the power of another Physical -> ({}**{})".format(other, self)
        )


# The seven SI base units
base_units = {
    "kg": Physical(1, Dimensions(1, 0, 0, 0, 0, 0, 0), PRECISION),
    "m": Physical(1, Dimensions(0, 1, 0, 0, 0, 0, 0), PRECISION),
    "s": Physical(1, Dimensions(0, 0, 1, 0, 0, 0, 0), PRECISION),
    "A": Physical(1, Dimensions(0, 0, 0, 1, 0, 0, 0), PRECISION),
    "cd": Physical(1, Dimensions(0, 0, 0, 0, 1, 0, 0), PRECISION),
    "K": Physical(1, Dimensions(0, 0, 0, 0, 0, 1, 0), PRECISION),
    "mol": Physical(1, Dimensions(0, 0, 0, 0, 0, 0, 1), PRECISION),
}

# preferred units
preferred = {
    Dimensions(0, 1, 0, 0, 0, 0, 0): 'mm',
    Dimensions(0, 0, 1, 0, 0, 0, 0): 's',
    Dimensions(1, 0, 0, 0, 0, 0, 0): 'kg',
    Dimensions(1, 1, -2, 0, 0, 0, 0): 'kN',
    Dimensions(1, 2, -2, 0, 0, 0, 0): 'kNm',
    Dimensions(1, -1, -2, 0, 0, 0, 0): 'MPa',
}

from simplesi.environment import Environment

environment = Environment(base_units=base_units, preferred_units=preferred)
