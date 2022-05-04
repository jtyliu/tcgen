from sympy import isprime
from tcgen.datatypes import *
from tcgen.datatypes import DataType
from tcgen.primitives import *
from tcgen.utils import random
from tcgen.utils.constants import *
import pytest
import sys

sys.setrecursionlimit(100000)


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
    def assert_arr(self, arr, N, L, U, type=None):
        if N:
            assert len(arr) == N
        for a in arr:
            assert L <= a <= U
            if type is not None:
                assert isinstance(a, type)

    def assert_str(self, str, N, L, U, type=None):
        arr = list(map(int, str.split(" ")))
        assert len(arr) == N
        self.assert_arr(arr, N, L, U, type)

    def test_array(self):
        N = 100
        arr = Array(N).val()
        self.assert_arr(arr, N, 1, 1e5, int)
        arr = Array(N, 1e4).val()
        self.assert_arr(arr, N, 1, 1e4, int)
        arr = Array(N, U=1e4).val()
        self.assert_arr(arr, N, 1, 1e4, int)
        arr = Array(N, L=0, U=10).val()
        self.assert_arr(arr, N, 0, 10, int)
        arr = Array(N, 0, 10).val()
        self.assert_arr(arr, N, 0, 10, int)
        arr = Array(N, type=Integer(3)).val()
        self.assert_arr(arr, N, 1, 3, int)
        arr = Array(N, type=Float(3)).val()
        self.assert_arr(arr, N, 1, 1e5, float)
        arr = Array(N, 0, 1e2, type=Float()).val()
        self.assert_arr(arr, N, 0, 1e2, float)
        arr = Array(N, 1e2, type=Float()).val()
        self.assert_arr(arr, N, 1, 1e2, float)
        arr = Array(N)
        self.assert_str(str(arr), N, 1, 1e5, int)
        arr = Array(N, wcnt=5)
        self.assert_str(str(arr), N, 1, 1e5, int)

    def test_integer(self):
        N = Integer(5)
        # Random value will be generated inside Array()
        # Providing an integer will not generate a random length
        arr = Array(N * 2).val()
        self.assert_arr(arr, None, 1, 1e5, int)
        assert 2 <= len(arr) <= 10

    def test_assign(self):
        N = 100
        arr = Array(N).assign(3, 10)
        self.assert_arr(arr.val(), N, 3, 10, int)

    def test_getitem(self):
        N = 100
        arr = Array(N).assign(3, 10)
        self.assert_arr(arr.val(), N, 3, 10, int)
        assert list(arr) == arr.val()
        arr_cpy = list(arr)
        for i in range(N):
            arr[i] == arr_cpy[i]

    def test_add(self):
        N = 100
        arr = Array(N, 10).add(1000).val()
        self.assert_arr(arr, N, 1001, 1010, int)
        arr = Array(N, 10)
        arr_cpy = list(arr)  # Force an array generation
        for a, b in zip(arr.add(1000).val(), arr_cpy):
            assert a == b + 1000

    def test_add_primitive(self):
        N = 100
        M = Integer(1000, 10000)
        arr = Array(N, 10).add(M).val()
        self.assert_arr(arr, N, 1 + M.val(), 10 + M.val(), int)
        arr = Array(N, 10)
        arr_cpy = list(arr)  # Force an array generation
        M = Integer(-10000, -100)

        for a, b in zip(arr.add(M).val(), arr_cpy):
            print(arr.val(), arr_cpy, M)
            assert a == b + M.val()

        with pytest.raises(TypeError):
            Array(5, Char()).add(100)

    def test_type(self):
        with pytest.raises(TypeError):
            Array(10, type=DataType())


class TestString(TestDataTypesMixin):
    def test_string(self):
        N = 100
        for c in String(N):
            assert c in LOWERCASE

        for c in String(N, char_set=UPPERCASE):
            assert c in UPPERCASE


class TestNonDecreasing(TestDataTypesMixin):
    def test_nondecreasing(self):
        N = 100
        arr = NonDecreasing(N, Prime(1000, 10000)).val()
        for a in arr:
            assert 1000 <= a <= 10000
            assert isprime(a)
        assert len(arr) == N
        for i in range(N - 1):
            assert arr[i] <= arr[i + 1]
        arr = NonDecreasing(N, Prime(1000, 10000), increasing=False).val()

        for i in range(N - 1):
            assert arr[i] >= arr[i + 1]


class TestStrictlyIncreasing(TestDataTypesMixin):
    def test_strictlyincreasing(self):
        N = 100
        arr = StrictlyIncreasing(N, Float(100, 110)).val()

        for a in arr:
            assert 100 <= a <= 110
            assert isinstance(a, float)

        assert len(arr) == N
        for i in range(N - 1):
            assert arr[i] < arr[i + 1]

        arr = StrictlyIncreasing(N, Integer(100, 1110)).val()
        for a in arr:
            assert 100 <= a <= 1110
            assert isinstance(a, int)

        assert len(arr) == N
        for i in range(N - 1):
            assert arr[i] < arr[i + 1]

        arr = StrictlyIncreasing(N, Prime(1, 10000)).val()
        for a in arr:
            assert 1 <= a <= 10000
            assert isprime(a)

        assert len(arr) == N
        for i in range(N - 1):
            assert arr[i] < arr[i + 1]

        with pytest.raises(ValueError):
            StrictlyIncreasing(1000, Integer(100, 110))
        with pytest.raises(TypeError):
            StrictlyIncreasing(10, Char())


class TestPermutation(TestDataTypesMixin):
    def test_permutation(self):
        N = 100
        arr = Permutation(N).val()
        assert sorted(arr) == list(range(1, N + 1))


class TestGraphMixin:
    def has_duplicate_edge(self, N, edges):
        return len(set(edges)) != len(edges)

    def has_self_edge(self, N, edges):
        for edge in edges:
            if edge[0] == edge[1]:
                return True
        return False

    def is_connected(self, N, edges):
        ufds = [val for val in range(N + 1)]

        def find_set(u):
            if ufds[u] == u:
                return u
            ufds[u] = find_set(ufds[u])
            return ufds[u]

        def union_set(u, v):
            ufds[find_set(u)] = find_set(v)

        def is_same_set(u, v):
            return find_set(u) == find_set(v)

        for edge in edges:
            union_set(edge[0], edge[1])

        for node in range(1, N + 1):
            if not is_same_set(1, node):
                return False
        return True

    def is_tree(self, N, edges):
        if N != len(edges) + 1:
            return False

        graph = [[]] * (N + 1)
        visited = [False] * (N + 1)
        is_tree = True

        def dfs(u, p):
            global is_tree
            if visited[u]:
                is_tree = False
                return
            visited[u] = True
            for edge in graph[u]:
                if edge[0] != p:
                    dfs(edge[0], u)

        for edge in edges:
            graph[edge[0]].append(edge[1:])

        dfs(1, -1)
        return is_tree

    def assert_str(self, str, N, M, W: Primitive = None, type=None):
        edges = str.split("\n")
        assert len(edges) == M
        for edge in edges:
            vals = edge.split(" ")
            assert not (bool(W) ^ bool(type))
            if W:
                u, v, w = vals
                assert W.L <= type(w) <= W.U
                # TODO: Figure out how to check the bounds of w
            else:
                u, v = vals
            assert 1 <= int(u) <= N
            assert 1 <= int(v) <= N


class TestGraph(TestDataTypesMixin, TestGraphMixin):
    def test_graph(self):
        with pytest.raises(TypeError):
            Graph(10, 1 + 10 * (10 - 1) // 2)
        with pytest.raises(TypeError):
            Graph(10, 200)
        with pytest.raises(TypeError):
            Graph(10, 8)
        with pytest.raises(TypeError):
            Graph(10, 20, dag=True, self_edge=True)
        with pytest.raises(TypeError):
            Graph(10, 15, Array(5))

        N = 100
        M = 300

        edges = Graph(N, N, Integer(1, 10)).val()

        assert not self.is_tree(N, edges)
        assert self.is_connected(N, edges)
        assert not self.has_self_edge(N, edges)
        assert not self.has_duplicate_edge(N, edges)

        graph = Graph(N, M, Integer(1, 10))
        self.assert_str(str(graph), N, M, Integer(1, 10), int)
        graph = Graph(N, M).val()
        assert len(graph) == M
        for edge in graph:
            assert len(edge) == 2
            assert 1 <= edge[0] <= N
            assert 1 <= edge[1] <= N
        graph = Graph(N, M)
        self.assert_str(str(graph), N, M)

    def test_adjmatrix(self):
        N = 10
        M = 20
        graph = Graph(N, M).adj_matrix().val()
        assert len(graph) == N
        for arr in graph:
            assert len(graph) == N

        assert sum([sum(i) for i in graph]) == M * 2

        graph = Graph(N, M).adj_matrix()
        graph = str(graph).split("\n")

        assert len(graph) == N
        tot = 0
        for edges in graph:
            edges = list(map(int, edges.split(" ")))
            assert len(edges) == N
            tot += sum(edges)
        assert tot == M * 2

        g = Graph(N, M, Integer())
        graph = g.adj_matrix().val()
        assert len(graph) == N
        tot = 0
        for edges in graph:
            assert len(edges) == N
            for edge in edges:
                if edge:
                    tot += 1
                    assert 1 <= edge <= 1e5
        print(g.val())
        assert tot == M * 2


class TestTree(TestDataTypesMixin, TestGraphMixin):
    def test_tree(self):
        # assert Tree(10).val() == [(2, 7), (3, 7), (4, 1), (1, 5), (6, 9), (9, 8), (8, 7), (7, 5), (5, 10)]
        for _ in range(20):
            edges = Tree(100).val()
            assert self.is_tree(100, edges)


class TestLineGraph(TestDataTypesMixin, TestGraphMixin):
    def test_linegraph(self):
        edges = LineGraph(10).val()
        assert self.is_tree(10, edges)
        assert self.is_connected(10, edges)
        assert not self.has_duplicate_edge(10, edges)
        assert not self.has_self_edge(10, edges)
        degree = [0] * (10 + 1)
        for edge in edges:
            degree[edge[0]] += 1
            degree[edge[1]] += 1
        assert all(deg <= 2 for deg in degree)


class TestGrid(TestDataTypesMixin, TestGraphMixin):
    def test_grid(self):
        with pytest.raises(TypeError):
            Grid(3, 4, Array(5))

        N = 100
        M = 300

        grid = Grid(N, M).val()
        assert len(grid) == N
        for arr in grid:
            assert len(arr) == M

        grid = str(Grid(N, M)).split("\n")
        assert len(grid) == N
        for arr in grid:
            assert len(arr.split(" ")) == M

        grid = Grid(N, M).set(0).val()
        assert len(grid) == N
        for arr in grid:
            assert len(arr) == M
            for cell in arr:
                assert cell == 0

        grid = Grid(N, M)
        grid_arr = grid.val()
        for i in range(N):
            for j in range(M):
                assert grid[i][j] == grid_arr[i][j]


class TestDAG(TestDataTypesMixin, TestGraphMixin):
    def test_dag(self):
        with pytest.raises(TypeError):
            DAG(5, 10, self_edge=True)
        N = 100
        M = 300
        graph = DAG(N, M).val()
        for edge in graph:
            u, v = edge
            assert 1 <= u < v <= N
