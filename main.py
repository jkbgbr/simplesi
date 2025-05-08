

import simplesi as si
si.environment(env_name='structural')
# si.environment(env_name='US_customary', replace=False)
#

si.environment.settings['to_fails'] = 'raise'

a = 0.134435 * si.m
print(a)
si.environment.settings['significant_digits'] = 5
print(a)


print(a())


exit()

print(a.to('m'))
# a.to('m')
print(a.to('N_m'))
print(a.to('kN/m'))
print(a.to('kN_m'))

si.environment.settings['print_unit'] = 'largest'
print(a)
si.environment.settings['print_unit'] = 'smallest'
print(a)
exit()
# b = 1 * si.ft
#
# print(a)
# print(a)
# # print(b)
# # print((a+b).to('ft'))
# # print(b+a)
#
# exit()
#

from simplesi import Physical

# Physical.as_str(value=12.2535)
# Physical.as_str(value=0.2535)
# Physical.as_str(value=0.253)
# Physical.as_str(value=0.25)
# Physical.as_str(value=0.2)
# Physical.as_str(value=0.02)
# Physical.as_str(value=0.002)
# Physical.as_str(value=0.0002)
# Physical.as_str(value=1.2)
# Physical.as_str(value=1.02)
# Physical.as_str(value=1.002)
# Physical.as_str(value=1.0002)
# Physical.as_str(value=2535)
# Physical.as_str(value=253.5)

print(2 * si.yard)
print((2 * si.yard).to('mm'))

exit()


import timeit

mysetup = """import simplesi as si
si.environment(env_name='us_customary')
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
