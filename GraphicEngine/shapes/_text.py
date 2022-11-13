from __future__ import annotations
import pygame


def Text(
    display: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    color: pygame._common._ColorValue,
    position: pygame._common._Coordinate = (20, 20),
    allowedWidth: int = None,
):
    if allowedWidth is None:
        allowedWidth = display.get_width() - position[0] - 10
    words = text.split()
    lines = []
    while len(words) > 0:
        line_words = []
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
            font.render(line, True, color), (textX, textY)
        )
        y_offset += fontHeight
    return position[1] + y_offset
