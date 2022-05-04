from sympy import isprime
from tcgen.primitives import *
from tcgen.primitives import Primitive, SortableMixin
from tcgen.utils import random, InvalidRangeException
from tcgen.utils.constants import *
import pytest
import re


class TestPrimitiveMixin:
    def setup_method(self):
        random.seed(0)

    def is_int(self, str):
        # Bleh, so hacky
        return re.match(r"(\d+)", str).groups()[0] == str
    
    def is_float(self, str):
        # Bleh, so hacky
        return re.match(r"(\d+\.\d+)", str).groups()[0] == str


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
        val = Integer().int()
        assert isinstance(val, int) and 1 <= val <= 1e5
        val = Integer().val()
        assert isinstance(val, int) and 1 <= val <= 1e5
        assert self.is_int(str(Integer()))

    def test_invalid_range(self):
        with pytest.raises(InvalidRangeException):
            Integer(1e9, 1)

    def test_multiple_args(self):
        with pytest.raises(TypeError):
            Integer(1, 2, 3)

    def test_valid_integer(self):
        assert 100 <= Integer(100, 110).int() <= 110

    # TODO: Use stats or something to test weighted randoms
    # def test_weighted_integer(self):
    #     assert Integer(1, 1e9, wcnt=25).int() == 985946605
    #     assert Integer(1, 1e9).int() == 976832603
    #     assert Integer(1, 1e9, wcnt=-10).int() == 79180333

    def test_exclusive(self):
        assert 1 < Integer(1, 3, inclusive=False).int() < 3
        assert 1 < Integer(1, 3).exclusive().int() < 3
        assert 1 <= Integer(1, 3).exclusive().inclusive().int() <= 3
        with pytest.raises(InvalidRangeException):
            Integer(1, 2, inclusive=False)

    def test_total_values(self):
        N = 100
        assert Integer(1, N)._total_values() == N
        assert Integer(1, N, inclusive=False)._total_values() == N - 2

    def test_default(self):
        assert Integer().default() == 0

    def test_kth_smallest(self):
        N = 100
        K = 15
        assert Integer(1, N)._kth_smallest(K) == K
        assert Integer(1, N, inclusive=False)._kth_smallest(K) == K + 1
        with pytest.raises(IndexError):
            Integer(1, N, inclusive=True)._kth_smallest(0)
        with pytest.raises(IndexError):
            Integer(1, N, inclusive=True)._kth_smallest(N + 1)

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
        val = Prime().int()
        assert isinstance(val, int) and 1 <= val <= 1e5 and isprime(val)
        assert self.is_int(str(Prime()))

    def test_invalid_range(self):
        with pytest.raises(InvalidRangeException):
            Prime(1e9, 1)

    def test_valid_prime(self):
        val = Prime(1, 1e9).int()
        assert 1 <= val <= 1e9 and isprime(val)
        val = Prime(1, 1e9).val()
        assert 1 <= val <= 1e9 and isprime(val)

    # TODO: Figure out how to test weighted randoms
    # def test_weighted_prime(self):
    #     assert Prime(1, 1e9, wcnt=25).int() == 985946617
    #     assert Prime(1, 1e9).int() == 976832621
    #     assert Prime(1, 1e9, wcnt=-10).int() == 79180349

    def test_total_values(self):
        def get_num_of_primes(L, U):
            tot = 0
            for i in range(L, U + 1):
                if isprime(i):
                    tot += 1
            return tot

        L = 100
        U = 5000
        assert Prime(L, U)._total_values() == get_num_of_primes(L, U)
        assert Prime(L, U, inclusive=False)._total_values() == get_num_of_primes(
            L + 1, U - 1
        )

    def test_kth_smallest(self):
        def get_kth_prime(L, K):
            cur = 0
            while K:
                if isprime(L):
                    cur = L
                    K -= 1
                L += 1
            return cur

        L = 1019
        U = 5000
        K = 15

        assert Prime(L, U)._kth_smallest(K) == get_kth_prime(L, K)
        assert Prime(L, U, inclusive=False)._kth_smallest(K) == get_kth_prime(L + 1, K)
        with pytest.raises(IndexError):
            Prime(1, 100, inclusive=True)._kth_smallest(0)
        with pytest.raises(IndexError):
            Prime(1, 100, inclusive=True)._kth_smallest(1000)

    def test_exclusive(self):
        assert 1 < Prime(1, 5, inclusive=False).int() < 5
        assert 1 < Prime(1, 5).exclusive().int() < 5
        assert 1 <= Prime(1, 5, wcnt=25).exclusive().inclusive().int() <= 5
        with pytest.raises(InvalidRangeException):
            Prime(1, 2, inclusive=False)
        with pytest.raises(ValueError):
            Prime(8, 10)


class TestBool(TestPrimitiveMixin):
    def test_bool(self):
        assert Bool().bool() in [0, 1]
        assert str(Bool()) in ["0", "1"]
        assert Bool().int() in [0, 1]


class TestFloat(TestPrimitiveMixin):
    def test_float(self):
        val = Float().float()
        assert isinstance(val, float) and 1 <= val <= 1e5
        assert self.is_float(str(Float()))

    def test_multiple_args(self):
        with pytest.raises(TypeError):
            Float(1, 2, 3)

    def test_cast(self):
        assert isinstance(int(Float(1, 1e9)), int)

    def test_invalid_range(self):
        with pytest.raises(InvalidRangeException):
            Float(1, 1.001, places=2, inclusive=False)

    def test_valid_float(self):
        assert isinstance(Float(1, 1e9).float(), float)

    # TODO: Test weighted randoms
    # def test_weighted_float(self):
    #     assert Float(1, 1e9, wcnt=25).float() == 987103120.89
    #     assert Float(1, 1e9).float() == 998318371.34
    #     assert Float(1, 1e9, wcnt=-10).float() == 105139493.52

    def test_total_values(self):
        L = 100
        U = 500
        assert Float(L, U)._total_values() == (U - L) * 100 + 1
        assert Float(L, U, inclusive=False)._total_values() == (U - L) * 100 - 1

    def test_kth_smallest(self):
        def get_kth_float(L, k, places=2):
            L *= 10**places
            return (L + k - 1) / (10**places)
        L = 500
        U = 5000
        K = 15
        assert Float(L, U)._kth_smallest(K) == get_kth_float(L, K)
        assert Float(L, U, inclusive=False)._kth_smallest(K) == get_kth_float(L, K + 1)
        with pytest.raises(IndexError):
            Float(1, 100, inclusive=True)._kth_smallest(0)
        with pytest.raises(IndexError):
            Float(1, 100, inclusive=True)._kth_smallest(10000)

    def test_exclusive(self):
        # TODO: Fix float it is able to generate values from 0 to 1
        # assert 1 < Float(1, 2, inclusive=False).float() < 2
        assert 1 < Float(1, 3).exclusive().float() < 3
        assert 1 <= Float(1, 3).exclusive().inclusive().float() <= 3
        with pytest.raises(InvalidRangeException):
            Float(1, 2, inclusive=False)

    def is_precise(self, val, places):
        val = str(val)
        if '.' not in val:
            return True
        val = len(val.split('.')[-1])
        return val <= places

    def test_places(self):
        places = 5
        assert self.is_precise(Float(1, 3, places=places), places)

    def test_round(self):
        assert self.is_precise(Float(1, 3, places=5).round(), 0)
        assert self.is_precise(Float(1, 3, places=2).round(1), 1)
        assert self.is_precise(round(Float(1, 100, places=2)), 2)
        assert self.is_precise(Float(1, 100, places=5), 5)


class TestChar(TestPrimitiveMixin):
    def test_char(self):
        with pytest.raises(TypeError):
            Char("")
        val = Char(LOWERCASE).char()
        assert len(val) == 1 and val in LOWERCASE
        assert Char("#.", [2, 1]).char() in "#."
        # TODO: Weighted random stats stuff
        # assert Char("#.", [2, 1], wcnt=10).char() == "."
        # assert Char("#.", wcnt=10).char() == "#"
        # assert Char("#.", wcnt=-10).char() == "."

    def test_invalid_permutation(self):
        with pytest.raises(TypeError):
            Char("#.", [3, 1, 2])
        with pytest.raises(TypeError):
            Char("#.", [0, 1])
        # TODO: Proper code for testing for no errors
        Char("#.", [2, 1])
        Char("#")
        with pytest.raises(TypeError):
            Char("#.", [2, 1], inclusive=True)

    def test_default(self):
        assert Char().default() == "a"
