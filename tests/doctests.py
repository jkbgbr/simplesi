
"""

# defining

>>> import simplesi as si
>>> si.environment(env_name='structural')
>>> print(1.34 * si.m)
1340 mm



# usage
>>> h = 2 * si.m  # height
>>> w = 350 * si.mm  # width
>>> q = 1.5 * si.kN_m2  # uniform load
>>> A = h * w  # area
>>> F = A * q  # total force
>>> print(F)  # total force in kN
1.05 kN
>>> print(F.to('N'))  # total force in N
1050 N
>>> rep = F('N')  # representation of the force in N
>>> print(rep.value, rep.unit)
1050.0 N
>>> F.to('lbf')  # coversion to lbf - will fail as the unit is not defined
Conversion not possible. Possible values to use are: "N", "kN"
>>> si.environment(env_name='US_customary', replace=False)  # extending the environment with US customary units
>>> print(F.to('lbf'))
236.06 lbf


# significant digits

>>> print(0.134435 * si.m)
134.44 mm

# to, to_fails

>>> a = 2.45 * si.kN_m
>>> print(a.to())
Conversion not possible. Possible values to use are: "N/m", "N_m", "kN/m", "kN_m"
>>> a.to('mm')
Conversion not possible. Possible values to use are: "N/m", "N_m", "kN/m", "kN_m"



>>> a = 1234.56 * si.m
>>> print(a.to('km'))
1.23 km
>>> print(a.to('mm'))
1234560 mm
>>> b = 2.45 * si.kN_m
>>> print(b.to('N/m'))
2450 N/m
>>> print(b.to('N_m'))
2450 N/m

>>> si.environment.settings['print_unit'] = 'largest'
>>> print(2.45 * si.kN_m)
2.45 kN/m

>>> si.environment.settings['print_unit'] = 'smallest'
>>> print(2.45 * si.kN_m)
2450 N/m

>>> si.environment.settings['to_fails'] = 'raise'
>>> a = 1234.56 * si.N_m
>>> print(a.to('m'))
Traceback (most recent call last):
...
ValueError: Conversion not possible. Possible values to use are: "N/m", "N_m", "kN/m", "kN_m"

>>> print(0.134435 * si.m)
134.44 mm
>>> si.environment.settings['significant_digits'] = 5
>>> print(0.0013441256745 * si.m)
1.3441 mm


>>> si.environment(env_name='US_customary', replace=False)
>>> a = 1 * si.mile
>>> print(a)
1609344 mm


>>> a = 2.45 * si.m
>>> b = -a
>>> print(b)
-2450 mm

>>> a = -2.45 * si.kN
>>> print(abs(a))
2.45 kN

>>> a = 2.45 * si.kN
>>> print(bool(a))
True

>>> a = 2.45 * si.kN
>>> print(hash(a))
-8489301225018749141

>>> si.environment.settings['significant_digits'] = 4
>>> a = 2.4345635 * si.kN
>>> print(round(a))
2.435 kN
>>> print(round(a).value)
2434.5635
>>> print(round(a, 1))
2.435 kN
>>> print(round(a, 1).value)
2434.6
>>> a = 240.545 * si.kN
>>> print(round(a, -3))
241 kN


>>> si.environment.settings['significant_digits'] = 3
>>> a = 2.45 * si.kN
>>> b = 3450 * si.lbf
>>> c = a + b
>>> print(c)
17.80 kN
>>> d = a - b
>>> print(d)
-12.90 kN

>>> a = 2.45 * si.kN
>>> print(a + 0)
2.45 kN
>>> print(a + 1)
Traceback (most recent call last):
...
ValueError: Can only __add__ between Physical instances, these are <class 'int'> = 1 and <class 'simplesi.Physical'> = 2.45 kN
>>> print(a + (1 * si.m))
Traceback (most recent call last):
...
ValueError: Cannot add between 2.45 kN and 1000 mm: dimensions are incompatible

>>> lst = [1 * si.m, 2 * si.m]
>>> print(sum(lst))
3000 mm

>>> a = 2.45 * si.kN
>>> a += 3.45 * si.kN
Traceback (most recent call last):
...
ValueError: Cannot incrementally add Physical instances because they are immutable. Use 'a = a + b', to make the operation explicit.

# multiplication

>>> a = 2.45 * si.kN
>>> print(a * 2)
4.90 kN

>>> a = 2.45 * si.kN
>>> b = 3 * si.ft
>>> print(a * b)
2.24 kNm
>>> a = 1 * si.m
>>> b = 1 * si.ft
>>> print((a * b).to('m2'))
0.305 m²
>>> a * (1 * si.K)
Physical(value=1, dimensions=Dimensions(kg=0, m=1, s=0, A=0, cd=0, K=1, mol=0), conv_factor=1.0)

>>> a = 3 * si.s
>>> b = 3 * si.Hz
>>> print(a * b)
9

# division
>>> a = 2.45 * si.kN
>>> b = 3
>>> print(a / b)
0.817 kN
>>> print(a / 0)
Traceback (most recent call last):
...
ZeroDivisionError: Cannot divide by zero.


>>> a = 2.45 * si.kN
>>> b = 3 * si.ft
>>> print(a / b)
2679.35 N/m
>>> a = 1 * si.m
>>> b = 1 * si.ft
>>> print(b / a == b.conv_factor)
True
>>> print(a / (1 * si.K))
Traceback (most recent call last):
...
ValueError: No units found for the dimensions Dimensions(kg=0, m=1, s=0, A=0, cd=0, K=-1, mol=0).

# power
>>> a = 8 * si.kN
>>> b = 2 * si.m
>>> print(a / b ** 2)
0.002 MPa
>>> print((a / b ** 2).to('kN_m2'))
2 kN/m²


>>> a = 9 * si.m2
>>> print(a.sqrt())
3000 mm
>>> a = 4 * si.m3
>>> print(a.root(3))
1587.40 mm
>>> a = 1 * si.m2
>>> print(a.root(3))
Traceback (most recent call last):
...
ValueError: No units found for the dimensions Dimensions(kg=0.0, m=0.6666666666666666, s=0.0, A=0.0, cd=0.0, K=0.0, mol=0.0).

# physrep
>>> p = 12 * si.m
>>> rep = p('mm')
>>> rep.value
12000.0
>>> rep.unit
'mm'
>>> rep = p('cm')
>>> rep.value
1200.0
>>> rep.unit
'cm'

>>> p = 12 * si.m
>>> rep = p('mm')
>>> p2 = rep.physical
>>> print(p2)
12000 mm
>>> print(type(p2))
<class 'simplesi.Physical'>
>>> print(p2.value)
12.0
>>> print(p2.dimensions)
Dimensions(kg=0, m=1, s=0, A=0, cd=0, K=0, mol=0)
>>> print(p2.conv_factor)
1

>>> p = 12 * si.m
>>> rep = p('cm')
>>> print(rep.value, rep.unit)
1200.0 cm


# rich comparison
>>> a = 1 * si.kN
>>> b = 2 * si.kN
>>> c = 2 * si.m
>>> print(a == b)
False
>>> print(0 < b)
True
>>> print(a < b)
True
>>> print(a <= b)
True
>>> print(b > c)
Traceback (most recent call last):
...
ValueError: Can only compare between Physical instances of equal dimension or zero.
>>> print(b > 3)
Traceback (most recent call last):
...
ValueError: Can only __gt__ between Physical instances, these are <class 'int'> = 3 and <class 'simplesi.Physical'> = 2 kN


# deep
>>> a = 1 * si.m3
>>> print(a.is_SI)
True
>>> print(a.to('m3'))
1 m³
>>> b = 1 * si.ft
>>> print(b.is_SI)
False

"""