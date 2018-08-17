import unittest
from dpl.cache import func_cache


@func_cache
def func(a_tuple, a_dict):
    print('computing for func')
    return a_tuple[0] + a_dict['x']


class ExampleClass(object):
    @func_cache
    def _method(self, a_tuple, a_dict):
        print('computing for method')
        return a_tuple[0] + a_dict['x']


class TestCache(unittest.TestCase):
    def test_func_cache(self):
        self.assertEqual(func._cache, {})
        for _ in range(3):
            result = func((1, 2), a_dict={'x': 2})
            self.assertEqual(result, 3)
            self.assertEqual(
                tuple(func._cache.values())[0],
                3)
        func.clear()
        self.assertEqual(func._cache, {})

    def test_method_cache(self):
        obj = ExampleClass()
        self.assertEqual(obj.__dict__[obj._method._cache_name], {})
        for _ in range(3):
            result = obj._method((1, 2), a_dict={'x': 2})
            self.assertEqual(result, 3)
            self.assertEqual(
                tuple(obj.__dict__[obj._method._cache_name].values())[0],
                3)
        obj._method.clear()
        self.assertEqual(obj.__dict__[obj._method._cache_name], {})
