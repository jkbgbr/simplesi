# # import pathlib
# # import pprint
# #
# #
# # import simplesi as si
# # si.environment('structural', top_level=False)
# # #
# # F = 3000 * si.N
# # h = 256 * si.mm
# # print(F * h)
# # print(F.to('kN'), 'x', h.to('m'), '=', (F * h).to('kNm'))
# #
# # print('{} = {}'.format(si.m.to('m'), si.m.to('mm')))
# # print('{} = {}'.format(si.m.to('m'), si.m.to('cm')))
# # print('{} = {}'.format(si.m.to('m'), si.m.to('km')))
# # print('{} = {}'.format((2.5 * si.m).to('m'), (2.5 * si.m).to('mm')))
# #
# #
# import simplesi as sit
# sit.environment(env_name='structural', top_level=True)
#
# F = 3000 * N
# h = 256 * mm
# print(F * h)
# print('{} x {} = {}'.format(F, h, F * h))
#
#
# print('{} = {}'.format(m.to('m'), m.to('mm')))
# print('{} = {}'.format(m.to('m'), m.to('cm')))
# print('{} = {}'.format(m.to('m'), m.to('km')))
# print('{} = {}'.format((2.51 * m).to('m'), (2.51 * m).to('mm')))
#
# q = -348 * kN / m**2
# q = -348 * kN_m2
# print(q)
# print(q.to())
# print(q.to('bar'))
#
# f = 1000 * kg * m / s**2
# print(f)
# # print(f.to())
# # print(f.to('N'))
# # print(f.to('kN'))
#
# exit()


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