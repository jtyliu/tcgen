from tcgen import *
import logging

# N = Integer(10, 20)

# print(StrictlyIncreasing(5, Float(100, 110)))
# print(NonDecreasing(5, Integer(100, 11000)))
logging.basicConfig(level=logging.INFO)
print(len(Tree(100000).val()))
print(len(Graph(100000, 200000).val()))
