import pprint
from dataclasses import dataclass
import pathlib
import json
import sys
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

    def __call__(self,
                 env_name: str,
                 env_path: pathlib.Path = None,
                 overload: bool = True,  # False: existing units are remoed first
                 top_level: bool = False
                 ):
        """
        Loads the environment from a json file.

        :param env_name: name of the environment file without the .json extension
        :param env_path: path to the environment file. If None, the file is assumed to be in the "environments" subfolder.
        :param overload: if True, the previously defined environment is left as is, new units are added to it.
        :param top_level: if True the environment is pushed to the top level namespace. If False, it is pushed to the module namespace.
        :return:
        """

        # no env_path provided: default location
        if env_path is None:
            env_path = pathlib.Path(__file__).parent
        env_path = env_path / 'environments' / (env_name + ".json")

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
        if top_level:
            import builtins
            self.push_module = builtins

        else:
            # get the name of the current package
            pkg = __name__.split('.')[0]
            self.push_module = sys.modules[pkg]

        # if overload is False, the old units, if any, are removed first.
        if not overload:
            for key in self.base_units.keys():
                self.push_module.__dict__.pop(key)
            for key in self.environment.keys():
                # some keys may have been removed earlier we jsut try
                try:
                    self.push_module.__dict__.pop(key)
                except KeyError:
                    pass

        self.environment = units_environment

        # pusing the environment to the global namespace. To do this, first the environment is
        # used to generate Physical objects, which are then pushed to the global namespace.
        self._units = {}
        from simplesi import Physical, PRECISION
        for unit, definitions in units_environment.items():
            self._units[unit] = Physical(value=definitions.get('Value', 1),
                                         dimensions=definitions["Dimension"],
                                         precision=PRECISION, )

        # push
        self._push_vars(self._units, self.push_module)  # from the userdefined environment
        self._push_vars(self.base_units, self.push_module)  # base units

    def _push_vars(self, units_dict: dict, module: ModuleType) -> None:
        module.__dict__.update(units_dict)


if __name__ == '__main__':

    # the path to the file named environmant.json in the current dir
    jsonpath = "environment.json"

