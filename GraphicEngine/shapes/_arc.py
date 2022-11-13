from __future__ import annotations
import pygame


def Arc(
    display: pygame.Surface,
    rect: pygame.Rect,
    color: pygame._common._ColorValue,
    startAngle: float,
    stopAngle: float,
    width: int = 1,
):
    surface = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.arc(surface, color, surface.get_rect(), startAngle, stopAngle, width)
    display.blit(surface, rect)
