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