from tcgen.primitives import *


__all__ = [
    'Array',
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
            Array(N, type=Integer(3))
            Array(N, type=Float(3))
            Array(N, 0, 1e4, type=Float()) # The bounds passed overwrite Float() bounds
            Array(N, 1e4, type=Float()) # The bounds passed overwrite Float() bounds
        '''
        # Most likely need to remove this later on for List()
        if not isinstance(N, (int, float, Integer)):
            raise TypeError

        # This too.
        self.N = int(N)

        if not issubclass(type.__class__, Primitive):
            raise TypeError

        self._type = type
        self._type.__init__(*args, **kwargs)
        DataType.__init__(self)

    def _generate(self):
        self.value = []
        for _ in range(self.N):
            self.value.append(self._type._generate())

    def assign(self, *args, **kwargs):
        self._type = self._type.__init__(*args, **kwargs)
        return self

    def val(self):
        super().__str__()
        return self.value

    def __str__(self):
        super().__str__()
        return ' '.join(map(str, self.value))
