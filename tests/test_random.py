from tcgen.utils.constants import LOWERCASE
from tcgen.utils import random, InvalidRangeException
import pytest


class TestRandom:
    def setup_method(self):
        random.seed(0)

    def test_randint(self):
        with pytest.raises(TypeError):
            random.randint()
        with pytest.raises(TypeError):
            random.randint(1, 2, 3, 4)
        with pytest.raises(InvalidRangeException):
            random.randint(10, 1)
        with pytest.raises(InvalidRangeException):
            random.randint(1, 2, False)
        assert random.randint(1, 100000) == 50495
        assert random.randint(L=12345, U=123456) == 111691
        assert random.randint(1, 3, False) == 2

    def test_wrandint(self):
        with pytest.raises(TypeError):
            random.wrandint()
        with pytest.raises(InvalidRangeException):
            random.wrandint(10, 1)
        with pytest.raises(InvalidRangeException):
            random.wrandint(1, 2, inclusive=False)
        assert random.wrandint(1, 100000) == 99347
        assert random.wrandint(1, 3, inclusive=False) == 2
        assert random.wrandint(1, 100000, -10) == 12430

    def test_noise(self):
        with pytest.raises(InvalidRangeException):
            random.noise(10, 1, [1, 1, 2, 3, 4])
        assert random.noise(1, 1000, [0, 0, 0, 0, 9999, 0, 0]) == [
            865,
            395,
            777,
            912,
            10430,
            42,
            266,
        ]
        assert random.noise(1, 100, []) == []

    def test_randfloat(self):
        with pytest.raises(InvalidRangeException):
            random.randfloat(1.15, 1.13, 2)
        with pytest.raises(InvalidRangeException):
            random.randfloat(1.00, 1.02, 1, inclusive=False)
        with pytest.raises(InvalidRangeException):
            random.randfloat(1.0, 1.1, 1, inclusive=False)
        assert random.randfloat(1.15, 2.35, 2) == 2.22
        assert random.randfloat(1.15, 2.35, 3) == 1.938
        assert random.randfloat(100, 200, 1, inclusive=False) == 177.7
        assert random.randfloat(1.00, 1.02, 2, inclusive=False) == 1.01
        assert random.randfloat(1.0, 1.2, 1, inclusive=False) == 1.1

    def test_wrandfloat(self):
        with pytest.raises(InvalidRangeException):
            random.wrandfloat(1.15, 1.13, 2)
        with pytest.raises(InvalidRangeException):
            random.wrandfloat(1.00, 1.02, 1, inclusive=False)
        with pytest.raises(InvalidRangeException):
            random.wrandfloat(1.0, 1.1, 1, inclusive=False)
        assert random.wrandfloat(1.15, 2.35, 2) == 2.27
        assert random.wrandfloat(1.15, 2.35, 3, wcnt=-10) == 1.435
        assert random.wrandfloat(100, 200, 1, inclusive=False) == 181.9
        assert random.wrandfloat(100, 200, 1, wcnt=-10, inclusive=False) == 110.2

    def test_choice(self):
        with pytest.raises(TypeError):
            random.choice("")
        assert random.choice(".#") == "#"
        assert random.choice(".#") == "#"
        assert random.choice(".#") == "."
        assert random.choice(LOWERCASE) == "i"

    def test_wchoice(self):
        assert (
            random.wchoice(LOWERCASE, list(range(1, len(LOWERCASE) + 1)), wcnt=10)
            == "a"
        )
        assert (
            random.wchoice(LOWERCASE, list(range(1, len(LOWERCASE) + 1)), wcnt=-50)
            == "z"
        )
        with pytest.raises(TypeError):
            random.wchoice("", [], wcnt=-50)

        with pytest.raises(TypeError):
            random.wchoice("aaa", [], wcnt=-50)

    def test_randprime(self):
        with pytest.raises(TypeError):
            random.randprime()
        with pytest.raises(TypeError):
            random.randprime(1, 2, 3, 4)
        with pytest.raises(InvalidRangeException):
            random.randprime(10, 1)
        with pytest.raises(InvalidRangeException):
            random.randprime(1, 2, False)
        assert random.randprime(1, 100000) == 50497
        assert random.randprime(L=12345, U=123456) == 111697
        assert random.randprime(1, 3, False) == 2

    def test_wrandprime(self):
        with pytest.raises(TypeError):
            random.wrandprime()
        with pytest.raises(InvalidRangeException):
            random.wrandprime(10, 1)
        with pytest.raises(InvalidRangeException):
            random.wrandprime(1, 2, inclusive=False)
        with pytest.raises(ValueError):
            random.wrandprime(8, 10)
        assert random.wrandprime(1, 100000) == 99347
        assert random.wrandprime(1, 3, inclusive=False) == 2
        assert random.wrandprime(1, 100000, -10) == 12433
