import pprint
from dataclasses import dataclass
import pathlib
import json
import sys
import builtins
from types import ModuleType

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
    base_units: {}
    environment: {} = None

    def __post_init__(self):
        if self.environment is None:
            self.environment = {}

    def __call__(self,
                 env_name: str,
                 env_path: pathlib.Path = None,
                 replace: bool = False,  # True: existing units are removed first
                 top_level: bool = False
                 ):
        """
        Loads the environment from a json file.

        :param env_name: name of the environment file without the .json extension
        :param env_path: path to the environment file. If None, the file is assumed to be in the "environments" subfolder.
        :param replace: if True, the previously defined environment is removed first.
        :param top_level: if True the environment is pushed to the top level namespace. If False, it is pushed to the module namespace.
        :return:
        """

        # no env_path provided: default location
        if env_path is None:
            env_path = pathlib.Path(__file__).parent / 'environments'
        env_path = env_path / (env_name + ".json")

        # check if the file exists
        if not env_path.exists():
            raise ValueError("Environment file not found at {}.".format(env_path))

        # open and load
        with open(env_path, "r", encoding="utf-8") as json_unit_definitions:
            units_environment = json.load(json_unit_definitions)

        # reading the environment file
        for unit, definitions in units_environment.items():
            dimensions = definitions.get("Dimension", ())
            symbol = definitions.get("Symbol", unit)

            if not dimensions:
                raise ValueError("Dimension not defined for unit {}.".format(unit))

            units_environment[unit]["Dimension"] = Dimensions(*dimensions)
            units_environment[unit]["Symbol"] = symbol

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
            for key in self.base_units.keys():
                self.namespace_module.__dict__.pop(key)
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

        # pusing the environment to the global namespace. To do this, first the environment is
        # used to generate Physical objects, which are then pushed to the global namespace.
        self._units = {}
        from simplesi import Physical, PRECISION
        for unit, definitions in self.environment.items():
            self._units[unit] = Physical(value=definitions.get('Value', 1),
                                         dimensions=definitions["Dimension"],
                                         precision=PRECISION, )

        # push
        self._push_vars(self._units, self.namespace_module)  # from the userdefined environment
        self._push_vars(self.base_units, self.namespace_module)  # base units

    def _push_vars(self, units_dict: dict, module: ModuleType) -> None:
        module.__dict__.update(units_dict)

    @property
    def number_defined_units(self):
        from simplesi import Physical
        return len({k: v for k, v in self.namespace_module.__dict__.items() if isinstance(v, Physical)})


if __name__ == '__main__':  # pragma: no cover

    # the path to the file named environmant.json in the current dir
    jsonpath = "environment.json"

