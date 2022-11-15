from __future__ import annotations
import GraphicEngine._common as _common
import pygame


def Circle(
    display: pygame.Surface,
    center: _common.Coordinate,
    radius: float,
    color: _common.ColorValue,
    width: int = 0,
):
    def getVector2d(Pos: _common.Coordinate):
        if isinstance(Pos, tuple) and len(Pos) >= 2:
            v1 = pygame.Vector2(Pos[0], Pos[1])
        elif isinstance(Pos, pygame.Vector2):
            v1 = Pos
        else:
            v1 = pygame.Vector2(0, 0)
        return v1
    vect = getVector2d(center)
    surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(surface, color, (radius, radius), radius, width)
    display.blit(surface, (vect.x - radius, vect.y - radius))
