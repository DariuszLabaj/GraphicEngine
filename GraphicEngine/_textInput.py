from __future__ import annotations
from functools import cached_property
from typing import Literal
import pygame


class _TextInput:
    @property
    def __textChanged(self) -> bool:
        if self.__lastTest != self.__text:
            self.__lastTest = self.__text[:]
            return True
        else:
            return False

    @cached_property
    def __txtRect(self) -> pygame._common._RectValue:
        return pygame.Rect(0, 0, self.__rect.width, self.__rect.height)

    def __init__(
        self,
        surface: pygame.Surface,
        rect: pygame.Rect,
        text: str,
        background: pygame._common._ColorValue = (255, 255, 255),
        foreground: pygame._common._ColorValue = (0, 0, 0),
        justify: Literal["LEFT"] | Literal["CENTER"] | Literal["RIGHT"] = "CENTER",
        font: pygame.font.Font = None,
        padx: int = 0,
        pady: int = 0,
    ):
        self.__surface = surface
        self.__rect = rect
        self.__text = text
        self.__lastTest = text+'!'
        self.__background = background
        self.__foreground = foreground
        self.__justify = justify
        if font:
            self.__font = font
        else:
            self.__font = pygame.font.SysFont(None, 16)
        self.__padx = padx
        self.__pady = pady
        self.__drawSurf = pygame.Surface(self.__rect.size, pygame.SRCALPHA)

    def __prepareText(self):
        labelWidth, labelHeight = self.__font.size(self.__text)
        match self.__justify:
            case "RIGHT":
                textX = self.__txtRect.width - labelWidth + self.__padx
            case "CENTER":
                textX = self.__txtRect.centerx - labelWidth / 2 + self.__padx
            case _:
                textX = self.__padx
        textY = self.__txtRect.centery - labelHeight / 2 + self.__pady
        return self.__font.render(self.__text, True, self.__foreground), textX, textY

    def __createSurface(self):
        self.__drawSurf = pygame.Surface(self.__rect.size, pygame.SRCALPHA)

    def update(self, text: str):
        self.__text = text

    def show(self):
        if self.__textChanged:
            self.__createSurface()
            pygame.draw.rect(self.__drawSurf, self.__background, self.__txtRect)
            text, textX, textY = self.__prepareText()
            self.__drawSurf.blit(text, (textX, textY))
        self.__surface.blit(self.__drawSurf, self.__rect)
