from tcgen.utils.constants import LOWERCASE
from tcgen.utils import random, InvalidRangeException
import sympy
import logging
import typing

__all__ = [
    'Primitive',
    'Integer',
    'Bool',
    'Float',
    'Char',
    'Prime',
]


class InclusiveMixin:

    def inclusive(self):
        self._inclusive = True
        return self

    def exclusive(self):
        self._inclusive = False
        return self


class SortableMixin:

    def _total_values(self):
        '''Returns the number of possible values it can generate'''
        raise NotImplementedError

    def _kth_smallest(self, k):
        '''
        Returns the kth smallest value it can generate
        1 <= k <= self._total_values()
        '''
        raise NotImplementedError


class ArithmeticMixin:

    def __add__(self, val):
        if self.is_generated:
            return self.value + val
        self.L += val
        self.U += val
        return self

    __radd__ = __add__

    def __sub__(self, val):
        if self.is_generated:
            return self.value - val
        self.L -= val
        self.U -= val
        return self

    __rsub__ = __sub__

    def __mul__(self, val):
        if self.is_generated:
            return self.value * val
        self.L *= val
        self.U *= val
        return self

    __rmul__ = __mul__

    def __floordiv__(self, val):
        if self.is_generated:
            return self.value / val
        self.L //= val
        self.U //= val
        return self

    __truediv__ = __floordiv__


class Primitive:
    L = None
    U = None
    _inclusive = None

    def __init__(
        self,
        weighted: bool = False,
        wcnt: int = None,
        **kwargs
    ):
        if kwargs:
            logging.warning('Recieved extra kwargs: ' + str(kwargs))

        if self.L and self.U:
            if self._inclusive is not None:
                if self._inclusive and self.L > self.U:
                    raise InvalidRangeException
                if not self._inclusive and self.L + 1 > self.U - 1:
                    raise InvalidRangeException
        if wcnt:
            self.weighted = True
        else:
            self.weighted = weighted
        self.value = None
        self.wcnt = wcnt

    @property
    def is_generated(self):
        return self.value is not None

    def _generate_value(self, **kwargs):
        raise NotImplementedError

    def _generate_weighted_value(self, **kwargs):
        raise NotImplementedError

    def val(self):
        raise NotImplementedError

    def default(self):
        raise NotImplementedError

    def _generate(self):
        kwargs = {}
        if self._inclusive is not None:
            kwargs['inclusive'] = self._inclusive

        if self.weighted:
            logging.debug('Generating weighted value')
            if self.wcnt:
                kwargs['wcnt'] = self.wcnt
            self._generate_weighted_value(**kwargs)
        else:
            logging.debug('Generating value')
            self._generate_value(**kwargs)
        return self.value

    def __str__(self):
        if not self.is_generated:
            self._generate()
        return str(self.value)


class Integer(Primitive, InclusiveMixin, ArithmeticMixin, SortableMixin):
    def __init__(
        self,
        *args: int,
        L: int = 1,
        U: int = 1e5,
        inclusive: bool = True,
        **kwargs,
    ):
        if len(args) == 1:
            U = args[0]
        elif len(args) == 2:
            L, U = args
        elif len(args) > 2:
            raise TypeError

        self.L = int(L)
        self.U = int(U)
        self._inclusive = inclusive
        Primitive.__init__(self, **kwargs)

    def _generate_weighted_value(self, **kwargs):
        self.value = random.wrandint(self.L, self.U, **kwargs)

    def _generate_value(self, **kwargs):
        self.value = random.randint(self.L, self.U, **kwargs)

    def _total_values(self):
        if self._inclusive:
            return self.U - self.L + 1
        return self.U - self.L - 1

    def _kth_smallest(self, k: int):
        if k < 1 or k > self._total_values():
            raise IndexError("k outside of bounds")
        if self._inclusive:
            return self.L + k - 1
        return self.L + k

    def default(self):
        return 0

    def val(self):
        self.__str__()
        return self.value

    __int__ = int = val


# class Integers():
#     def __init__(num: int = 0, bounds: list[Union[int, Tuple[int, int]]] = [], *args, **kwargs):
#         '''
#         Generate N numbers

#         Args:
#             num: The number of integers to generate


#         Examples:
#             Integers(4)
#             Integers(4, OE5)
#             Integers([OE5, (50, 100), OE7])
#             Integers(4, U=OE4)
#             Integers(4, 0, OE5)
#             Integers(4, L=0, U=OE5)
#         '''
#         if num < 1 and len(bounds == 0):
#             raise Exception('Number of must be greater than or equal to one.')

#         if len(bounds) != num and len(bounds) != 0:
#             raise Exception('Len of the bounds array does not equal number of integers')

#         if len(bounds) == 0 and 'U' in kwargs:


#         return [Integer(*args, **kwargs) for _ in range(num)]


class Prime(Integer):
    def __init__(self, *args, **kwargs):
        Integer.__init__(self, *args, **kwargs)
        # To raise error
        random.randprime(self.L, self.U)

    def _generate_weighted_value(self, **kwargs):
        self.value = random.wrandprime(self.L, self.U, **kwargs)

    def _generate_value(self, **kwargs):
        self.value = random.randprime(self.L, self.U, **kwargs)

    def _total_values(self):
        '''
        Get number of primes between range

        !! Slow function !!
        '''
        if self._inclusive:
            return len(list(sympy.primerange(self.L, self.U + 1)))
        return len(list(sympy.primerange(self.L + 1, self.U)))

    def _kth_smallest(self, k: int):
        if k < 1 or k > self._total_values():
            raise IndexError("k outside of bounds")
        # TODO: take advantage of generator to reduce from all primes generated, only the first k primes
        if self._inclusive:
            return list(sympy.primerange(self.L, self.U + 1))[k - 1]
        return list(sympy.primerange(self.L + 1, self.U))[k - 1]

    def val(self):
        return super().val()

    prime = val


class Bool(Integer):
    def __init__(self, **kwargs):
        Integer.__init__(self, 0, 1, **kwargs)

    def bool(self):
        return self.val()


# class Bools():
#     def __init__(num: int, *args, **kwargs):
#         if num < 1:
#             raise Exception('Number of must be greater than or equal to one.')
#         return [Bool(*args, **kwargs) for _ in range(num)]


class Float(Primitive, InclusiveMixin, ArithmeticMixin, SortableMixin):
    def __init__(
        self,
        *args: float,
        L: float = 1,
        U: float = 1e5,
        places: int = 2,
        inclusive: bool = True,
        **kwargs
    ):
        if len(args) == 1:
            U = args[0]
        elif len(args) == 2:
            L, U = args
        elif len(args) > 2:
            raise TypeError

        self.L = L
        self.U = U
        self.places = places
        self._inclusive = inclusive
        Primitive.__init__(self, **kwargs)

    def _generate_weighted_value(self, **kwargs):
        self.value = random.wrandfloat(self.L, self.U, places=self.places, **kwargs)

    def _generate_value(self, **kwargs):
        self.value = random.randfloat(self.L, self.U, places=self.places, **kwargs)

    def _total_values(self):
        L_i = int(self.L * 10**self.places)
        U_i = int(self.U * 10**self.places)
        if self._inclusive:
            return U_i - L_i + 1
        return U_i - L_i - 1

    def _kth_smallest(self, k):
        if k < 1 or k > self._total_values():
            raise IndexError("k outside of bounds")
        L_i = int(self.L * 10**self.places)
        if self._inclusive:
            return (L_i + k - 1) / (10**self.places)
        return (L_i + k) / (10**self.places)

    def __str__(self):
        super().__str__()
        fmt = '{:.' + str(self.places) + 'f}'
        return fmt.format(self.value)

    def val(self):
        self.__str__()
        return self.value

    def round(self, val=None):
        self.__str__()
        return round(self.value, val)

    __round__ = round

    def __int__(self):
        return int(self.val())

    __float__ = float = val


class Char(Primitive):
    def __init__(self, char_set: str = LOWERCASE, priority: typing.List[int] = [], **kwargs):
        '''
        Args:
            char_set: A string which the character will use
                If weighted and wcnt > 0, the left most characters in the string are favoured more than the right
                If weighted and wcnt > 0, the right most characters in the string are favoured more than the left
            priority: A list which states the priority of each character in char_set
                The array must be a permutation of [1 ... len(char_set)]
        '''
        if 'weighted' in kwargs and kwargs['weighted']:
            if len(priority) != len(char_set) and len(priority):
                raise TypeError('The array must be a permutation of [1 ... len(char_set)]')

            if len(priority) and sorted(priority) != list(range(1, len(char_set) + 1)):
                raise TypeError('The array must be a permutation of [1 ... len(char_set)]')
        elif len(priority):
            logging.warning('Not weighted, but priority arg still is passed')

        if len(char_set) == 0:
            raise TypeError

        if len(char_set) == 1:
            logging.warning('Len or character set is 1')

        if 'inclusive' in kwargs:
            raise TypeError

        self.char_set = char_set
        if len(priority):
            self.priority = [0] * (len(char_set))
            for k, v in enumerate(priority):
                self.priority[v - 1] = k + 1
        else:
            self.priority = list(range(1, len(char_set) + 1))

        Primitive.__init__(self, **kwargs)

    def _generate_weighted_value(self, **kwargs):
        self.value = random.wchoice(self.char_set, self.priority, **kwargs)

    def _generate_value(self, **kwargs):
        self.value = random.choice(self.char_set, **kwargs)

    def default(self):
        return self.char_set[0]

    def val(self):
        self.__str__()
        return self.value

    char = val
