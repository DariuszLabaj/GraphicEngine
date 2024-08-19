from __future__ import annotations

from typing import Tuple

from pygame.color import Color

import GraphicEngine._common as _common


class InvalidHexValue(Exception):
    ...


class UnsuportedLenght(Exception):
    ...


class InvalidColorFormat(Exception):
    ...


class IncorrectSubType(Exception):
    ...


def getColor_Int(
    value: _common.ColorValue, alpha: bool = True
) -> Tuple[int, int, int, int] | Tuple[int, int, int]:
    ret = (0, 0, 0, 0)
    if isinstance(value, Color):
        ret = (value.r, value.g, value.b, value.a)
    elif isinstance(value, int):
        ret = (value, value, value, 0)
    elif isinstance(value, str):
        if value.startswith("#") and len(value) == 7:
            r = int(value[1:3], base=16)
            g = int(value[3:5], base=16)
            b = int(value[5:], base=16)
            if -1 < r < 256 and -1 < g < 256 and -1 < b < 256:
                ret = (r, g, b, 0)
            else:
                raise InvalidHexValue()
        else:
            raise InvalidHexValue()
    elif isinstance(value, tuple) or isinstance(value, list):  # type: ignore
        for var in value:
            if not (isinstance(var, float) or isinstance(var, int)):  # type: ignore
                raise IncorrectSubType(
                    f"Incorrect sub type, should be int or float but is {type(var)}"
                )
        match len(value):  # type: ignore
            case 1:
                r = value[0]
                if -1 < r < 256:
                    ret = (r, r, r, 0)
                else:
                    raise InvalidHexValue()
            case 2:
                r = value[0]
                a = value[1]
                if -1 < r < 256 and -1 < a < 256:
                    ret = (r, r, r, a)
            case 3:
                r = value[0]
                g = value[1]
                b = value[2]  # type: ignore
                if -1 < r < 256 and -1 < g < 256 and -1 < b < 256:
                    ret = (r, g, b, 0)
                else:
                    raise InvalidHexValue()
            case 4:
                r = value[0]
                g = value[1]
                b = value[2]  # type: ignore
                a = value[3]  # type: ignore
                if -1 < r < 256 and -1 < g < 256 and -1 < b < 256 and -1 < a < 256:
                    ret = (r, g, b, a)
                else:
                    raise InvalidHexValue()
                ret = (r, g, b, a)
    else:
        raise InvalidColorFormat()
    if alpha:
        return (int(ret[0]), int(ret[1]), int(ret[2]), int(ret[3]))
    else:
        return (int(ret[0]), int(ret[1]), int(ret[2]))


def getColor_float(value: _common.ColorValue, alpha: bool = True):
    intVal = getColor_Int(value, alpha)
    if alpha:
        return (intVal[0] / 255, intVal[1] / 255, intVal[2] / 255, intVal[3] / 255)  # type: ignore
    else:
        return (intVal[0] / 255, intVal[1] / 255, intVal[2] / 255)
