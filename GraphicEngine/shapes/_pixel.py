from __future__ import annotations
import pygame


def Pixel(
    display: pygame.Surface,
    color: pygame._common._ColorValue,
    pos: pygame._common._Coordinate,
):
    display.set_at(pos, color)
