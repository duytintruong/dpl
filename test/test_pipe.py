from unittest import TestCase

from dpl.pipe import (
    func_pipe, pipe_class,
    chain_pipe, map_pipe,
    filter_pipe, reduce_pipe
)


def add_1(value):
    return value + 1


def add_tuple_1(values):
    return tuple([v + 1 for v in values])


def sum_all(x, y, z):
    return x + y + z


class TestFuncPipe(TestCase):
    def test_func_pipe_for_single_input(self):
        test_pipe = func_pipe(add_1)
        self.assertEqual(1 >> test_pipe, 2)
        self.assertEqual(1 | test_pipe, 2)

    def test_func_pipe_for_tuple_input(self):
        test_pipe = func_pipe(add_tuple_1)
        self.assertEqual((1, 2) | test_pipe, (2, 3))

    def test_func_pipe_partial(self):
        result = (1, 2, 3) | (func_pipe(map).partial(lambda x: x+1) | tuple)
        self.assertEqual(result, (2, 3, 4))

    def test_unpacked_pipe(self):
        # unpack a dict
        result = {'y': 2, 'x': 1, 'z': 3} >> func_pipe(sum_all)
        self.assertEqual(result, 6)

        # unpack a tuple
        result = (1, 2, 3) >> func_pipe(sum_all)
        self.assertEqual(result, 6)

    def test_unpacked_and_partial_pipe(self):
        result = {'y': 2, 'x': 1} >> func_pipe(sum_all).partial(z=3)
        self.assertEqual(result, 6)

    def test_map_pipe(self):
        result = (1, 2) | (map_pipe(lambda x: x+1) | tuple)
        self.assertEqual(result, (2, 3))

    def test_filter_pipe(self):
        result = (1, 2, 3, 4) | (filter_pipe(lambda x: x % 2 == 0) | tuple)
        self.assertEqual(result, (2, 4))

    def test_reduce_pipe(self):
        result = (1, 2, 3, 4) | reduce_pipe(lambda x, y: x + y)
        self.assertEqual(result, 10)


class ExampleClassWithMethodPipe(object):
    @func_pipe
    def add_1(self, x, y):
        return x + 1, y + 1

    @func_pipe
    def add_2(self, x, y):
        return x + 2, y + 2

    @func_pipe
    def add_3(self, x, y):
        return x + y + 3

    @func_pipe
    def add_4(self, x):
        return x + 4

    def straight_pipe(self):
        return (1, 2) >> self.add_1 >> self.add_2 >> self.add_3 >> self.add_4

    def nested_pipe(self):
        return (1, 2) >> (self.add_1 >> self.add_2) >> self.add_3 >> self.add_4

    def pipe_call(self):
        return (self.add_1 >> self.add_2)(1, 2)

    def partial_pipe(self):
        return 2 | self.add_1.partial(1)


class TestMethodPipe(TestCase):
    def test_straight_pipe(self):
        test_obj = ExampleClassWithMethodPipe()
        self.assertEqual(test_obj.straight_pipe(), 16)

    def test_nested_pipe(self):
        test_obj = ExampleClassWithMethodPipe()
        self.assertEqual(test_obj.nested_pipe(), 16)

    def test_pipe_call(self):
        test_obj = ExampleClassWithMethodPipe()
        self.assertEqual(test_obj.add_1(1, 2), (2, 3))
        self.assertEqual(test_obj.pipe_call(), (4, 5))

    def test_partial_pipe(self):
        test_obj = ExampleClassWithMethodPipe()
        self.assertEqual(test_obj.partial_pipe(), (2, 3))

    def test_new_pipes(self):
        test_obj = ExampleClassWithMethodPipe()
        pipe_1 = test_obj.add_1 >> test_obj.add_2
        pipe_2 = test_obj.add_1 >> test_obj.add_2
        self.assertEqual((1, 2) >> pipe_1, (4, 5))
        self.assertEqual((1, 2) >> pipe_2, (4, 5))
        self.assertNotEqual(id(test_obj.add_1), id(pipe_1))
        self.assertNotEqual(id(test_obj.add_1), id(pipe_2))
        self.assertNotEqual(id(pipe_1), id(pipe_2))


@pipe_class
class ExampleClassWithClassPipe(object):
    def add_1(self, x, y):
        return x + 1, y + 1

    def add_2(self, x, y):
        return x + 2, y + 2

    def add_3(self, x, y):
        return x + y + 3

    def add_4(self, x):
        return x + 4

    def straight_pipe(self):
        return (1, 2) >> self.add_1 >> self.add_2 >> self.add_3 >> self.add_4

    def nested_pipe(self):
        return (1, 2) >> (self.add_1 >> self.add_2) >> self.add_3 >> self.add_4


class TestClassPipe(TestCase):
    def test_straight_pipe(self):
        test_obj = ExampleClassWithClassPipe()
        self.assertEqual(test_obj.straight_pipe(), 16)

    def test_nested_pipe(self):
        test_obj = ExampleClassWithClassPipe()
        self.assertEqual(test_obj.nested_pipe(), 16)


class TestChainPipe(TestCase):
    def test_chain_pipe_not_unpacked(self):
        result = '1.2' | chain_pipe(float, int, str, unpacked=False)
        self.assertEqual(result, '1')

    def test_list_unpacked(self):
        def count_args(*args):
            return len(args)
        result = 1.2 >> chain_pipe(str, list, count_args, unpacked=True)
        self.assertEqual(result, 3)
