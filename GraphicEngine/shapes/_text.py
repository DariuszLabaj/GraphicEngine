from __future__ import annotations
import math
from typing import Optional
import pygame
from GraphicEngine._processColor import getColor_Int
import GraphicEngine._common as _common


def Text(
    display: pygame.Surface | pygame.surface.Surface,
    font: pygame.font.Font,
    text: str,
    color: _common.ColorValue,
    position: _common.Coordinate = (20, 20),
    allowedWidth: Optional[int] = None,
):
    if allowedWidth is None:
        allowedWidth = math.floor(display.get_width() - position[0] - 10)
    words = text.split()
    lines: list[str] = []
    while len(words) > 0:
        line_words: list[str] = []
        while len(words) > 0:
            line_words.append(words.pop(0))
            fontWidth, _ = font.size(" ".join(line_words + words[:1]))
            if fontWidth > allowedWidth:
                break
        lines.append(" ".join(line_words))
    y_offset = 0
    for line in lines:
        fontWidth, fontHeight = font.size(line)
        textX = position[0]  # - fontWidth/2 Center
        textY = position[1] + y_offset
        display.blit(
            font.render(line, True, getColor_Int(color)), (textX, textY)
        )
        y_offset += fontHeight
    return position[1] + y_offset
