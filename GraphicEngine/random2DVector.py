from math import pi
from typing import Optional, overload


import pygame
import random

from GraphicEngine.mathMap import mathMap


@overload
def random2DVector() -> pygame.Vector2:
    ...


@overload
def random2DVector(x1: float, y1: float) -> pygame.Vector2:
    ...


def random2DVector(
    x1: Optional[float] = None, y1: Optional[float] = None, x2: Optional[float] = None, y2: Optional[float] = None
) -> pygame.Vector2:
    if x1 is None and x2 is None and y1 is None and y2 is None:
        vect = pygame.Vector2(1, 0)
        vect.rotate_rad_ip(random.random() * 2 * pi)
        return vect
    elif x2 is None and y2 is None:
        a = 0
        b = x1
        c = 0
        d = y1
    elif x1 is not None and x2 is not None and y1 is not None and y2 is not None:
        a = x1
        b = y1
        c = x2
        d = y2
    else:
        raise ValueError()
    if b is None or d is None:
        raise ValueError()
    rng = random.Random()
    return pygame.Vector2(
        mathMap(rng.random(), 0, 1, a, b), mathMap(rng.random(), 0, 1, c, d)
    )
