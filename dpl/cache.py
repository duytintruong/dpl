class func_cache(object):
    '''
        A decorator to cache the function or method result.
    '''
    def __init__(self, function):
        self._function = function
        self._function_self = None
        self.__doc__ = function.__doc__
        self.__name__ = function.__name__
        self._cache_name = f'_{function.__name__}_cache_'
        self._cache = {}

    def __call__(self, *args, **kwargs):
        if self._function_self:
            cache = self._function_self.__dict__[self._cache_name]
        else:
            cache = self._cache
        key = str(args) + str(kwargs)
        if key not in cache:
            if self._function_self:
                cache[key] = self._function(
                    self._function_self, *args, **kwargs)
            else:
                cache[key] = self._function(*args, **kwargs)
        return cache[key]

    def __get__(self, instance, owner):
        self._function_self = instance
        if self._cache_name not in instance.__dict__:
            instance.__dict__[self._cache_name] = {}
        return self

    def clear(self):
        if self._function_self:
            self._function_self.__dict__[self._cache_name] = {}
        else:
            self._cache = {}
