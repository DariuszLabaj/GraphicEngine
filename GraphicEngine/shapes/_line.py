from __future__ import annotations
import pygame
from math import ceil


def Line(
    display: pygame.Surface,
    startPos: pygame._common._Coordinate,
    endPos: pygame._common._Coordinate,
    color: pygame._common._ColorValue,
    width: int = 1,
):
    def getVector2d(
        startPos: pygame._common._Coordinate, endPos: pygame._common._Coordinate
    ):
        if isinstance(startPos, tuple) and len(startPos) >= 2:
            v1 = pygame.Vector2(startPos[0], startPos[1])
        elif isinstance(startPos, pygame.Vector2):
            v1 = startPos
        else:
            v1 = pygame.Vector2(0, 0)
        if isinstance(endPos, tuple) and len(startPos) >= 2:
            v2 = pygame.Vector2(endPos[0], endPos[1])
        elif isinstance(endPos, pygame.Vector2):
            v2 = endPos
        else:
            v2 = pygame.Vector2(0, 0)
        return v1, v2

    start, end = getVector2d(startPos, endPos)
    rectWidth = ceil(abs(start.x - end.x))
    rectHeight = ceil(abs(start.y - end.y))
    if rectWidth == 0:
        rectWidth = 1
    if rectHeight == 0:
        rectHeight = 1
    surface = pygame.Surface((rectWidth, rectHeight), pygame.SRCALPHA)
    pygame.draw.line(surface, color, (0, 0), (surface.get_rect().size), width)
    display.blit(surface, start)
