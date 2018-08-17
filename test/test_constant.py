from unittest import TestCase
import pytest

from dpl.constant import (
    ConstantInstanceVariables,
    ConstantError,
)


class SomeClass(ConstantInstanceVariables):
    def __init__(self, value):
        self.value = value


class TestConstant(TestCase):
    def test_constant_instance_variables(self):
        obj = SomeClass(1)
        with pytest.raises(ConstantError):
            obj.value = 10
