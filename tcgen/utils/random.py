import random as random_pkg
import sympy
import logging
import typing
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
    def noise(L: int, U: int, data: typing.List[int], inclusive: bool = True) -> typing.List[int]:
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
        L_i = int(L * 10**places)
        U_i = int(U * 10**places)
        if not inclusive:
            L_i += 1
            U_i -= 1
        if L_i > U_i:
            raise InvalidRangeException
        if L_i == U_i:
            logging.warning(f"The bounds {L} and {U} can only generated one value")
        return random_pkg.randint(L_i, U_i) / 10**places

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

    @staticmethod
    def choice(char_set: str) -> str:
        '''
        Returns a random character in string

        Args:
            char_set: Character set to choose string from

        Returns:
            A random character

        Raises:
            TypeError: where char_set is empty
        '''
        if len(char_set) == 0:
            raise TypeError
        idx = random.randint(1, len(char_set))
        return char_set[idx - 1]

    @staticmethod
    def wchoice(char_set: str, priority: typing.List[int], wcnt: int = 5):
        '''
        Returns a weighted random character in string

        Args:
            char_set: Character set to choose string from
            priority: Priority of each character in char_set
            wcnt: weighted count.
                if wcnt > 0, it returns the max of wcnt random floats
                if wcnt < 0, it returns the min of abs(wcnt) random floats

        Returns:
            A weighted random character

        Raises:
            TypeError: where char_set is empty
        '''
        if len(char_set) == 0:
            raise TypeError
        if len(char_set) != len(priority):
            raise TypeError

        ret = random.randint(1, len(char_set))
        for _ in range(abs(wcnt)):
            if wcnt > 0:
                ret = max(ret, random.randint(1, len(char_set)))
            if wcnt < 0:
                ret = min(ret, random.randint(1, len(char_set)))
        return char_set[priority[len(char_set) - ret] - 1]

    @staticmethod
    def randprime(L: int, U: int, inclusive: bool = True) -> int:
        '''
        Returns a random prime

        Args:
            L: Lower bound
            U: Upper bound
            inclusive: whether the bounds are inclusive

        Returns:
            A random prime

        Raises:
            InvalidRangeException: where L > U
            ValueError: prime does not exist in range
        '''
        if not inclusive:
            L += 1
            U -= 1
        if L > U:
            raise InvalidRangeException
        if L == U:
            logging.warning(f"The bounds {L} and {U} are the same, only one "
                            "value can be generated")
        # randprime is [a, b)
        return sympy.randprime(L, U + 1)

    @staticmethod
    def wrandprime(L: int, U: int, wcnt: int = 5, inclusive: bool = True) -> int:
        '''
        Returns a weighted random prime

        Args:
            L: Lower bound
            R: Upper bound
            wcnt: weighted count.
                if wcnt > 0, it returns the max of wcnt random primes
                if wcnt < 0, it returns the min of abs(wcnt) random primes
            inclusive: whether the bounds are inclusive

        Returns:
            A weighted random prime

        Raises:
            InvalidRangeException: where L > U
            ValueError: prime does not exist in range
        '''
        # The way cf testlib does it is a bit different.
        # https://github.com/MikeMirzayanov/testlib/blob/master/testlib.h#L787
        ret = random.randprime(L, U, inclusive)
        for _ in range(abs(wcnt)):
            if wcnt > 0:
                ret = max(ret, random.randprime(L, U, inclusive))
            if wcnt < 0:
                ret = min(ret, random.randprime(L, U, inclusive))
        return ret

    @staticmethod
    def shuffle(arr: list) -> list:
        '''
        Randomly shuffles a list

        Args:
            arr: list to shuffle

        Returns:
            Shuffled list
        '''

        random_pkg.shuffle(arr)
        return arr
