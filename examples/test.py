from tcgen.datatypes import StrictlyIncreasing
from tcgen import *

N = Integer(10, 20)

print(StrictlyIncreasing(5, Float(100, 110)))
print(NonDecreasing(5, Integer(100, 11000)))
