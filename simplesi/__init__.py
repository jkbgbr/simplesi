"""
The SI Units: "For all people, for all time"

A module to simply model SI base units.

"""

from __future__ import annotations

__version__ = "0.1"

import math

from simplesi.dimensions import Dimensions

RE_TOL = 1e-9
ABS_TOL = 1e-12

NUMBER = int, float
PRECISION = 3


class Physical:
    """
    An SI class for representing structural physical quantities.
    """

    __slots__ = ("value", "dimensions", "precision", "conv_factor")

    def __init__(
            self,
            value: float,
            dimensions: Dimensions,
            precision: int = PRECISION,
            conv_factor: float = 1.0,
    ):
        """


        :param value: How many pieces of this unit. Non-SI units are converted to the SI unit of the same dimensionality when instantiated.
        e.g. 1 ft = 0.3048 m -> value = n x 0.3048
        :param dimensions: dimensionality
        :param precision:
        :param conv_factor: number of base SI units in this unit. e.g. 1 ft = 0.3048 m -> conv_factor = 0.3048
        """

        # being strict about the input makes life easier later
        if not isinstance(value, NUMBER):
            raise ValueError("Value must be a number, you have {}.".format(type(value)))

        if not isinstance(conv_factor, NUMBER):
            raise ValueError("Conversion factor must be a number, you have {}.".format(type(conv_factor)))

        if conv_factor <= 0:
            raise ValueError("Conversion factor must be positive, you have {}.".format(conv_factor))

        if not isinstance(precision, int):
            raise ValueError("Precision must be an integer,you have {}.".format(type(precision)))

        # use a scalar if you have no dimensions
        if dimensions.dimensionsless:
            raise ValueError("Dimensions must be non-zero. Use a scalar instead.")

        self.value = value
        self.dimensions = dimensions
        self.precision = precision
        self.conv_factor = conv_factor

    def __str__(self):
        """A pretty print of the Physical instance"""

        # checking if there is a preferred unit for the dimensions
        unit = {k for k, v in environment.preferred_units.items() if v == self.dimensions}
        unit = unit.pop() if unit else None

        # if there is no preferred unit, use the smallest available from the environment
        if unit is None:
            # possible units, ascending order

            unit = tuple(k for k, v in sorted(self.all_units.items(), key=lambda x: x[1].get('Value') * x[1].get('Factor')) if
                         v.get('Dimension') == self.dimensions)

            if not unit:
                raise ValueError('No units found for the dimensions {}.'.format(self.dimensions))

            # using the unit as set
            printsetting = environment.settings.get('print_unit', None)
            if printsetting == 'smallest':
                unit = unit[0]
            elif printsetting == 'largest':
                unit = unit[-1]
            else:
                unit = unit[0]

        return self.to(unit)

    def __repr__(self):
        """
        Returns a traditional Python string representation of the Physical instance.
        """
        return "Physical(value={}, dimensions={}, precision={}, conv_factor={})".format(self.value,
                                                                                        self.dimensions,
                                                                                        self.precision,
                                                                                        self.conv_factor)

    @property
    def keep_SI(self):
        """shortcut to the environment setting"""
        return environment.settings.get('keep_SI', True)

    @property
    def is_SI(self):
        """True, if the unit is an SI unit"""
        return self.conv_factor == 1.0

    @property
    def all_units(self):
        """Returns an environment-like dict made from environment.environment and the base si units"""
        # the base SI units
        env = {k: {'Dimension': v.dimensions, 'Factor': v.conv_factor, 'Symbol': k, "Value": v.value} for k, v in
               environment.si_base_units.items()}
        env.update(environment.environment)
        return env

    def to(self, unit: str = None):
        """
        Prints the Physical instance to the specified unit.
        DOES NOT CHANGE ANYTHING, just prints.

        Does multiple checks to ensure the result is correct:
        - the requested unit is compatible with the dimensions of the Physical instance
        - the requested unit is available in the environment
        - the requested unit has a Value defined
        Latter two tests check the environment definition.

        :param unit: from the environment either the key or the symbol of a unit
        :return:
        """
        value = self.value

        # looking for the symbol in the environment
        env = self.all_units
        possible_units = {k: v for k, v in env.items() if v['Dimension'] == self.dimensions}

        # if the requested unit is not compatible with the dimensions defined in the environment,
        # the requested unit does not show up in the possible_units dictionary
        # we both check the keys and the symbols
        # raise an error
        keys = list(possible_units.keys())
        symbols = list(x.get('Symbol') for x in possible_units.values())
        keys_and_symbols = keys + symbols

        if unit is not None:
            if unit not in keys_and_symbols:
                raise ValueError(
                    'The requested unit is not compatible with the dimensions of the Physical instance or not defined in this environment.')

        # if nothing was found - it is not possible as self must have a unit from the environment but still
        # check for it
        if not possible_units:
            raise ValueError('No units found for the given dimensions. This should not be possible!')

        # finding the requested unit
        available = {k: v for k, v in possible_units.items() if v.get('Symbol') == unit or k == unit}

        # is the requested unit available? If not, give the possible alternatives
        if not available:
            _list = ', '.join(['"{}"'.format(v.get('Symbol', k)) for k, v in possible_units.items()])
            print('No unit for conversion defined. Compatible units are: {}'.format(_list))
            return

        # this should not be possible for many reasons but still
        if len(available) > 1:
            raise ValueError('More than one unit found for the given dimensions. This means, symbols and keys in the environment are used multiple times.')

        # finally, the unit is found and we are sure there is only one
        # but maybe we found it by the symbol -> let's find the unit
        if available.get(unit, None) is None:
            unit = list(available.keys())[0]

        # last check: if the unit is found, but the value is missing, raise an error
        # this should not happen as we check for the existence of the value in the environment but still
        _value = available[unit].get('Value', 1)
        _factor = available[unit].get('Factor', 1)
        _symbol = available[unit].get('Symbol', '')

        divider = _value * _factor
        new_value = round(value / divider, self.precision)
        return '{} {}'.format(new_value, _symbol)

    ### "Magic" Methods ###

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
            (self.value, self.dimensions, self.precision, self.conv_factor)
        )

    def __round__(self, n=0):
        return Physical(round(self.value, n), self.dimensions, n, self.conv_factor)

    def __contains__(self, other):
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):

        # comparison between Physical and a zero
        if isinstance(other, NUMBER) and other == 0:
            return math.isclose(self.value, 0, rel_tol=RE_TOL, abs_tol=ABS_TOL)

        # otherwise only compare between Physical instances
        self._check_other(other, "__eq__")

        # comparable dimensions
        if self.dimensions == other.dimensions:
            return math.isclose(self.value, other.value, rel_tol=RE_TOL, abs_tol=ABS_TOL)

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
            return self.value * self.conv_factor > other.value * other.conv_factor

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
            return self.value * self.conv_factor >= other.value * other.conv_factor
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
            return self.value * self.conv_factor < other.value * other.conv_factor
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
            return self.value * self.conv_factor <= other.value * other.conv_factor
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

            new_value = self.value + other.value
            new_factor = self.conv_factor

            return Physical(
                new_value,
                self.dimensions,
                min(self.precision, other.precision),  # the lower precision is kept
                new_factor,
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

            new_value = self.value - other.value
            new_factor = self.conv_factor

            return Physical(
                new_value,
                self.dimensions,
                min(self.precision, other.precision),  # the lower precision is kept
                new_factor,
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
                    self.conv_factor,
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
                self.conv_factor,
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
                self.conv_factor,
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

        if isinstance(other, NUMBER):

            return Physical(
                other / self.value,
                Dimensions(*[-x for x in self.dimensions]),
                self.precision,  # the lower precision is kept
                self.conv_factor,
            )

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

    def sqrt(self):
        """
        square root, as math.sqrt raises a TypeError
        """
        return self ** 0.5

    def root(self, n: NUMBER = 2):
        """
        nth root, as math.pow raises a TypeError
        """
        return self ** (1 / n)


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
# the preferred units are used to print the Physical instances so usually the most common units are used
# the VALUES must beunique, but this is checked for in the environment file
preferred_units = {
    'mm': Dimensions(0, 1, 0, 0, 0, 0, 0),
    's': Dimensions(0, 0, 1, 0, 0, 0, 0),
    'kg': Dimensions(1, 0, 0, 0, 0, 0, 0),
    'kN': Dimensions(1, 1, -2, 0, 0, 0, 0),
    'kNm': Dimensions(1, 2, -2, 0, 0, 0, 0),
    'MPa': Dimensions(1, -1, -2, 0, 0, 0, 0),
}

# # dump the perferred units in an utf-8 json file
# import json
# with open('preferred_units.json', 'w', encoding='utf-8') as f:
#     json.dump(preferred, f, ensure_ascii=True)

environment_settings = {
    'print_unit': 'smallest',  # smallest, largest
    'keep_SI': True,  # if True, operations on SI and non-SI units return the result to SI units
}

from simplesi.environment import Environment

environment = Environment(si_base_units=base_units, preferred_units=preferred_units, settings=environment_settings)
