class ConstantInstanceVariables(object):
    '''
        This class prevents rebinding the instance variables.
    '''
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise ConstantError('Cannot rebind constant "%s"' % name)
        self.__dict__[name] = value


class ConstantError(TypeError):
    pass
