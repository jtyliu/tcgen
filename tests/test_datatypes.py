from tcgen.datatypes import *
from tcgen.primitives import *
from tcgen.utils import random
from tcgen.utils.constants import *
# import pytest


class TestDataTypesMixin:

    def setup_method(self):
        random.seed(0)


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
