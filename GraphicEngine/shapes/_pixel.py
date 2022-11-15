from __future__ import annotations
from typing import Sequence
import GraphicEngine._common as _common
import pygame


def Pixel(
    display: pygame.Surface,
    color: _common.ColorValue,
    pos: Sequence[int],
):
    display.set_at(pos, color)
