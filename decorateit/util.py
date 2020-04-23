#!/usr/bin/python
"""
"""


# imported as __pc to prevent it from appearing in 'dir()'
from time import perf_counter as __pc
import functools
import logging


# 'dict' that stores all plugins
# see 'util.register()' for more details.
plugins = dict()


def timer(_func=None, *, times: int = 1):
    """
    Decorator that times how much it takes to run a function.

        Parameters:
            _func:
                function to be used for timing.

            times: int
                number of times to run a '_func' function, by default 1.

        Returns:
            wrapped return value of '_func'

        Usage example:

            >>> from decorateit.util import timer
            >>>
            >>> @timer(times=5)
            ... def sqrt(n):
            ...     return n ** 0.5
            ...
            >>> sqrt(64)
            DEBUG:root:'sqrt' has been called 5 times. Average executing time is 1.4200000805431046e-06 seconds.
            8.0
    """
    def inner(func):
        func.count, func.total = 0, 0
        func.avg = None

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                t1 = __pc()
                val = func(*args, **kwargs)
                res = __pc() - t1
                func.count += 1
                func.total += res

            if func.count == times:
                func.avg = func.total / func.count
                logging.basicConfig(level=logging.DEBUG)
                logging.debug(
                    f"{func.__name__!r} has been called {func.count} times. " +
                    f"Average executing time is {func.avg} seconds."
                )
                logging.basicConfig(level=logging.WARNING)
            return val
        return wrapper

    if _func is None:
        return inner
    else:
        return inner(_func)


def count_calls(func):
    """
    Decorator that keeps track of how much times a function is called.

        Parameters:
            func:
                function to be used for counting

        Attributes:
            func.num_of_calls: number of times function has been called.

        Returns:
            wrapped return value of 'func'

        Usage example:

            >>> from decorateit.util import count_calls
            >>>
            >>> @count_calls
            ... def fib(n):
            ...     if n < 2:
            ...         return n
            ...     else:
            ...         return fib(n - 2) + fib(n - 1)
            ...
            >>> fib(6)
            DEBUG:root:'fib' called 1 time(s).
            DEBUG:root:'fib' called 2 time(s).
            DEBUG:root:'fib' called 3 time(s).
            DEBUG:root:'fib' called 4 time(s).
            DEBUG:root:'fib' called 5 time(s).
            2
            >>> fib.num_of_calls
            5
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        val = func(*args, **kwargs)
        wrapper.num_of_calls += 1
        logging.basicConfig(level=logging.DEBUG)
        logging.debug(
            f"{func.__name__!r} called {wrapper.num_of_calls} time(s). "
        )
        logging.basicConfig(level=logging.WARNING)
        return val

    wrapper.num_of_calls = 0
    return wrapper


def register(func):
    """
    Decorator that registers and stores given function as plugin in 'util.plugins'
    dictionary. Function name as a key and function itself as a value.

        Parameters:
            func:
                function to be used for registering

        Returns:
            return value of the given 'func'

        Usage example:

            >>> from decorateit.util import register
            >>>
            >>> @register
            ... def fib(n):
            ...     if n < 2:
            ...         return n
            ...     else:
            ...         return fib(n - 2) + fib(n - 1)
            ...
            >>>
            >>> @register
            ... def insert_sort(lst):
            ...     for i in range(1, len(lst)):
            ...         unsort = lst[i]
            ...         ins_idx = i
            ...
            ...         while ins_idx > 0 and unsort < lst[ins_idx - 1]:
            ...             lst[ins_idx] = lst[ins_idx - 1]
            ...             ins_idx -= 1
            ...
            ...         lst[ins_idx] = unsort
            ...
            ...     return lst
            ...
            >>> fib(4)
            3
            >>> insert_sort([5, 9, 2, 3, -4, 11])
            [-4, 2, 3, 5, 9, 11]
            >>> print(util.plugins)
            {'fib': <function fib at 0x0000024FE5020678>, 'insert_sort': <function insert_sort at 0x0000024FE505E708>}
    """
    plugins[func.__name__] = func
    return func


def memorise(func):
    """
    Decorator that "memorises" the return value of the given function as a 'dict' value
    and takes its arguments and keyword arguments as a key. Usualy used with recursive functions.

        Parameters:
            func:
                function to be used for "memorising"

        Returns:
            wrapped return value of 'func'

        Usage example:

            >>> from decorateit.util import count_calls, memorise
            >>>
            >>> @memorise
            ... @count_calls
            ... def fib(n):
            ...     if n < 2:
            ...         return n
            ...     else:
            ...         return fib(n - 2) + fib(n - 1)
            ...
            >>> fib(14)
            DEBUG:root:'fib' called 1 time(s).
            DEBUG:root:'fib' called 2 time(s).
            DEBUG:root:'fib' called 3 time(s).
            DEBUG:root:'fib' called 4 time(s).
            DEBUG:root:'fib' called 5 time(s).
            DEBUG:root:'fib' called 6 time(s).
            DEBUG:root:'fib' called 7 time(s).
            DEBUG:root:'fib' called 8 time(s).
            DEBUG:root:'fib' called 9 time(s).
            DEBUG:root:'fib' called 10 time(s).
            DEBUG:root:'fib' called 11 time(s).
            DEBUG:root:'fib' called 12 time(s).
            DEBUG:root:'fib' called 13 time(s).
            DEBUG:root:'fib' called 14 time(s).
            DEBUG:root:'fib' called 15 time(s).
            377
            >>> fib(8)
            21
            >>> # note that there haven't been made any calculations
            >>> # to get the 8th fibonacci number, because it has
            >>> # already been done when running fib(14).
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = args + tuple(kwargs.items())
        if key not in func.memorised__:
            func.memorised__[key] = func(*args, **kwargs)
        return func.memorised__[key]

    func.memorised__ = {}
    return wrapper


def debug(func):
    """
    Decorator that debugs the given function by keeping track
    of each call, all passed in and returned values.

        Parameters:
            func:
                function to be used for debugging

        Returns:
            wrapped return value of 'func'

        Usage example:

            >>> from decorateit.util import debug
            >>>
            >>> @debug
            ... def fib(n):
            ...     if n < 2:
            ...         return n
            ...     else:
            ...         return fib(n - 2) + fib(n - 1)
            ...
            >>> fib(3)
            DEBUG:root:1 has been passed in 'fib' and returned '1'
            DEBUG:root:0 has been passed in 'fib' and returned '0'
            DEBUG:root:1 has been passed in 'fib' and returned '1'
            DEBUG:root:2 has been passed in 'fib' and returned '1'
            DEBUG:root:3 has been passed in 'fib' and returned '2'
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        _arg = [(repr(arg), arg)[isinstance(arg, str)] for arg in args]
        _kwarg = [f"{key}: {val!r}" for key, val in kwargs.items()]
        total = ', '.join(_arg + _kwarg)
        val = func(*args, **kwargs)

        logging.basicConfig(level=logging.DEBUG)
        logging.debug(
            f"{str(total)} has been passed in {str(func.__name__)!r} " +
            f"and returned {str(val)!r}"
        )
        logging.basicConfig(level=logging.WARNING)

        return val
    return wrapper
