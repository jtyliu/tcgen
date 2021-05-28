from utils import random, InvalidRangeException
import logging

__all__ = [
    'Primitive',
    'Integer',
    'Bool',
    'Float',
]


class InclusiveMixin:

    def inclusive(self):
        self._inclusive = True
        return self

    def exclusive(self):
        self._inclusive = False
        return self


class Primitive:
    L = None
    U = None
    _inclusive = False

    def __init__(
        self,
        weighted: bool = False,
        wcnt: int = None,
        **kwargs
    ):
        if kwargs:
            logging.info('Recieved extra kwargs: '+kwargs)

        if self.L and self.U:
            if self._inclusive and self.L > self.U:
                raise InvalidRangeException
            if not self._inclusive and self.L + 1 > self.U - 1:
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

    def val(self):
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


class Integer(Primitive, InclusiveMixin):
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

    def _generate_weighted_value(self):
        kwargs = {}
        if self.wcnt:
            kwargs['wcnt'] = self.wcnt
        if self._inclusive is not None:
            kwargs['inclusive'] = self._inclusive
        self.value = random.wrandint(self.L, self.U, **kwargs)

    def _generate_value(self):
        kwargs = {}
        if self._inclusive is not None:
            kwargs['inclusive'] = self._inclusive
        self.value = random.randint(self.L, self.U, **kwargs)

    def val(self):
        self.__str__()
        return self.value

    int = val


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
        return self.val()


# class Bools():
#     def __init__(num: int, *args, **kwargs):
#         if num < 1:
#             raise Exception('Number of must be greater than or equal to one.')
#         return [Bool(*args, **kwargs) for _ in range(num)]


class Float(Primitive):
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
        elif len(args) == 3:
            L, U, places = args
        elif len(args) > 3:
            raise TypeError

        self.L = L
        self.U = U
        self.places = places
        self.inclusive = inclusive
        Primitive.__init__(self, **kwargs)

    def val(self):
        self.__str__()
        return self.value

    float = val
