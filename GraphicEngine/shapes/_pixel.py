from __future__ import annotations
from GraphicEngine._processColor import getColor_Int
from GraphicEngine.constrain import constrain
import pygame


def Pixel(
    display: pygame.Surface,
    color: pygame._common._ColorValue | float,
    pos: pygame._common._Coordinate,
):
    if isinstance(color, float):
        constcolor = constrain(color, 0, 255)
        display.set_at(pos, getColor_Int(constcolor))
    else:
        display.set_at(pos, getColor_Int(color))
