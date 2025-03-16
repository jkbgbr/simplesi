import pathlib
import pprint
import unittest
from os import environ

import simplesi
import sys


class TestEnvironmentCreation(unittest.TestCase):

    def test_environment_module_level(self):
        # no environment loaded yet
        # by importing the basic units are loaded
        self.assertTrue(len(simplesi.environment.si_base_units) == 7)
        # no environment yet
        self.assertFalse(simplesi.environment.environment)
        with self.assertRaises(AttributeError):
            simplesi.environment.number_defined_units

        # loading an environment
        simplesi.environment(env_name='default')
        self.assertTrue(len(simplesi.environment.si_base_units) == 7)  # still the same
        self.assertTrue(simplesi.environment.environment)
        self.assertTrue(len(simplesi.environment.environment) > 0)
        environment_length = simplesi.environment.number_defined_units

        # loading a new, smaller environment, REPLACING the old one
        envpath = pathlib.Path(__file__).parent
        simplesi.environment(env_name='test_definitions', env_path=envpath, replace=True)
        # overloading (adding) an environment, should not change the number of base units
        self.assertTrue(len(simplesi.environment.si_base_units) == 7)  # still the same
        self.assertGreaterEqual(environment_length, len(simplesi.environment.environment))  # added some units
        environment_length = len(simplesi.environment.environment)

        # trying to load one but bad name
        with self.assertRaises(ValueError):
            simplesi.environment(env_name='whatever', replace=False)

        # loading a new, ADDING TO the old one
        simplesi.environment(env_name='default', replace=False)

        # overloading (adding) an environment, should not change the number of base units
        self.assertTrue(len(simplesi.environment.si_base_units) == 7)  # still the same
        self.assertGreaterEqual(len(simplesi.environment.environment), environment_length)  # added some units
        environment_length = len(simplesi.environment.environment)

        # units are in the namespace
        self.assertTrue('m' in simplesi.environment.namespace_module.__dict__)
        self.assertTrue('kg' in simplesi.environment.namespace_module.__dict__)
        self.assertFalse('whatever' in simplesi.environment.namespace_module.__dict__)


if __name__ == '__main__':
    unittest.main()
