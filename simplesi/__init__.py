"""
The SI Units: "For all people, for all time"

A module to simply model SI base units.

"""

from __future__ import annotations

__version__ = "0.1"

import math
import pprint

from simplesi.dimensions import Dimensions

RE_TOL = 1e-9
ABS_TOL = 1e-12

NUMBER = int, float


class Physical:
    """
    An SI class for representing structural physical quantities.
    """

    __slots__ = ("value", "dimensions", "conv_factor")

    def __init__(
            self,
            value: float,
            dimensions: Dimensions,
            conv_factor: float = 1.0,
    ):
        """


        :param value: How many pieces of this unit. Non-SI units are converted to the SI unit of the same dimensionality when instantiated.
        e.g. 1 ft = 0.3048 m -> value = n x 0.3048
        :param dimensions: dimensionality
        :param conv_factor: number of base SI units in this unit. e.g. 1 ft = 0.3048 m -> conv_factor = 0.3048
        """

        # being strict about the input makes life easier later
        if not isinstance(value, NUMBER):
            raise ValueError("Value must be a number, you have {}.".format(type(value)))

        if not isinstance(conv_factor, NUMBER):
            raise ValueError("Conversion factor must be a number, you have {}.".format(type(conv_factor)))

        if conv_factor <= 0:
            raise ValueError("Conversion factor must be positive, you have {}.".format(conv_factor))

        # use a scalar if you have no dimensions
        if dimensions.dimensionsless:
            raise ValueError("Dimensions must be non-zero. Use a scalar instead.")

        self.value = value
        self.dimensions = dimensions
        self.conv_factor = conv_factor

    def __call__(self, unit: str) -> PhysRep:
        """Returns the value in the given unit as a PhysRep instance"""
        return self._repr(unit)

    @classmethod
    def as_str(cls, value: NUMBER) -> str:
        """Returns the value as a string with N significant digits"""

        if not isinstance(value, NUMBER):
            raise ValueError("Value must be a number, you have {}.".format(type(value)))

        # essentially an integer
        if float(value) == int(value):
            return str(int(value))

        # it is truly a float
        # formatting to N significant digits
        _ret1 = '{:.{}g}'.format(value, environment.settings.get('significant_digits'))
        # formatting to at least 2 deciman spaces
        _ret2 = '{:.{}f}'.format(value, min(2, environment.settings.get('significant_digits')))

        # making sure scientific notation does not kick in
        if any(x in _ret1 for x in '+-'):
            _ret1 = '0'

        # returning the "longest" number
        return sorted([_ret1, _ret2], key=lambda x: len(x))[-1]

    def __str__(self):
        """A pretty print of the Physical instance"""

        # checking if there is a preferred unit for the dimensions
        unit = {k for k, v in environment.preferred_units.items() if v == self.dimensions}
        unit = unit.pop() if unit else None

        # if there is no preferred unit, use the smallest or largest available from the environment
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
        return "Physical(value={}, dimensions={}, conv_factor={})".format(self.value,
                                                                          self.dimensions,
                                                                          self.conv_factor)

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

    def _repr(self, unit: str) -> PhysRep:
        """
        Representation of the Physical instance in the given unit, as a pair of value, unit.
        THIS IS NOT A SRTING, but a glorified NamedTuple.
        """
        u = self.to(unit)  # getting the string representation
        rep = split_str(u)  # splitting it into value and unit, both strings

        return PhysRep(*rep)

    def to(self, unit: str = None) -> str:
        """
        Prints the Physical instance to the specified unit.
        DOES NOT CHANGE ANYTHING, just prints and returns a string.

        Does multiple checks to ensure the result is correct:
        - the requested unit is compatible with the dimensions of the Physical instance
        - the requested unit is available in the environment
        - the requested unit has a Value defined
        Latter two tests check the environment definition.

        :param unit: from the environment either the key or the symbol of a unit
        :return:
        """

        def print_or_raise():
            # either print it or raise an exception, based on the setting
            if environment.settings.get('to_fails') == 'print':
                # print it by the dimensions
                # results something like 1.73 kg⁰‧⁵ × m⁰‧⁵ × s⁻¹‧⁰
                _ret = []
                for u, ex in zip(environment.si_base_units.keys(), self.dimensions):  # SI base unit, exponent
                    # getting rid of unnecessary zeros
                    try:
                        ex.is_integer()
                        ex = int(ex)
                    except AttributeError:
                        pass
                    if ex == 0:  # u^ex = 1 removed
                        continue
                    elif ex == 1:  # ex = 1 -> simply the SI base unit
                        _ret.append('{}'.format(u))
                    else:  # the exponent is shown
                        _superex = []
                        _superscripts = "⁰¹²³⁴⁵⁶⁷⁸⁹"
                        _minus = "⁻"
                        for x in str(ex):
                            if x == '-':
                                _superex.append(_minus)
                            elif x == '.':
                                _superex.append('\u2027')  # dot in the exponent
                            else:
                                _superex.append(_superscripts[int(x)])
                        ex = ''.join(_superex)
                        _ret.append('{}{}'.format(u, ex))

                return self.as_str(self.value) + ' \u00d7 '.join(_ret)
                return "{} ".format(self.value) + ' \u00d7 '.join(_ret)

            elif environment.settings.get('to_fails') == 'raise':

                raise ValueError(
                    'Conversion not possible. Possible values to use are: {}'.format(
                        possible_units))

        value = self.value

        # looking for the units in the environment that have the same dimensionality
        env = self.all_units
        units_same_dims = {k: v for k, v in env.items() if v['Dimension'] == self.dimensions}

        # going over the units with same dims, looking for the desired unit in the keys and symbols
        keys = list(units_same_dims.keys())
        symbols = list(x.get('Symbol') for x in units_same_dims.values())
        keys_and_symbols = sorted(set(keys + symbols))
        possible_units = ', '.join('"{}"'.format(x) for x in keys_and_symbols)

        # there is a unit given as argument to print self in
        if unit is not None:  # a unit is provided to print self in
            # the unit is not found in the environment
            if unit not in keys_and_symbols:

                # either print the value or raise an exception
                # either print the value or raise an exceptionprint
                if environment.settings.get('to_fails') == 'raise':
                    raise ValueError(
                        'Conversion not possible. Possible values to use are: {}'.format(
                            possible_units))
                elif environment.settings.get('to_fails') == 'print':
                    print(
                        'Conversion not possible. Possible values to use are: {}'.format(
                            possible_units))

            else:  # the requested unit was found
                # finding the requested unit
                available = {k: v for k, v in units_same_dims.items() if v.get('Symbol') == unit or k == unit}

                # is the requested unit available? If not, give the possible alternatives
                if not available:
                    _list = ', '.join(['"{}"'.format(v.get('Symbol', k)) for k, v in units_same_dims.items()])
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
                new_value = value / divider

                return '{} {}'.format(self.as_str(new_value), _symbol)

        else:  # no unit is provided to print self in

            # no units available in the environment
            if not units_same_dims:
                # either print the value or raise an exception
                return print_or_raise()

            # there are some units available, list them.
            else:
                if environment.settings.get('to_fails') == 'raise':
                    raise ValueError('Conversion not possible. Possible values to use are: {}'.format(possible_units))
                else:
                    return 'Conversion not possible. Possible values to use are: {}'.format(possible_units)

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
            (self.value, self.dimensions, self.conv_factor)
        )

    def __round__(self, n=0):
        return Physical(round(self.value, n), self.dimensions, self.conv_factor)

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
                self.conv_factor,
            )

        # compare only between Physical instances
        self._check_other(other, "__mul__")

        # multiplying by another Physical instance, e.g. si.N * si.m
        new_dims = Dimensions(*[x + y for x, y in zip(self.dimensions, other.dimensions)])
        new_value = self.value * other.value

        # if the result is dimensionless, the value is returned
        if new_dims.dimensionsless:
            return new_value
        else:
            return Physical(new_value, new_dims)

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
            return Physical(new_value, new_dims)

    def __rtruediv__(self, other):

        if isinstance(other, NUMBER):

            return Physical(
                other / self.value,
                Dimensions(*[-x for x in self.dimensions]),
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

            return Physical(new_value, new_dimensions)

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


class PhysRep:
    """
    A class that makes handling units as string, number easier.

    When a Physical is printed, a string is returned.
    Using PhysRep this string becomes an object with value and unit attributes.
    Value is a float, unit is a string.
    Thus, converting to another unit while being able to use the value as a number is easier.

    say we have a Physical instance 12 m:
    p = 12 * si.m

    then we can do:
    rep = p._repr('mm')
    rep.value
    >>>12000
    rep.unit
    >>>'mm'

    rep = p._repr('cm')
    rep.value
    >>>120
    rep.unit
    >>>'cm'


    """

    def __init__(self, value: float, unit: str):
        self.value = value
        self.unit = unit

    @classmethod
    def split_str(cls, in_string: str) -> PhysRep:
        """
        Given a string representation of the Physical instance e.g. from Physical.to(), splits it into value and unit

        Expected input is line '12 mm'

        """
        valunit = in_string.split(' ')

        # checking that the split was successful
        if not len(valunit) == 2:
            raise ValueError('in_string must have 2 parts: value and unit')

        # taking it apart
        value, unit = valunit

        # checking the first part, it must be converted to float later
        try:
            value = float(value)
        except ValueError:
            raise ValueError('could not convert value to float: {}'.format(value))
        except:
            raise ValueError('could not convert value to float: {}'.format(value))

        # checking the second part, it must be a string
        try:
            unit = unit.lower()
        except AttributeError:
            raise ValueError('unit is not a string: {}'.format(unit))
        except:
            raise ValueError('unit is not a string: {}'.format(unit))

        return cls(float(value), unit.lower())

    @property
    def physical(self):
        """Returns a physical of the same value and unit"""

        keys = environment.namespace_module.__dict__.keys()
        new_unit = [x for x in keys if x == self.unit]
        if not new_unit:
            raise ValueError('unit {} is not defined in the environment'.format(self.unit))
        elif len(new_unit) > 1:
            raise ValueError('unit {} is defined multiple times in the environment'.format(self.unit))
        else:
            new_unit = new_unit[0]

        return self.value * environment.namespace_module.__dict__[new_unit]


def split_str(physical: str) -> tuple[float, str]:
    """Given a string representation of the Physical instance, splits it into value and unit"""
    value, unit = physical.split(' ')
    return float(value), unit


def justvalue(physical: str) -> float:
    """
    Given a string representation of the Physical instance, returns the value

    This can be used to e.g. after having printed a Physical instance using to(), return the value

    """
    return split_str(physical)[0]


# The seven SI base units
base_units = {
    "kg": Physical(1, Dimensions(1, 0, 0, 0, 0, 0, 0)),
    "m": Physical(1, Dimensions(0, 1, 0, 0, 0, 0, 0)),
    "s": Physical(1, Dimensions(0, 0, 1, 0, 0, 0, 0)),
    "A": Physical(1, Dimensions(0, 0, 0, 1, 0, 0, 0)),
    "cd": Physical(1, Dimensions(0, 0, 0, 0, 1, 0, 0)),
    "K": Physical(1, Dimensions(0, 0, 0, 0, 0, 1, 0)),
    "mol": Physical(1, Dimensions(0, 0, 0, 0, 0, 0, 1)),
}

# # preferred units
# # the preferred units are used to print the Physical instances so usually the most common units are used
# # the VALUES must beunique, but this is checked for in the environment file
preferred_units = {
    'mm': Dimensions(0, 1, 0, 0, 0, 0, 0),
    's': Dimensions(0, 0, 1, 0, 0, 0, 0),
    'kg': Dimensions(1, 0, 0, 0, 0, 0, 0),
    'kN': Dimensions(1, 1, -2, 0, 0, 0, 0),
    'kNm': Dimensions(1, 2, -2, 0, 0, 0, 0),
    'MPa': Dimensions(1, -1, -2, 0, 0, 0, 0),
}
#
# # dump the perferred units in an utf-8 json file
# import json
# with open('_preferred_units.json', 'w', encoding='utf-8') as f:
#     json.dump(preferred_units, f, ensure_ascii=True)
#
environment_settings = {
    'to_fails': 'print',  # raise, print
    'significant_digits': 3,
    'print_unit': 'smallest',  # smallest, largest
    # 'print_unit': 'largest',  # smallest, largest
}
# import json
# with open('_settings.json', 'w', encoding='utf-8') as f:
#     json.dump(environment_settings, f, ensure_ascii=True, indent=4)

from simplesi.environment import Environment

environment = Environment(si_base_units=base_units,
                          preferred_units=preferred_units,
                          settings=environment_settings)
