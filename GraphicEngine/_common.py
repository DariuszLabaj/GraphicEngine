import functools
import warnings
from os import PathLike
from typing import IO, Any, Callable, List, Literal, Sequence, Tuple, Union, Protocol

from pygame.color import Color
from pygame.math import Vector2
from pygame.rect import Rect


def deprecate(msg: str, klass: Warning | None | type = PendingDeprecationWarning):
    def decorator(func: Callable[..., Any]):
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any):
            warnings.warn(message=msg, category=klass, stacklevel=2)  # type: ignore
            return func(*args, **kwargs)

        return wrapper

    return decorator


Direction = Literal[-1, 0, 1]


# For functions that take a file name
AnyPath = Union[str, bytes, PathLike[str], PathLike[bytes]]

# Most pygame functions that take a file argument should be able to handle
# a _FileArg type
FileArg = Union[AnyPath, IO[bytes], IO[str]]

Coordinate = Union[Tuple[float, float], Sequence[float], Vector2]

# This typehint is used when a function would return an RGBA tuble
RgbaOutput = Tuple[int, int, int, int]
ColorValue = Union[Color, int, str, Tuple[int, int, int], List[int], RgbaOutput]

CanBeRect = Union[
    Rect,
    Tuple[int, int, int, int],
    List[int],
    Tuple[Coordinate, Coordinate],
    List[Coordinate],
]


class HasRectAttribute(Protocol):
    rect: CanBeRect


RectValue = Union[CanBeRect, HasRectAttribute]
