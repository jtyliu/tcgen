import random as random_pkg
import logging
# This is meant to be a wrapper to allow
# weighted randoms
# noise


class InvalidRangeException(Exception):
    '''The bounds for the range is impossible'''
    pass


class random():

    @staticmethod
    def seed(seed: int) -> None:
        random_pkg.seed(seed)

    @staticmethod
    def randint(L: int, U: int, inclusive: bool = True) -> int:
        '''
        Returns a random integer

        Args:
            L: Lower bound
            U: Upper bound
            inclusive: whether the bounds are inclusive

        Returns:
            A random integer

        Raises:
            InvalidRangeException: where L > U
        '''
        if not inclusive:
            L += 1
            U -= 1
        if L > U:
            raise InvalidRangeException
        if L == U:
            logging.warning(f"The bounds {L} and {U} are the same, only one "
                            "value can be generated")
        return random_pkg.randint(L, U)

    @staticmethod
    def wrandint(L: int, U: int, wcnt: int = 5, inclusive: bool = True) -> int:
        '''
        Returns a weighted random integer

        Args:
            L: Lower bound
            R: Upper bound
            wcnt: weighted count.
                if wcnt > 0, it returns the max of wcnt random integers
                if wcnt < 0, it returns the min of abs(wcnt) random integers
            inclusive: whether the bounds are inclusive

        Returns:
            A weighted random

        Raises:
            InvalidRangeException: where L > U
        '''
        # The way cf testlib does it is a bit different.
        # https://github.com/MikeMirzayanov/testlib/blob/master/testlib.h#L787
        ret = random.randint(L, U, inclusive)
        for _ in range(abs(wcnt)):
            if wcnt > 0:
                ret = max(ret, random.randint(L, U, inclusive))
            if wcnt < 0:
                ret = min(ret, random.randint(L, U, inclusive))
        return ret

    @staticmethod
    def noise(L: int, U: int, data: list[int], inclusive: bool = True) -> list[int]:
        '''
        Returns data added with noise

        Args:
            L: Lower bound
            U: Upper bound
            data: data to add noise to.

        Returns:
            The original data + random noise

        Raises:
            InvalidRangeException: where L > U
        '''
        # Not sure if this should be inclusive or not
        return [data[i] + random.randint(L, U, inclusive) for i in range(len(data))]

    @staticmethod
    def randfloat(L: float, U: float, places: int, inclusive: bool = True) -> float:
        '''
        Returns a random float

        Args:
            L: Lower bound
            U: Upper bound
            inclusive: whether the bounds are inclusive
            places: rounded decimal places

        Returns:
            A random float

        Raises:
            InvalidRangeException: where L > U
        '''
        L_i = int(L*10**places)
        U_i = int(U*10**places)
        if not inclusive:
            L_i += 1
            U_i -= 1
        if L_i > U_i:
            raise InvalidRangeException
        if L_i == U_i:
            logging.warning(f"The bounds {L} and {U} can only generated one value")
        return random_pkg.randint(L_i, U_i)/10**places

    @staticmethod
    def wrandfloat(L: float, U: float, places: int, wcnt: int = 5, inclusive: bool = True) -> float:
        '''
        Returns a weighted random float

        Args:
            L: Lower bound
            R: Upper bound
            wcnt: weighted count.
                if wcnt > 0, it returns the max of wcnt random floats
                if wcnt < 0, it returns the min of abs(wcnt) random floats
            inclusive: whether the bounds are inclusive
            places: rounded decimal places

        Returns:
            A weighted random

        Raises:
            InvalidRangeException: where L > U
        '''
        ret = random.randfloat(L, U, places, inclusive)
        for _ in range(abs(wcnt)):
            if wcnt > 0:
                ret = max(ret, random.randfloat(L, U, places, inclusive))
            if wcnt < 0:
                ret = min(ret, random.randfloat(L, U, places, inclusive))
        return ret
