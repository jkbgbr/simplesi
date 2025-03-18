import math
import pprint
from dataclasses import dataclass, field
import pathlib
import json
import sys
import builtins
from types import ModuleType

from simplesi import NUMBER
from simplesi.dimensions import Dimensions


@dataclass
class Environment:
    """
    This class defines the environment in which the Physical objects are created.

    The preferred way to use this class is to use the instance created at the end of the __init__.py file.
    This way the environment is loaded with the base units when the module is imported.

    A subsequent call to the instance will load the environment defined by env_name and optionally env_path.
    If no env_path is provided, the environment file is assumed to be in the same directory as the module.
    In all cases the .json extension is not needed.

    import simplesi as si
    si.environment(env_name='default')  # no path provided
    si.environment(env_name='default', env_path=pathlib.Path('path_to_env_file'))  # path defined

    see the __call__ method for more details.
    """
    si_base_units: dict
    preferred_units: dict
    environment: {} = None
    settings: dict = field(default_factory=lambda: {'print_unit': 'smallest',
                                                    'keep_SI': True})

    def __post_init__(self):
        if self.environment is None:
            self.environment = {}

        # checking the environment
        errors = self._check_environment_definition(self.environment)
        if errors:
            for error in errors:
                print(error)
            raise ValueError("Errors in the environment.")

        # checking preferred units: all values must be unique.
        # This is so when printing the Physical in preferred units the choice is unambiguous.
        if self.preferred_units:
            if not len(self.preferred_units) == len(set(self.preferred_units.values())):
                raise ValueError("Preferred unit values must be unique.")

    @classmethod
    def _check_environment_definition(cls, definitions: dict):
        """Checks if all unit definitions are formally correct"""

        errors = []

        # check unit uniqueness
        if not len(definitions) == len(set(definitions.keys())):
            errors.append("Unit names must be unique.")

        for k, v in definitions.items():

            # check if the unit is a string
            if not isinstance(k, str):
                errors.append("Unit name must be a string.")

            # check dimension
            if "Dimension" in v.keys():
                # 7 dimensions
                if len(v["Dimension"]) != 7:
                    errors.append(f"Dimension must have a length of 7 for unit {k}.")
                # no dimensionsless units
                if all(d == 0 for d in v["Dimension"]):
                    errors.append(f"Unit {k} is dimensionless.")
            else:
                errors.append(f"Dimension not defined for unit {k}.")

            # check symbol
            if "Symbol" in v.keys():
                if not isinstance(v["Symbol"], str):
                    errors.append(f"Symbol must be a string for unit {k}.")

            # check factor
            if "Factor" in v.keys():
                if not isinstance(v["Factor"], NUMBER):
                    errors.append(f"Factor must be a number for unit {k}.")

            # check value
            if "Value" in v.keys():
                if not isinstance(v["Value"], NUMBER):
                    errors.append(f"Value must be a number for unit {k}.")

        return tuple(errors)

    def __call__(self,
                 env_name: str = None,
                 env_path: pathlib.Path = None,
                 env_dict: dict = None,
                 replace: bool = False,  # True: existing units are removed first
                 top_level: bool = False,
                 preferred_units: dict = None,
                 settings: dict = None,
                 ):
        """
        Loads the environment from a json file.

        :param env_name: name of the environment file without the .json extension
        :param env_path: path to the environment file. If None, the file is assumed to be in the "environments" subfolder.
        :param replace: if True, the previously defined environment is removed first.
        :param top_level: if True the environment is pushed to the top level namespace. If False, it is pushed to the module namespace.
        :param preferred_units: defines which unit to use by default when printing the Physical object.
        :param env_dict: a dictionary of the environment. If provided, the env_name and env_path are ignored.
        :return:
        """

        if not env_dict:

            # no env_path provided: default location
            if env_path is None:
                env_path = pathlib.Path(__file__).parent / 'environments'
            env_path = env_path / (env_name + ".json")

            # check if the file exists
            if not env_path.exists():
                raise ValueError("Environment file not found at {}.".format(env_path))

            # open and load
            # not tested!
            with open(env_path, "r", encoding="utf-8") as json_unit_definitions:
                try:
                    units_environment = json.load(json_unit_definitions)
                except json.decoder.JSONDecodeError as e:
                    raise ValueError("Error decoding the environment file at {}. Problem: {}".format(env_path, *e.args)) from None

        else:
            units_environment = env_dict

        _ret = self._check_environment_definition(units_environment)
        if _ret:
            for error in _ret:
                print(error)
            raise ValueError("Errors in the environment file at {}.".format(env_path))

        # reading the environment file
        for unit, definitions in units_environment.items():
            # previous checks make sure Dimension is present and correwt
            dimensions = definitions.get("Dimension")
            # the unitname, if not defined
            symbol = definitions.get("Symbol", unit)
            # conversion factor is 1 if not defined
            conv_factor = definitions.get("Factor", 1)
            # Value is 1 if not defined
            value = definitions.get("Value", 1)

            units_environment[unit]["Dimension"] = Dimensions(*dimensions)
            units_environment[unit]["Symbol"] = symbol
            units_environment[unit]["Factor"] = conv_factor
            units_environment[unit]["Value"] = value

        # deciding which namespace to push the environment to
        # top level -> builtins. In this case the units are available simply by name, e.g. "m" or "kg"
        if top_level:
            self.namespace_module = builtins

        # module. The units are available by e.g. "si.m" or "si.kg"
        else:
            # get the name of the current package
            pkg = __name__.split('.')[0]
            self.namespace_module = sys.modules[pkg]

        # if replace is True, the old units, if any, are removed first.
        if replace:
            for key in self.si_base_units.keys():
                try:
                    self.namespace_module.__dict__.pop(key)
                except KeyError:
                    pass
            for key in self.environment.keys():
                # some keys may have been removed earlier we jsut try
                try:
                    self.namespace_module.__dict__.pop(key)
                except KeyError:
                    pass
            # to be synced, the environment is also emptied
            self.environment = None

        # updating the environment
        if self.environment is None:
            self.environment = {}
        self.environment.update(units_environment)

        # pusing the environment to the chosen namespace. To do this, first the environment is
        # used to generate a dict of Physical objects, which is then pushed to the namespace.
        self._units = {}
        from simplesi import Physical, PRECISION
        for unit, definitions in self.environment.items():

            # Physical holds:
            # - the value of the unit. The value of non-SI units is the value in SI units.
            # - the conversion factor for non_SI units. For SI units this is 1.
            # - the dimensions of the unit as a Dimensions object
            # - the precision of the unit for displaying

            self._units[unit] = Physical(value=definitions.get('Value') * definitions.get('Factor'),
                                         conv_factor=definitions.get('Factor'),
                                         dimensions=definitions["Dimension"],
                                         precision=PRECISION, )

        # push
        self._push_vars(self._units, self.namespace_module)  # from the userdefined environment
        self._push_vars(self.si_base_units, self.namespace_module)  # base units

    def _push_vars(self, units_dict: dict, module: ModuleType) -> None:
        module.__dict__.update(units_dict)

    @property
    def number_defined_units(self):
        from simplesi import Physical
        return len({k: v for k, v in self.namespace_module.__dict__.items() if isinstance(v, Physical)})


if __name__ == '__main__':  # pragma: no cover

    # the path to the file named environmant.json in the current dir
    jsonpath = "environment.json"
