from tcgen.datatypes import *
from tcgen.datatypes import DataType
from tcgen.primitives import *
from tcgen.utils import random
from tcgen.utils.constants import *
import pytest


class TestDataTypesMixin:

    def setup_method(self):
        random.seed(0)


class TestDataTypes(TestDataTypesMixin):

    def test_generate(self):
        with pytest.raises(NotImplementedError):
            DataType()._generate()
        with pytest.raises(NotImplementedError):
            DataType().val()


class TestArray(TestDataTypesMixin):

    def test_array(self):
        N = 10
        assert Array(N).val() == [50495, 99347, 55126, 5307, 33937, 67014, 63692, 53076, 39756, 62469]
        assert Array(N, 1e4).val() == [5867, 9559, 3579, 8269, 2282, 4618, 2290, 1554, 4105, 8726]
        assert Array(N, U=1e4).val() == [9862, 2408, 5082, 1619, 1209, 5410, 7736, 9172, 1650, 5797]
        assert Array(N, L=0, U=1e4).val() == [7113, 5180, 3350, 9052, 7815, 7253, 8541, 4267, 1020, 8989]
        assert Array(N, 0, 1e4).val() == [230, 1528, 6534, 18, 8086, 5458, 3996, 5328, 1031, 3130]
        assert Array(N, type=Integer(3)).val() == [74385, 29060, 31276, 18678, 71171, 58717, 11956, 10545, 41951, 66577]
        assert Array(N, type=Float(3)).val() == [82089.7, 18297.87, 50575.37, 92488.29, 48837.91, 20940.76, 91846.34, 55827.27, 90645.54, 34092.61]
        assert Array(N, 0, 1e4, type=Float()).val() == [8382.6, 6324.85, 5738.12, 6161.61, 3016.3, 4666.04, 960.83, 6252.52, 8366.95, 4035.98]
        assert Array(N, 1e4, type=Float()).val() == [3325.47, 6037.13, 2539.67, 3045.32, 1929.0, 1986.91, 8614.7, 1959.0, 346.74, 6426.39]
        assert str(Array(N)) == '86070 34087 62460 9056 11774 88962 99301 17069 19602 5065'
        assert str(Array(N, 1e4)) == '1315 8858 6411 8595 4516 8550 3859 3526 9664 6872'
        assert str(Array(N, U=1e4)) == '9498 4510 7383 8072 5856 1350 5314 1890 7970 9619'
        assert str(Array(N, L=0, U=1e4)) == '5493 3119 3981 265 4440 1919 3612 6095 2793 5448'
        assert str(Array(N, 0, 1e4)) == '6981 1018 1648 2397 3584 741 9402 8752 9865 1212'
        assert str(Array(N, type=Integer(3))) == '3500 16312 83231 24710 79474 75492 15689 51277 11998 48515'
        assert str(Array(N, type=Float(3))) == '19470.31 6106.57 3631.0 32647.94 31034.14 20787.15 80403.06 35329.87 10249.34 3823.28'
        assert str(Array(N, 0, 1e4, type=Float())) == '5706.72 4462.93 6507.46 1064.3 8765.07 2725.45 734.04 2315.56 754.67 6783.5'
        assert str(Array(N, 1e4, type=Float())) == '3157.85 3674.09 4573.51 1891.77 641.07 5282.01 4899.22 413.91 6255.59 1059.23'
        assert Array(N, weighted=True).val() == [95893, 91449, 88632, 87243, 89297, 86196, 97200, 96865, 99899, 88265]
        assert Array(N, 1e9, weighted=True).val() == [803680594, 890027575, 750097452, 939978709, 939027650, 829128097, 753247254, 975000373, 949053721, 899513086]
        assert Array(N, U=1e9, weighted=True).val() == [939541626, 899203368, 728549939, 883401125, 657196529, 938078652, 990816454, 981272369, 924878154, 877540437]
        assert Array(N, Integer(3)).val() == [1, 1, 2, 1, 1, 1, 1, 3, 2, 3]
        assert Array(N, 0, 1e4, Integer(3)).val() == [5156, 6011, 9297, 688, 9954, 8101, 7514, 7134, 6102, 8813]

    def test_integer(self):
        N = Integer(5)
        M = Integer(5)
        # Random value will be generated inside Array()
        # Providing an integer will not generate a random length
        assert Array(N * 2).val() == [99347, 55126, 5307, 33937, 67014, 63692, 53076, 39756]
        assert Array(2 * M).val() == [46931, 76466, 28632, 66151, 18255, 36942, 18317, 99065, 12430]

    def test_assign(self):
        arr = Array(5).assign(3, 10)
        assert list(arr) == [9, 9, 3, 7, 10]
        assert list(arr) == [9, 9, 3, 7, 10]

    def test_getitem(self):
        arr = Array(5).assign(3, 10)
        assert list(arr) == [9, 9, 3, 7, 10]
        for test, val in zip(arr, [9, 9, 3, 7, 10]):
            assert test == val
        for idx in range(5):
            arr[idx] == [9, 9, 3, 7, 10][idx]

    def test_type(self):
        with pytest.raises(TypeError):
            Array(10, type=DataType())


class TestString(TestDataTypesMixin):

    def test_string(self):
        assert str(String(10)) == 'mynbiqpmzj'
        assert str(String(10, char_set=UPPERCASE)) == 'PLSGQEJEYD'


class TestStrictlyIncreasing(TestDataTypesMixin):

    def test_strictlyincreasing(self):
        assert StrictlyIncreasing(5, Float(100, 110)).val() == [103.94, 104.31, 107.77, 108.64, 109.14]
        assert StrictlyIncreasing(5, Integer(100, 110)).val() == [100, 104, 105, 109, 110]
        with pytest.raises(ValueError):
            StrictlyIncreasing(1000, Integer(100, 110))
        with pytest.raises(TypeError):
            StrictlyIncreasing(10, Char())
