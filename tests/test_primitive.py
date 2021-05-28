from primitives import *
from utils import random, InvalidRangeException
from utils.constants import *
import pytest


class TestInteger:

    def setup_method(self):
        random.seed(0)

    def test_integer(self):
        assert Integer().int() == 50495
        assert str(Integer()) == "99347"

    def test_invalid_range(self):
        with pytest.raises(InvalidRangeException):
            Integer(1e9, 1)

    def test_valid_integer(self):
        assert Integer(1, 1e9).int() == 906691060

    def test_weighted_integer(self):
        assert Integer(1, 1e9, weighted=True, wcnt=25).int() == 985946605
        assert Integer(1, 1e9, weighted=True).int() == 976832603
        assert Integer(1, 1e9, weighted=True, wcnt=-10).int() == 79180333

    def test_exclusive(self):
        assert Integer(1, 3, inclusive=False).int() == 2
        assert Integer(1, 3, weighted=True).exclusive().int() == 2
        assert Integer(1, 3, weighted=True).exclusive().inclusive().int() == 3
        with pytest.raises(InvalidRangeException):
            Integer(1, 2, inclusive=False)


class TestBool:

    def setup_method(self):
        random.seed(0)

    def test_bool(self):
        assert Bool().bool() == 1
        assert str(Bool()) == '1'
        assert Bool().int() == 0
