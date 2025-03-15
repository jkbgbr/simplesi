import pathlib
import pprint

import simplesi as si
si.environment(env_name='default', env_path=pathlib.Path('E:/modules/simplesi/simplesi/'))

pprint.pprint(si.environment)

print(si.m)
print(si.mm)

print(si.m * si.mm / si.A)