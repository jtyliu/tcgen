from tcgen.utils.constants import LOWERCASE
from tcgen.primitives import *
from tcgen.primitives import SortableMixin
from tcgen.utils.random import *
import logging


__all__ = [
    'Array',
    'String',
    'NonDecreasing',
    'StrictlyIncreasing',
    'Permutation',
    'Graph',
    'Tree',
    'LineGraph',
]


class DataType:
    def __init__(self):
        self.value = None

    @property
    def is_generated(self):
        return self.value is not None

    def _generate(self):
        raise NotImplementedError

    def val(self):
        raise NotImplementedError

    def __str__(self) -> str:
        if not self.is_generated:
            self._generate()
        return str(self.value)


class Array(DataType):
    def __init__(self, N: int, *args, type: Primitive = Integer(), **kwargs):
        '''
        Create an array of a specified primitive datatype

        Args:
            N: Number of elements in the array
            type: Primitive data type to generate for each element

        Examples:
            Array(N)
            Array(N, 1e4)
            Array(N, U=1e4)
            Array(N, L=0, U=1e4)
            Array(N, 0, 1e4)
            Array(N, Integer(3))
            Array(N, 0, 1e4, Integer(3))
            Array(N, type=Integer(3))
            Array(N, type=Float(3))
            Array(N, 0, 1e4, type=Float()) # The bounds passed overwrite Float() bounds
            Array(N, 1e4, type=Float()) # The bounds passed overwrite Float() bounds
        '''
        # Most likely need to remove this later on for List()
        # if not isinstance(N, (int, float, Integer)):
        #     raise TypeError

        # TODO: Generate this number only when needed to, like with primitives
        self.N = N

        parse_idx = -1
        for idx, val in enumerate(args):
            if issubclass(val.__class__, Primitive):
                parse_idx = idx

        if parse_idx != -1:
            type = args[parse_idx]
            args = list(args)
            args.pop(parse_idx)
            args = tuple(args)

        if not issubclass(type.__class__, Primitive):
            raise TypeError

        self._type = type
        if parse_idx == -1:
            self._type.__init__(*args, **kwargs)
        else:
            # Only override default args passed to type is bounds are passed
            if len(args) != 0 or len(kwargs) != 0:
                self._type.__init__(*args, **kwargs)
        self.idx = 0
        DataType.__init__(self)

    def _generate(self):
        self.value = []
        for _ in range(self.N):
            self.value.append(self._type._generate())

    def shuffle(self):
        super().__str__()
        random.shuffle(self.value)
        return self

    def assign(self, *args, **kwargs):
        self._type.__init__(*args, **kwargs)
        return self

    def val(self):
        self.N = int(self.N)
        super().__str__()
        return self.value

    def __iter__(self):
        return self

    def __next__(self):
        self.val()
        try:
            ret = self.value[self.idx]
            self.idx += 1
            return ret
        except IndexError:
            self.idx = 0
            raise StopIteration

    def __str__(self):
        self.val()
        return ' '.join(map(str, self.value))

    def __getitem__(self, item):
        self.val()
        return self.value[item]


class String(Array):

    def __init__(self, N: int, char_set: str = LOWERCASE, *args, **kwargs):
        Array.__init__(self, N, *args, type=Char(), char_set=char_set, **kwargs)

    def _generate(self):
        self.value = ''
        for _ in range(self.N):
            self.value += self._type._generate()

    def __str__(self):
        super().__str__()
        return self.value


class NonDecreasing(Array):

    def __init__(self, N: int, *args, increasing: bool = True, **kwargs):
        self.increasing = increasing

        Array.__init__(self, N, *args, **kwargs)

        if not issubclass(self._type.__class__, SortableMixin):
            raise TypeError

    def _generate(self):
        self.value = []
        for _ in range(self.N):
            self.value.append(self._type._generate())
        self._sort()

    def _sort(self):
        self.value.sort(reverse=not self.increasing)

    def __str__(self):
        return super().__str__()


class StrictlyIncreasing(NonDecreasing):

    def __init__(self, N: int, *args, **kwargs):
        NonDecreasing.__init__(self, N, *args, **kwargs)

        if N > self._type._total_values():
            raise ValueError('Asked for more values than can generate')

    def _generate(self):
        # Bad memory comlpextity
        # O(max(a_i))
        # TODO: There's a better O(N) memory solution, using a nested binary search
        # We need a DS which supports O(logn) insertion and sorting
        tot_vals = self._type._total_values()
        bit = [0] * (tot_vals + 1)

        def update(idx, val):
            while idx <= tot_vals:
                bit[idx] += val
                idx += idx & -idx

        def query(idx):
            ret = 0
            while idx:
                ret += bit[idx]
                idx -= idx & -idx
            return ret

        for idx in range(1, tot_vals + 1):
            update(idx, 1)

        self.value = []
        for cnt in range(self.N):
            to_pick = random.randint(1, tot_vals - cnt)
            l_ptr, r_ptr = 1, tot_vals
            while l_ptr <= r_ptr:
                m_ptr = (l_ptr + r_ptr) // 2
                if query(m_ptr) < to_pick:
                    l_ptr = m_ptr + 1
                else:
                    r_ptr = m_ptr - 1
            update(l_ptr, -1)
            self.value.append(self._type._kth_smallest(l_ptr))
        self._sort()


class Permutation(Array):

    def __init__(self, N: int):
        # For now, it's 1 indexed.
        # Later on, I should consider if I should suppport other types
        # TODO
        Array.__init__(self, N, N)

    def _generate(self):
        self.value = []
        tot_vals = self._type._total_values()
        for idx in range(1, tot_vals + 1):
            self.value.append(self._type._kth_smallest(idx))
        self.shuffle()


class Graph(DataType):
    # weighted = False
    # connected = True
    # directed = False
    def __init__(
        self,
        N: int,
        M: int,
        W: Primitive = None,
        *,
        connected: bool = True,
        duplicate: bool = False,
        dag: bool = False,
        self_edge: bool = False,
    ):
        if connected and M < N - 1:
            raise TypeError('Not enough edges for connected graph')
        # TODO: log a warning if it's not connected and there's too many edges
        if not duplicate and M > N * (N - 1) // 2:
            raise TypeError('Too many edges for connected graph')

        if W and not issubclass(W.__class__, Primitive):
            raise TypeError('Weight passed is not a primitive data type')

        if dag and self_edge:
            raise TypeError('A dag cannot have self loops')

        self.N = N
        self.M = M
        self.W = W
        self.dag = dag
        self.connected = connected
        self.self_edge = self_edge
        self.duplicate = duplicate
        DataType.__init__(self)

    def _make_edge(self, u, v):
        if self.dag and u > v:
            u, v = v, u
        if self.W:
            return (u, v, self.W._generate())
        return (u, v)

    def _generate_prufer(self):
        return Array(self.N - 2, Integer(1, self.N)).val()

    def _generate(self):
        self.value = []
        logging.info('Generating tree')
        if self.connected:
            # https://cp-algorithms.com/graph/pruefer_code.html
            prufer = self._generate_prufer()
            degree = [0] + [1] * (self.N)
            for val in prufer:
                degree[val] += 1
            ptr = 0
            while degree[ptr] != 1:
                ptr += 1
            leaf = ptr
            for val in prufer:
                self.value.append(self._make_edge(leaf, val))
                degree[val] -= 1
                if degree[val] == 1 and val < ptr:
                    leaf = val
                else:
                    ptr += 1
                    while degree[ptr] != 1:
                        ptr += 1
                    leaf = ptr

        value_set = set(self.value)
        integer = Integer(1, self.N)
        logging.info('Generating the rest of the edges')
        for _ in range(len(self.value), self.M):
            u, v = integer._generate(), integer._generate()
            while not self.self_edge and u == v:
                u, v = integer._generate(), integer._generate()
            while not self.duplicate and any(edge in value_set for edge in [(u, v), (v, u)]):
                u, v = integer._generate(), integer._generate()

            value_set.add(self._make_edge(u, v))
            self.value.append(self._make_edge(u, v))

    def val(self):
        self.N = int(self.N)
        self.M = int(self.M)
        super().__str__()
        return self.value

    def __str__(self):
        self.val()
        ret = [' '.join(map(str, v)) for v in self.value]
        return '\n'.join(ret)


class Tree(Graph):
    def __init__(self, N: int, W: Primitive = None):
        Graph.__init__(self, N, N - 1, W)


class LineGraph(Tree):
    def __init__(self, N: int, W: Primitive = None):
        Tree.__init__(self, N, W)

    def _generate_prufer(self):
        return Permutation(self.N).val()[:self.N - 2]
