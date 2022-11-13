from typing import Literal
import functools
import warnings

_Direction = Literal[-1, 0, 1]


def deprecate(msg, klass=PendingDeprecationWarning):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(msg, klass, stacklevel=2)
            return func(*args, **kwargs)

        return wrapper

    return decorator
