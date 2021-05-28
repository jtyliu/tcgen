from primitives import *
from utils import random, InvalidRangeException
from utils.constants import *
import pytest


class TestPrimitiveMixin:

    def setup_method(self):
        random.seed(0)


class TestInteger(TestPrimitiveMixin):

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


class TestBool(TestPrimitiveMixin):

    def test_bool(self):
        assert Bool().bool() == 1
        assert str(Bool()) == '1'
        assert Bool().int() == 0


class TestFloat(TestPrimitiveMixin):

    def test_float(self):
        assert Float().float() == 64634.43
        assert str(Float()) == "70561.20"

    def test_invalid_range(self):
        with pytest.raises(InvalidRangeException):
            Float(1, 1.001, places=2, inclusive=False)

    def test_valid_float(self):
        assert Float(1, 1e9).float() == 551663718.89

    def test_weighted_float(self):
        assert Float(1, 1e9, weighted=True, wcnt=25).float() == 987103120.89
        assert Float(1, 1e9, weighted=True).float() == 998318371.34
        assert Float(1, 1e9, weighted=True, wcnt=-10).float() == 105139493.52

    def test_exclusive(self):
        assert Float(1, 3, inclusive=False).float() == 1.99
        assert Float(1, 3, weighted=True).exclusive().float() == 2.95
        assert Float(1, 3, weighted=True).exclusive().inclusive().float() == 3.00
        with pytest.raises(InvalidRangeException):
            Float(1, 2, inclusive=False)

    def test_places(self):
        assert Float(1, 3, places=5).float() == 2.00989
        assert Float(1, 3, places=1).float() == 2.3


class TestChar(TestPrimitiveMixin):
    def test_char(self):
        with pytest.raises(TypeError):
            Char('')
        assert Char(LOWERCASE).char() == 'm'
        assert Char('#.', [2, 1], weighted=True).char() == '.'
        assert Char('#.', [2, 1], weighted=True, wcnt=10).char() == '.'
        assert Char('#.', weighted=True, wcnt=10).char() == '#'
        assert Char('#.', weighted=True, wcnt=-10).char() == '.'
