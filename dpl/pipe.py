from functools import partial, reduce


class func_pipe(object):
    '''
        A decorator to convert This function or method into a pipe
        that allows using the '|', or '>>' operator to pass arguments.
    '''
    __name__ = "func_pipe"

    def __init__(self, function, chained_pipes=(), unpacked_args=()):
        self._function = function
        self._binding_function_self = False
        self.__doc__ = function.__doc__
        self._chained_pipes = chained_pipes
        self._unpacked_args = unpacked_args

    def __or__(self, another):
        if not isinstance(another, func_pipe):
            another = func_pipe(another)
        return func_pipe(
            self._function,
            self._chained_pipes + (another,),
            self._unpacked_args + (False,)
        )

    def __rshift__(self, another):
        if not isinstance(another, func_pipe):
            another = func_pipe(another)
        return func_pipe(
            self._function,
            self._chained_pipes + (another,),
            self._unpacked_args + (True,)
        )

    def __ror__(self, args):
        return self.__call__(args)

    def __rrshift__(self, args):
        if (isinstance(args, list) or isinstance(args, tuple)):
            return self.__call__(*args)
        elif isinstance(args, dict):
            return self.__call__(**args)
        else:
            return self.__call__(args)

    def __call__(self, *args, **kwargs):
        result = self._function(*args, **kwargs)
        for pipe, unpacked in zip(self._chained_pipes, self._unpacked_args):
            if unpacked and (isinstance(result, list) or isinstance(result, tuple)):
                result = pipe.__call__(*result)
            else:
                result = pipe.__call__(result)
        return result

    def partial(self, *args, **kwargs):
        return func_pipe(function=partial(self._function, *args, **kwargs))

    def __get__(self, instance, owner):
        if not self._binding_function_self:
            self._binding_function_self = True
            self._function = partial(self._function, instance)
        return self


def pipe_class(Cls):
    '''
        A decorator used to turn all instance methods into func_pipe objects.
    '''
    class ClassPipe(object):
        def __init__(self, *args, **kwargs):
            self._instance = Cls(*args, **kwargs)
            for attr in filter(lambda attr: callable(Cls.__dict__[attr]), Cls.__dict__):
                setattr(
                    self._instance, attr,
                    func_pipe(object.__getattribute__(self._instance, attr))
                )

        def __getattr__(self, attr):
            return object.__getattribute__(self._instance, attr)
    return ClassPipe


def chain_pipe(*args, unpacked=False):
    '''
        This function used to form a func_pipe by concatenating
        the functions passed to it.
    '''
    if len(args) < 1:
        raise Exception(
            'There must be at least 1 functions or methods to build a '
            'chain_pipe!')
    a_pipe = (
        args[0] if args[0] is isinstance(args[0], func_pipe)
        else func_pipe(args[0]))
    for func in args[1:]:
        a_pipe = (
            a_pipe >> func_pipe(func) if unpacked
            else a_pipe | func_pipe(func))
    return a_pipe


def map_pipe(func):
    '''
        This function partially applies the map function
        and return a func_pipe object.
    '''
    return func_pipe(partial(map, func))


def filter_pipe(func):
    '''
        This function partially applies the filter function
        and return a func_pipe object.
    '''
    return func_pipe(partial(filter, func))


def reduce_pipe(func):
    '''
        This function partially applies the reduce function
        and return a func_pipe object.
    '''
    return func_pipe(partial(reduce, func))
