# # import pathlib
# # import pprint
# #
# #
import pprint

import simplesi as si
si.environment('imperial', top_level=False)
print(si.environment.number_defined_units)
pprint.pprint(si.environment.environment)


a = 1 * si.ft
b = 1 * si.m

print('==', a == b)
print('!=', a != b)
print('<=', a <= b)
print('>=', a >= b)







exit()
import timeit

mysetup = """import simplesi as si
si.environment(env_name='structural')
import math
import random"""

mycode = """

x = random.randint(1, 100) * si.mm
y = random.randint(1, 100) * si.m
z = 0

def f(x, y, z):
    _ret = (z + x - y) / (x + y - z) * math.log(x/y)

f(x, y, z)
"""

print(timeit.timeit(setup=mysetup,
                    stmt=mycode,
                    number=100000))