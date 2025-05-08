<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
-->


<!-- PROJECT LOGO -->
<!--
<br />
<div align="center">
  <a href="https://github.com/jkbgbr/simplesi">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">simplesi</h3>

  <p align="center">
    project_description
    <br />
    <a href="https://github.com/jkbgbr/simplesi"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/jkbgbr/simplesi">View Demo</a>
    &middot;
    <a href="https://github.com/jkbgbr/simplesi/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/jkbgbr/simplesi/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>
-->

<!-- ABOUT THE PROJECT -->
## About The Project

Simplesi is a package enabling units-aware engineering calculations. It is based on and heavily influenced by [forallpeople](https://github.com/connorferster/forallpeople), but differs from it considerably.
It scratches somewhat the itch that most such packages are quite slow. Also, this module was made with apps in head rather than interactive use (e.g. jupyter).

Compared to forallpeople:
- faster - I measured ~3-4x speedup but YMMW.
- the concept of environments is adapted with changes.
  - SI and non-SI units are in separated environments; environment definitions are otherwise similar
  - loading multiple environments is allowed, hence mixing e.g. US customary and SI units is still possible
- more robust operations, e.g. between a scalar and a Physical - no ambiguous additions
- modified, maybe more intuitive behavior of printing
- user-defined environment behaviour
  - exception handling: print or raise
  - number of significant digits for print can be set
  - user-defined preferred units can be defined for printing to reduce boilerplate code
- [Fractions](https://docs.python.org/3/library/fractions.html) are not used anymore, which resulted in the massive speedup but makes using fractional dimensions - well, in some cases impossible as fractional dimensions are now subject to float precision issues.

Compared to [pint](https://github.com/hgrecco/pint) - just kidding, not a fair comparison.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Installation

Currently only available by direct download from github.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

I chose `si` to be the customary abbreviation for the package. 
The simplest way to use the package is to import it and call the environment with the filename of the environment. `env_name` is optional, if omitted, the seven base SI units are available only.

```python
>>> import simplesi as si
>>> si.environment(env_name='structural')
```

This will load units defined in the environment file `structural.json` from the `environments` subdirectory, which is the default place the unit definitions.

At this point the units defined in `structural.json` are loaded in the `si` namespace and are available for use.
In an IDE the units are probably not recognized and thus marked unknown as they are not directly defined in the code.

From here on, defining a variable with a unit is as simple as

```python
>>> a = 2.45 * si.m
```

Values defined with a unit are `Physical` objects. These have three attributes:
- `value` - the value of the object, e.g. 2.45
- `dimensions` - a 7-element namedtuple defining the dimension of the unit. See [dimensional analysis](https://en.wikipedia.org/wiki/Dimensional_analysis) for the theory.
- `conv_factor` - a (linear) conversion factor to allow for non-SI units. The conversion factor means: what number of base SI-units are in this unit. For example 1 ft = 0.3048 m -> conv_factor = 0.3048

```python
>>> print(a.value)
2.45
>>> print(a.dimensions)
Dimensions(kg=0, m=1, s=0, A=0, cd=0, K=0, mol=0)
>>> print(a.conv_factor)
1
```

The `Physical` object is callable and returns a `PhysRep` object. See [Representing a Physical object](#representing-a-physical-object) for more details.

Importing the package will create an `Environment` object with some default settings that define the default behavior of the `Physical` objects. These are:

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Printing

The aim is to reduce boilerplate by defining some key behavior properties, thus reducing the amount of typing.

If for a `Physical` a preferred unit is set, it will be used to display the number with the set number of significant digits.

```python
>>> print(1.34 * si.m)
1340 mm  # the default unit for length is [mm]
```

```python
>>> print(0.134435 * si.m)
134.44 m  # the default number of significant digits is 3
```

A list of available units is shown when the `to()` method is called empty or with an incompatible unit.
Note: for this example the setting `to_fails` is set 'print'. See the section [Exception handing](#exception-handing) for more details.
```python
>>> a = 2.45 * si.kN_m
>>> print(a.to())
Conversion not possible. Possible values to use are: "kN_m", "N/m", "kN/m", "N_m"
>>> print(a.to('mm'))
Conversion not possible. Possible values to use are: "kN_m", "N/m", "kN/m", "N_m"
```

Otherwise a conversion simply returns the value in the requested unit. Both the symbol and the unit name can be used to define the unit to convert to.
```python
>>> a = 1234.56 * si.m
>>> print(a.to('km'))
1.23 km  # remember the significant digits?
>>> print(a.to('mm'))
1234560 mm
>>> b = 2.45 * si.kN_m
>>> print(b.to('N/m'))
2450 N/m
>>> print(b.to('N_m'))
2450 N/m
```

If no preferred unit is set for a `Physical` object, depending on the setting 'print_unit' it will use the smallest or the largest compatible unit.
```python
>>> si.environment.settings['print_unit'] = 'largest'
>>> print(2.45 * si.kN_m)
2.45 kN/m  # the default setting is to use the 'largest' unit (providing the smallest value)
```

Using the setting 'smallest' will use the smallest compatible unit.
```python
>>> si.environment.settings['print_unit'] = 'smallest'
>>> print(2.45 * si.kN_m)
2450 N/m
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Exception handing
One can choose to print the exception or raise it. This is useful for interactive use cases, where one may want to see the error message, but in an app it is better to raise an exception.
By default, the exception is printed. 

```python
>>> si.environment.settings['to_fails'] = 'raise'
>>> a = 1234.56 * si.N_m
>>> print(a.to('m'))
Traceback (most recent call last):
...
ValueError: Conversion not possible. Possible values to use are: "N/m", "N_m", "kN/m", "kN_m"
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Significant digits
Finally, the number of significant digits can be set. This is useful for printing the results in a more readable way. The default is 3 significant digits.

```python
>>> print(0.134435 * si.m)
134.44 mm
>>> si.environment.settings['significant_digits'] = 5
>>> print(0.0013441256745 * si.m)
1.3441 mm
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Environments

Environments are meant to separate "families" of units.

When defining an SI unit, the bare minimum to define is a unit name, a value and a dimension.
- name is the one to be used when defining `Physical` objects, e.g. `si.km
- value is the conversion factor to the base SI unit`, e.g. 1 km = 1000 m means value = 1000
- dimension is a 7-element list defining the exponents for the `Physical` object's Dimension property.

The base SI units are as follows:

```python
base_units = {
    "kg": Physical(1, Dimensions(1, 0, 0, 0, 0, 0, 0)),
    "m": Physical(1, Dimensions(0, 1, 0, 0, 0, 0, 0)),
    "s": Physical(1, Dimensions(0, 0, 1, 0, 0, 0, 0)),
    "A": Physical(1, Dimensions(0, 0, 0, 1, 0, 0, 0)),
    "cd": Physical(1, Dimensions(0, 0, 0, 0, 1, 0, 0)),
    "K": Physical(1, Dimensions(0, 0, 0, 0, 0, 1, 0)),
    "mol": Physical(1, Dimensions(0, 0, 0, 0, 0, 0, 1)),
}
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Default environment

The default settings are probably best for structural engineers writing an app (yours truly). When simply importing the package and setting the environment name via `si.environment()`, only the base SI units are available and following settings are applied:

```python
preferred_units = {
    'mm': Dimensions(0, 1, 0, 0, 0, 0, 0),
    's': Dimensions(0, 0, 1, 0, 0, 0, 0),
    'kg': Dimensions(1, 0, 0, 0, 0, 0, 0),
    'kN': Dimensions(1, 1, -2, 0, 0, 0, 0),
    'kNm': Dimensions(1, 2, -2, 0, 0, 0, 0),
    'MPa': Dimensions(1, -1, -2, 0, 0, 0, 0),
}

environment_settings = {
    'to_fails': 'raise',  # raise, print
    'significant_digits': 3,
    'print_unit': 'smallest',  # smallest, largest
}
```

When calling `si.environment()` the following arguments are available:

- `env_name`: the name of the environment to load. An 'env_name.json' file must exist in the default environmants directory or the one provided in `env_path`.
- `env_path`: a pathlib.Path object defining the path to the environment file. If not provided, the default path is used.
- `env_dict`: a dictionary defining the environment if for some reason it makes more sense to provide it directly rather than in a file.
- `replace`: see Loading multiple environments
- `top_level`: if True, the environment is loaded to `__builtins__` and units are available instead of e.g. `si.m` as `m`. If False, the environment is loaded to the `simplesi` namespace and are available via e.g. `si.m`.
- `preferred_units`: the dictionary defining the preferred units for printing.
- `settings`: the dictionary defining the environment settings. The default settings are used if not provided.

Getting the environment from files is possible, but currently there is nothing implemented to do the same for settings and preferred units.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Loading multiple environments

If you can't avoid using e.g. US customary units and SI units in the same project, you can load multiple environments. Which allows for fun definitions like

```python
m = 1 * si.mile
```

Loading the second environment is simple and any number of environments can be loaded.

```python
>>> si.environment(env_name='structural')
>>> si.environment(env_name='US_customary', replace=False)  # loads the second environment and doesn't replace the first one
>>> si.environment(env_name='US_customary', replace=True)  # loads the second environment and replaces any previously loaded environment
```

When loading multiple environments, the settings are not affected.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Arithmetics

`Physical` objects can be added, subtracted, multiplied, divided, compared etc. like scalars, assuming they are compatible. `Physical` objects are compatible if their `Dimensions` properties are equal. If compatible, arithmetics is basically same as scalar arithmetics with the exception that operations between SI and non-SI units are possible.  
All operations result in a new `Physical` instance since these are immutable. This also means, none of the incremepntal operations are available.

#### Negation

Negation is possible in any cases even if the result has no physical sense.

```python
>>> a = 2.45 * si.m
>>> b = -a
>>> print(b)
-2450 mm
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

#### Absolute value

```python
>>> a = -2.45 * si.kN
>>> print(abs(a))
2.45 kN
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

#### Addition, substraction

The operations are straightforward.

```python
>>> a = 2.45 * si.kN
>>> b = 3450 * si.lbf
>>> c = a + b
>>> print(c)
17.80 kN
>>> d = a - b
>>> print(d)
-12.90 kN
```

Adding a scalar other than zero or any non-compatible `PhysicaL` fails.

```python
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
```

Being able to add zero, using the sum() function on `Physical` objects is possible.

```python
>>> lst = [1 * si.m, 2 * si.m]
>>> print(sum(lst))
3000 mm
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

#### Multiplication

Multiplication with a scalars is possible.

```python
>>> a = 2.45 * si.kN
>>> print(a * 2)
4.90 kN
```
Multiplication with a `Physical` object returns a new `Physical` object with the dimensions of the two added elementwise.
If the return value is not defined, a `Physical` is still returned. If the multiplication yields a dimensionsless value, a float is returned.

```python
>>> a = 2.45 * si.kN
>>> b = 3 * si.ft
>>> print(a * b)
2.24 kNm
>>> a = 1 * si.m
>>> b = 1 * si.ft
>>> print((a * b).to('m2'))
0.305 m²
>>> print(a * (1 * si.K))
Physical(value=1, dimensions=Dimensions(kg=0, m=1, s=0, A=0, cd=0, K=1, mol=0), conv_factor=1.0)
```

The multiplication can yield a dimensionsless result - it is a scalar then.
```python
>>> a = 3 * si.s
>>> b = 3 * si.Hz
>>> print(a * b)
9
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

#### Division

Division with a scalar other than zero is possible.

```python
>>> a = 2.45 * si.kN
>>> b = 3
>>> print(a / b)
0.817 kN
>>> print(a / 0)
Traceback (most recent call last):
...
ZeroDivisionError: Cannot divide by zero.
```
Division with a `Physical` object returns a new `Physical` object with the dimensions of the two substracted elementwise.
If the return value is not defined, a `Physical` is still returned. If the division yields a dimensionsless value, a float is returned.

```python
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
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

#### Power

Raising a `Physical` object to a power returns a new `Physical` object with each element of dimensions multiplied with the power.

```python
>>> a = 8 * si.kN
>>> b = 2 * si.m
>>> print(a / b ** 2)
0.002 MPa
>>> print((a / b ** 2).to('kN_m2'))
2 kN/m²
```
There is a `Physical.sqrt()` method, as `math.sqrt()` is not defined for `Physical` objects and raises TypeError. There is also a `Physical.root()` to calculate the nth root. Internally both use `__pow__()`.

```python
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
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Representing a Physical object

Printing a `Physical` object is just a string. Great, it is not really easy to reuse the value from that point.
The `PhysRep` class is used to represent a `Physical` objects value as float and unit as string. The `Physical` is a callable so accessing the `PhysRep` of a `Physical` is simple.

```python
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
```

From the `PhysRep` the `Physical` object can be recreated.

```python
>>> p = 12 * si.m
>>> rep = p('mm')
>>> p2 = rep.physical
>>> print(p2)
12000 mm
>>> print(type(p2))
<class 'simplesi.Physical'>
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Rich comparison

`Physical` objects can be compared with each other if they are compatible. Comparison with a scalar other than zero raises a ValueError.


```python
>>> a = 1 * si.kN
>>> b = 2 * si.kN
>>> c = 2 * si.m
>>> print(a == b)
False
>>> print(a < b)
True
>>> print(0 < b)
True
>>> print(a <= b)
True
>>> print(b > c)
Traceback (most recent call last):
...
ValueError: Can only compare between Physical instances of equal dimension or zero.
>>> print(b > c)
Traceback (most recent call last):
...
ValueError: Can only __gt__ between Physical instances, these are <class 'int'> = 3 and <class 'simplesi.Physical'> = 2 kN
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Other cool stuff

`Physical` objects 
- evaluate to True
- are hashable
- can be rounded

Rounding is essentially like the built-in round() function but instead of returning the int() of the number if no significant digits is provided, the current setting of the environment is used. Rounding affects `Physical.value`, and the result may be unexpected if `Physical` is represented in something else than the base unit. 

```python
>>> si.environment.settings['significant_digits'] = 4
>>> a = 2.4345635 * si.kN
>>> print(round(a))  # same as round(a, 4)
2.435 kN
>>> print(round(a).value)  # value is rounded to 4 significant digits
2434.5635
>>> print(round(a, 1))  # same return value as round(a, 4)
2.435 kN
>>> print(round(a, 1).value)  # value is rounded to 1 significant digit
2434.6
>>> a = 240.545 * si.kN
>>> print(round(a, -3))
241 kN
```

## Some additional details from the deep

### The Physical object

Defining a `Physical` requres at least a value and a dimension. If no `conv_factor` is provided, it is set to 1.0. 
It is the `conv_factor` what makes a `Physical` SI or non-SI: a value other than 1.0 means the unit is non-SI.
An optional `symbol` can be provided, which is used for pretty printing. If not provided, the unit name is used.

```python
>>> a = 1 * si.m3
>>> print(a.is_SI)
True
>>> print(a.to('m3'))
1 m³
>>> b = 1 * si.ft
>>> print(b.is_SI)
False
```

### The Environment object

The environment object is a callable instance of the Environment class that gets created when the package is imported and can be accessed via `si.environment`. 
It holds the units available to create `Physical` objects, the settings and the preferred units etc. 
When unit definitions are provided, they are checked formally for correctness - not necessarily a bulletproof solution, but probably good enough.
Preferences and settings can be updated using the `apply_preferences()` and `apply_settings()` methods. 


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->


## Contributing

Contributions are welcome! Fork it, fix it, PR it.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Connor Fester](https://github.com/connorferster)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
