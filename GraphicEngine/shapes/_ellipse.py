from __future__ import annotations
import GraphicEngine._common as _common
import pygame


def Ellipse(
    display: pygame.Surface, rect: pygame.Rect, color: _common.ColorValue, width: int = 0
):
    surface = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.ellipse(
        surface, color, pygame.Rect(0, 0, rect.size[0], rect.size[1]), width
    )
    display.blit(surface, rect)
