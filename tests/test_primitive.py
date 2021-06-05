from tcgen.primitives import *
from tcgen.primitives import Primitive, SortableMixin
from tcgen.utils import random, InvalidRangeException
from tcgen.utils.constants import *
import pytest


class TestPrimitiveMixin:

    def setup_method(self):
        random.seed(0)


class TestSortableMixin:

    def test_not_implemented(self):
        with pytest.raises(NotImplementedError):
            SortableMixin()._total_values()
        with pytest.raises(NotImplementedError):
            SortableMixin()._kth_smallest(1)


class TestPrimitive:

    def test_extra_kwargs(self):
        # This should log a warning
        Primitive(a=1, b=1)

    def test_generate_value(self):
        with pytest.raises(NotImplementedError):
            Primitive()._generate_value()
        with pytest.raises(NotImplementedError):
            Primitive()._generate_weighted_value()
        with pytest.raises(NotImplementedError):
            Primitive().val()

    def test_default(self):
        with pytest.raises(NotImplementedError):
            Primitive().default()


class TestInteger(TestPrimitiveMixin):

    def test_integer(self):
        assert Integer().int() == 50495
        assert str(Integer()) == "99347"

    def test_invalid_range(self):
        with pytest.raises(InvalidRangeException):
            Integer(1e9, 1)

    def test_multiple_args(self):
        with pytest.raises(TypeError):
            Integer(1, 2, 3)

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

    def test_total_values(self):
        assert Integer(1, 100)._total_values() == 100
        assert Integer(1, 100, inclusive=False)._total_values() == 98

    def test_default(self):
        assert Integer().default() == 0

    def test_kth_smallest(self):
        assert Integer(1, 100)._kth_smallest(15) == 15
        assert Integer(1, 100, inclusive=False)._kth_smallest(30) == 31
        with pytest.raises(IndexError):
            Integer(1, 100, inclusive=True)._kth_smallest(0)
        with pytest.raises(IndexError):
            Integer(1, 100, inclusive=True)._kth_smallest(1000)

    def test_arithmetic(self):
        a = Integer(1, 3)
        b = Integer(1, 3)
        c = Integer(1, 3)
        d = Integer(1, 100)
        assert int(a + 5) == 7
        assert int(a - 5) == 2
        assert int(b - 5) == -3
        assert int(b + 5) == 2
        assert int(c * 10) == 11
        assert int(c / 10) == 1
        assert int(d / 10) == 4
        assert int(d * 10) == 40


class TestPrime(TestPrimitiveMixin):

    def test_prime(self):
        assert Prime().int() == 99347
        assert str(Prime()) == "5309"

    def test_invalid_range(self):
        with pytest.raises(InvalidRangeException):
            Prime(1e9, 1)

    def test_valid_prime(self):
        assert Prime(1, 1e9).int() == 413654009
        assert Prime(1, 1e9).val() == 955892131

    def test_weighted_prime(self):
        assert Prime(1, 1e9, weighted=True, wcnt=25).int() == 985946617
        assert Prime(1, 1e9, weighted=True).int() == 976832621
        assert Prime(1, 1e9, weighted=True, wcnt=-10).int() == 79180349

    def test_total_values(self):
        assert Prime(1, 100)._total_values() == 25
        assert Prime(5, 100, inclusive=False)._total_values() == 22

    def test_kth_smallest(self):
        assert Prime(1, 100)._kth_smallest(15) == 47
        assert Prime(1, 100, inclusive=False)._kth_smallest(3) == 5
        with pytest.raises(IndexError):
            Prime(1, 100, inclusive=True)._kth_smallest(0)
        with pytest.raises(IndexError):
            Prime(1, 100, inclusive=True)._kth_smallest(1000)

    def test_exclusive(self):
        assert Prime(1, 5, inclusive=False).int() == 3
        assert Prime(1, 5, weighted=True).exclusive().int() == 3
        assert Prime(1, 5, weighted=True, wcnt=25).exclusive().inclusive().int() == 5
        with pytest.raises(InvalidRangeException):
            Prime(1, 2, inclusive=False)
        with pytest.raises(ValueError):
            Prime(8, 10)


class TestBool(TestPrimitiveMixin):

    def test_bool(self):
        assert Bool().bool() == 1
        assert str(Bool()) == '1'
        assert Bool().int() == 0


class TestFloat(TestPrimitiveMixin):

    def test_float(self):
        assert Float().float() == 64634.43
        assert str(Float()) == "70561.20"

    def test_multiple_args(self):
        with pytest.raises(TypeError):
            Float(1, 2, 3)

    def test_cast(self):
        assert int(Float(1, 1e9)) == 551663718

    def test_invalid_range(self):
        with pytest.raises(InvalidRangeException):
            Float(1, 1.001, places=2, inclusive=False)

    def test_valid_float(self):
        assert Float(1, 1e9).float() == 551663718.89

    def test_weighted_float(self):
        assert Float(1, 1e9, weighted=True, wcnt=25).float() == 987103120.89
        assert Float(1, 1e9, weighted=True).float() == 998318371.34
        assert Float(1, 1e9, weighted=True, wcnt=-10).float() == 105139493.52

    def test_total_values(self):
        assert Float(1, 100)._total_values() == 9901
        assert Float(5, 100, inclusive=False)._total_values() == 9499

    def test_kth_smallest(self):
        assert Float(1, 100)._kth_smallest(15) == 1.14
        assert Float(1, 100, inclusive=False)._kth_smallest(3) == 1.03
        with pytest.raises(IndexError):
            Float(1, 100, inclusive=True)._kth_smallest(0)
        with pytest.raises(IndexError):
            Float(1, 100, inclusive=True)._kth_smallest(10000)

    def test_exclusive(self):
        assert Float(1, 3, inclusive=False).float() == 1.99
        assert Float(1, 3, weighted=True).exclusive().float() == 2.95
        assert Float(1, 3, weighted=True).exclusive().inclusive().float() == 3.00
        with pytest.raises(InvalidRangeException):
            Float(1, 2, inclusive=False)

    def test_places(self):
        assert Float(1, 3, places=5).float() == 2.00989
        assert Float(1, 3, places=1).float() == 2.3

    def test_round(self):
        assert Float(1, 3, places=5).round() == 2
        assert Float(1, 3, places=2).round(1) == 2.9
        assert round(Float(1, 100, places=2)) == 70
        assert round(Float(1, 100, places=5), 2) == 7.79


class TestChar(TestPrimitiveMixin):
    def test_char(self):
        with pytest.raises(TypeError):
            Char('')
        assert Char(LOWERCASE).char() == 'm'
        assert Char('#.', [2, 1], weighted=True).char() == '.'
        assert Char('#.', [2, 1], weighted=True, wcnt=10).char() == '.'
        assert Char('#.', weighted=True, wcnt=10).char() == '#'
        assert Char('#.', weighted=True, wcnt=-10).char() == '.'

    def test_invalid_permutation(self):
        with pytest.raises(TypeError):
            Char('#.', [3, 1, 2], weighted=True)
        with pytest.raises(TypeError):
            Char('#.', [0, 1], weighted=True)
        Char('#.', [2, 1])
        Char('#')
        with pytest.raises(TypeError):
            Char('#.', [2, 1], weighted=True, inclusive=True)

    def test_default(self):
        assert Char().default() == 'a'
