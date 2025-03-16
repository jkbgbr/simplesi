# # import pathlib
# # import pprint
# #
# #
import pprint

import simplesi as si
si.environment('imperial')
si.environment('structural', replace=False)
# pprint.pprint(si.environment.environment)



a = 1 * si.ft
b = 1 * si.m
c = 1 * si.inch

print('==', a == b)
print('!=', a != b)
print('<=', a <= b)
print('>=', a >= b)

# to
print((1 * si.inch).to('inch'))
print((1 * si.inch).to('m'))
print((1 * si.m).to('m'))
print((3 * si.mol).to('mol'))
print(3 * si.mol)
print(3 * si.ft)

# addition
print()
print('ADDITION')
print()
print((a+b))
print((a+0))
print((0+b))
print()
print((0+c))
print(c)
print((c+0))

print((a+b).to())
print((a+b+c).to('m'))
print((a+b+c).to('ft'))
print((a+b).to('inch'))
print((a+b+c).to('inch'))

print(c.to('inch'))

# substraction
print()
print('SUBSTRACTION')
print()
print((a-b))
print((a-0))
print((0-c))
print((a-b).to())
print((a-b+c).to('m'))
print((a+b-c).to('ft'))
print((a-b).to('inch'))
print((a-b-c).to('inch'))
print((c-c))
print((c-c).to('inch'))


exit()
# print((a+b).to('m'))
# print((b+a).value)
#
#
#
#
#
# exit()
import timeit

mysetup = """import simplesi as si
si.environment(env_name='imperial')
si.environment(env_name='structural', replace=False)
import math
import random"""

mycode = """

x = random.randint(1, 100) * si.mm
y = random.randint(1, 100) * si.mm
z = 0

def f(x, y, z):
    _ret = (z + x - y) / (x + y - z) * math.log(x/y)

f(x, y, z)
"""

print(timeit.timeit(setup=mysetup,
                    stmt=mycode,
                    number=100000))