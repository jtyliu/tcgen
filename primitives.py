from typing import Tuple, Union
from utils.constants import *
from utils import random, InvalidRangeException
import logging

__all__ = [
    'Primitive',
    'Integer',
    'Integers',
    'Bool',
    'Bools',
]


class Primitive:
    L = None
    U = None
    inclusive = False

    def __init__(
        self,
        weighted: bool = False,
        wcnt: int = None,
        **kwargs
    ):
        if kwargs:
            logging.info('Recieved extra kwargs: '+kwargs)

        if self.L and self.U:
            if self.inclusive and self.L > self.U:
                raise InvalidRangeException
            if not self.inclusive and self.L + 1 > self.U - 1:
                raise InvalidRangeException

        self.weighted = weighted
        self.value = None
        self.wcnt = wcnt

    @property
    def is_generated(self):
        return self.value is not None

    def _generate_value(self):
        raise NotImplementedError

    def _generate_weighted_value(self):
        raise NotImplementedError

    def __str__(self):
        if not self.is_generated:
            if self.weighted:
                logging.debug('Generating weighted value')
                self._generate_weighted_value()
            else:
                logging.debug('Generating value')
                self._generate_value()
        return str(self.value)


class Integer(Primitive):
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
            L = args[0]
            U = args[1]
        elif len(args) > 2:
            raise TypeError

        self.L = L
        self.U = U
        self.inclusive = inclusive
        Primitive.__init__(self, **kwargs)

    def _generate_weighted_value(self):
        kwargs = {}
        if self.wcnt:
            kwargs['wcnt'] = self.wcnt
        if self.inclusive:
            kwargs['inclusive'] = self.inclusive
        self.value = random.wrandint(self.L, self.U, **kwargs)

    def _generate_value(self):
        kwargs = {}
        if self.inclusive:
            kwargs['inclusive'] = self.inclusive
        self.value = random.randint(self.L, self.U, **kwargs)

    def inclusive(self):
        self.inclusive = True
        return self

    def exclusive(self):
        self.inclusive = False
        return self

    def int(self):
        self.__str__()
        return self.value


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


class Bool(Integer):
    def __init__(self, **kwargs):
        Integer.__init__(self, 0, 1, **kwargs)

    def bool(self):
        return self.int()


# class Bools():
#     def __init__(num: int, *args, **kwargs):
#         if num < 1:
#             raise Exception('Number of must be greater than or equal to one.')
#         return [Bool(*args, **kwargs) for _ in range(num)]


class Float(Primitive):
    def __init__(self, weighted: bool, wcnt: int, **kwargs):
        super().__init__(weighted=weighted, wcnt=wcnt, **kwargs)