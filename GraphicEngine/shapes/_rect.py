from __future__ import annotations
import pygame


def Rect(
    display: pygame.Surface,
    rect: pygame.Rect,
    color: pygame._common._ColorValue,
    width: int = 0,
    borderRadius: int = -1,
    borderTopLeftRadius: int = -1,
    borderTopRightRadius: int = -1,
    borderBottomLeftRadius: int = -1,
    borderBottmRightRadius: int = -1,
):
    surface = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(
        surface,
        color,
        pygame.Rect(0, 0, rect.width, rect.height),
        width,
        borderRadius,
        borderTopLeftRadius,
        borderTopRightRadius,
        borderBottomLeftRadius,
        borderBottmRightRadius,
    )
    display.blit(surface, rect)
