# tcgen
Yet another test case generator (But hopefully better)

Quickly and painlessly generate testcases with a minimal amount of code

# Installation

```bash
python3.7 -m pip install cp-tcgen
```

# Capabilities

tcgen creates several endpoints to generate data with several different methods

## Primitives
```
Primitive
Integer
Bool
Float
Char
Prime
```
## Datatypes
```
Array
String
NonDecreasing
StrictlyIncreasing
Permutation
Graph
Tree
LineGraph
Grid
DAG
StarGraph
KRegularTree
```

# Examples
https://dmoj.ca/problem/dpa

```python
from tcgen import *
# Bounds are 1..1e5 by default
N = Integer(2, 100000)
print(N)
print(Array(N, Integer(10000)))
```

https://dmoj.ca/problem/dpb
```python
from tcgen import *
class Gen(Generator):
    def generate(self, case_num):
        N = Integer(L=2, wcnt=20)  # Weighted random
        K = Integer(100)
        self.p(N, K)
        self.p(Array(N, U=10000))

gen = Gen()
print(gen.get_test_cases(10))
print(gen.get_test_case())
```

```python
from tcgen import *
A, B = Integer(), Integer()
print(A, B)
# 1 <= N <= A+B
N = Integer(A + B)
print(N)
```

```python
from tcgen import *
N = Integer()
print(N)
M = Integer(2 * N)
print(M)
print(Graph(N, M).shuffle())
```

```python
from tcgen import *
N = Integer()
print(N)
print(StrictlyIncreasing(N).shuffle())
```