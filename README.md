# A library supporting functional programming in Python.
## Tested environments
Tested on `Python 3.6.3`.
## Installation
Install with pip as follows:

```python
pip install dpl
```

# `func_pipe` decorator
This decorator turns a function or an object method into a `func_pipe` object and then you can pass arguments to it in different ways which are convenient to build pipelines later.


Let's see an example. Assume that you have the following functions decorated with `func_pipe`:

```python
from dpl.pipe import chain_pipe
@func_pipe
def add_1(x):
    return x + 1

@func_pipe
def multiply_2(x):
    return x * 2

@func_pipe
def subtract_3(x):
    return x - 3
```

Then you can write a pipeline like this:

```python
y = 1 | add_1 | multiply_2 | subtract_3
```

which is equivalent to:

```python
y = subtract_3(
        multiply_2(
            add_1(1)))
```

Note that a `func_pipe` object is callable, so you can use it as a normal function if you need as the above code.

## Plain argument passing
The first way to pass an argument to a `func_pipe` object is to use the operator `|` as you see above:

```python
from dpl.pipe import func_pipe
@func_pipe
def sum_all(array):
    return sum(array)
y = (1, 2, 3) | sum_all
```

which is equivalent to:
```python
def sum_all(array):
    return sum(array)
y = sum_all((1, 2, 3))
```

## Unpacking argument passing
### Unpacking a tuple of arguments
You can pass a tuple of arguments and unpack them when passing to a `func_pipe` object by using the operator `>>`. For example:

```python
@func_pipe
def my_sum(x, y, z):
    return x + y + z
y = (1, 2, 3) >> my_sum
```

is equivalent to:
```python
def my_sum(x, y, z):
    return x + y + z
y = my_sum(1, 2, 3)
```

### Unpacking a dictionary of arguments
You can also pass a dictionary of arguments and unpack them when passing to a `func_pipe` object by using the operator `>>`. For example:

```python
from dpl.pipe import func_pipe
@func_pipe
def my_sum(x, y, z):
    return x + y + z
y = {'x': 1, 'y': 2, 'z': 3} >> my_sum
```

is equivalent to:

```python
def my_sum(x, y, z):
    return x + y + z
y = my_sum(x=1, y=2, z=3)
```

### Passing `numpy.ndarray`, `pandas.DataFrame` objects and other objects having definitions for operators `|` or `>>`
Because `numpy.ndarray` and `pandas.DataFrame` classes define the `|` and `>>`
operators, so to pass their objects to a `func_pipe` object, you need to wrap
them in a tuple or a list and passing with unpacking operator `>>`. For example:

```python
import numpy as np
from dpl.pipe import func_pipe
@func_pipe
def my_sum(array):
    return sum(array)
y = [np.array((1, 2, 3))] >> my_sum
```


## Partially apply a `func_pipe` object
You can partially apply a `func_pipe` object as follows:

```python
from dpl.pipe import func_pipe
@func_pipe
def my_sum(x, y, z):
    return x + y + z
y = (1, 2) >> my_sum.partial(z=3)
```

and that is equivalent to:

```python
def my_sum(x, y, z):
    return x + y + z
y = my_sum(x=1, y=2, z=3)
```

The same way is applied for keyword parameters.

```python
from dpl.pipe import func_pipe
@func_pipe
def my_sum(x, y, z):
    return x + y + z
y = {'x': 1, 'y': 2} >> my_sum.partial(z=3)
```

# Function composition as a function chain
Assume that you have the following functions:

```python
def add_1(x):
    return x + 1

def multiply_2(x):
    return x * 2

def subtract_3(x):
    return x - 3
```

and you want to compose them to calculate a value:

```python
y = subtract_3(
        multiply_2(
            add_1(1)))
```

You compute `y` by adding 1 to `x=1`, then multiplying the result by 2, and finally subtracting the previous result by 3 but you write the code in the following order: `subtract_3`, `multiply_2`, and `add_1`. With the helper `dpl.pipe.chain_pipe`, we can rewrite it a more natural order:

```python
from dpl.pipe import chain_pipe
y = 1 | chain_pipe(add_1, multiply_2, subtract_3)
```

The third last in the above code will do exactly the same thing as the way we compose three functions but it is much easier to read.
Another advantage of `chain_pipe` is that you can chain the `lambda` functions:

```python
from dpl.pipe import chain_pipe
y = 1 | chain_pipe(
    lambda x: x + 1,
    lambda x: x * 2,
    lambda x: x - 3
)
```

You can also control how to pass the arguments between the functions in the chain pipe by setting the keyword parameter `unpacked` (default `False`). The meaning of unpacking arguments while passing is described in the section of `func_pipe`.
For example, the following code:

```python
from dpl.pipe import chain_pipe
y = (1, 2) >> chain_pipe(
    lambda x: x + 1, x + 2,
    lambda x, y: x * 2, y * 2,
    lambda x, y: x - 3, y - 3,
    unpacked=True
)
```

is equivalent to:

```python
def add_1_2(x, y):
    return x + 1, y + 2

def multiply_2(x, y):
    return x * 2, y * 2

def subtract_3(x, y):
    return x - 3, y - 3
y = subtract_3(
        *multiply_2(
            *add_1_2(1, 2)))
```

# `pipe_class` decorator
This decorator will turns all instance methods into `func_pipe` objects that you can use to build pipelines later.

For example:

```python
from dpl.pipe import pipe_class

@pipe_class
class MyClass(object):
    def add_1(self, x):
        return x + 1

    def multiply_2(self, x):
        return x * 2

    def subtract_3(self, x):
        return x - 3

    def main(self):
        y = 1 | self.add_1 | self.multiply_2 | self.subtract_3
```

is equivalent to:

```python
class MyClass(object):
    def add_1(self, x):
        return x + 1

    def multiply_2(self, x):
        return x * 2

    def subtract_3(self, x):
        return x - 3

    def main(self):
        y = self.subtract_3(
            self.multiply_2(
                self.add_1(1)))
```

# `map_pipe`, `reduce_pipe`, `filter_pipe` function
Those are helpers for writing codes with traditional `map`, `reduce`, `filter` functions in a more readable way. The `map_pipe` function accepts a function which is the function will be applied on all elements of an array and return a `func_pipe` object that you can use to build pipelines later.
For example:

The following code

```python
from dpl.pipe import map_pipe
y = (1, 2, 3) | map_pipe(lambda x: x + 1)
```

is equivalent to:
```python
y = map(lambda x: x + 1, (1, 2, 3))
```

The same principle is applied for `reduce_pipe` and `filter_pipe`.

# `ConstantInstanceVariables` class
Sometimes, you want to force all instance variables to be constants or cannot be reassigned so that you guarantee that there is no place in you code changing those variables to avoid some bugs. This can be done by subclassing the class `ConstantInstanceVariables`.

For example, the following code:

```python
from dpl.constant import ConstantInstanceVariables
class MyClass(ConstantInstanceVariables):
    def __init__(self, value):
        self._value = value
    def main(self):
        self._value = 1

MyClass(10).main()
```

will raise the error

```python
ConstantError: Cannot rebind constant "_value"
```

as I am trying to rebind the instance variable `self._value` in the main method.

# Converting return results into constant objects

When a function returns a tuple of results, the code using this result will need to know the position of each arguments in the tuple result.
For example:

```python
def add_1(x, y, x):
    x_prime = x + 1
    y_prime = y + 1
    z_prime = z + 1
    return x_prime, y_prime, z_prime

y_prime = add_1(1, 2, 3)[1]
```

It is much easier to use the result if we combine the result variables into an immutable object. For example:

```python
from dpl.converter import vars_to_object
def add_1(x, y, z):
    x_prime = x + 1
    y_prime = y + 1
    z_prime = z + 1
    return vars_to_object(x_prime, y_prime, z_prime, local_dict=locals())

y_prime = add_1(1, 2, 3).y_prime
```

Remember to add the part `local_dict=locals()` when calling the function `vars_to_object`.

You can also convert a dictionary to an object or a `zip` pair. For example:

```python
from dpl.converter import dict_to_object
def add_1(x, y, z):
    x_prime = x + 1
    y_prime = y + 1
    z_prime = z + 1
    return dict_to_object({
        'x_prime': x_prime,
        'y_prime': y_prime,
        'z_prime': z_prime
    })

y_prime = add_1(1, 2, 3).y_prime
```

or

```python
from dpl.converter import zip_to_object
def add_1(x, y, z):
    x_prime = x + 1
    y_prime = y + 1
    z_prime = z + 1
    return zip_to_object(
        ('x_prime', 'y_prime', 'z_prime'),
        (x_prime, y_prime, z_prime))

y_prime = add_1(1, 2, 3).y_prime
```

# Caching a function result
Sometimes, it is useful to cache the result of a heavily computing function (or instance method). You can cache a function result by using the decorator `dpl.cache.func_cache` as follows:

```python
from dpl.cache import func_cache
@func_cache
def add_1(x):
    print(f'calling add_1 on x={x}')
    return x + 1

for i in range(3):
    y = add_1(1)
    print(f'i = {i}, y = {y}')
```

You will see the following result:

```python
calling add_1 on x=1
i = 0, y = 2
i = 1, y = 2
i = 2, y = 2
```

which means the function `add_1` is called to compute the result for `x=1` only once.
