import pathlib
import pprint

import simplesi as si
si.environment(env_name='structural', top_level=False)


# pprint.pprint(si.environment)
#
print(si.m)
print(si.mm)
#
print(si.m * si.mm / si.A)