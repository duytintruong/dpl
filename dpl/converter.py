from collections import namedtuple, OrderedDict
from .pipe import func_pipe


@func_pipe
def dict_to_object(a_dict, type_name='NamedTuple'):
    '''
        This function converts a dictionary into a namedtuple object.
    '''
    return namedtuple(type_name, a_dict.keys())(**a_dict)


@func_pipe
def vars_to_object(*args, local_dict, type_name='NamedTuple'):
    '''
        This function converts the variables into a namedtuple object.
    '''
    a_dict = OrderedDict()
    for value in args:
        for k, val in local_dict.items():
            if val is value:
                a_dict[k] = val
    return dict_to_object(a_dict, type_name)


@func_pipe
def zip_to_object(first_list, second_list):
    '''
        This function zips and converts the zip result into
        a namedtuple object.
    '''
    return dict_to_object(dict(zip(first_list, second_list)))
