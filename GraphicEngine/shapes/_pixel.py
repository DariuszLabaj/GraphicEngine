from __future__ import annotations
from typing import Sequence
import GraphicEngine._common as _common
import pygame


def Pixel(
    display: pygame.Surface | pygame.surface.Surface,
    color: _common.ColorValue,
    pos: Sequence[int],
):
    if not(isinstance(color, tuple) and len(color) == 2):
        display.set_at(pos, color)
