from __future__ import annotations

from enum import Enum, auto
from functools import cached_property
from typing import Callable, Literal, Optional

import pygame

import GraphicEngine._common as _common


class BaseButtonAbstract:
    __currentState: BaseButtonAbstract.State
    __lastState: BaseButtonAbstract.State

    class State(Enum):
        Normal = auto()
        Pressed = auto()
        Disabled = auto()

    @property
    def __stateChanged(self) -> bool:
        if self.__lastState != self.__currentState:
            self.__lastState = self.__currentState
            return True
        else:
            return False

    @property
    def __color(self) -> _common.ColorValue:
        color = (0, 0, 0)
        match self.__currentState:
            case BaseButtonAbstract.State.Normal:
                color = self.__background
            case BaseButtonAbstract.State.Pressed:
                color = self.__activeBackground
            case BaseButtonAbstract.State.Disabled:
                color = (51, 51, 51)
        return color

    @property
    def __textColor(self) -> _common.ColorValue:
        color = (0, 0, 0)
        match self.__currentState:
            case BaseButtonAbstract.State.Normal:
                color = self.__foreground
            case BaseButtonAbstract.State.Pressed:
                color = self.__activeForeground
            case BaseButtonAbstract.State.Disabled:
                color = (180, 180, 180)
        return color

    @property
    def Center(self) -> _common.Coordinate:
        return self.__rect.center

    @property
    def __textCenter(self) -> _common.Coordinate:
        return self.__btnRect.center

    @cached_property
    def __btnRect(self) -> pygame.Rect:
        return pygame.Rect(0, 0, self.__rect.width, self.__rect.height)

    def __init__(
        self,
        surface: pygame.Surface,
        rect: pygame.Rect,
        command: Callable[[], None] | None = None,
        background: _common.ColorValue = (255, 255, 255),
        foreground: _common.ColorValue = (0, 0, 0),
        activeBackground: _common.ColorValue = (51, 51, 51),
        activeForeground: _common.ColorValue = (255, 255, 255),
        label: str = "Button",
        justify: Literal["LEFT"] | Literal["CENTER"] | Literal["RIGHT"] = "CENTER",
        font: Optional[pygame.font.Font] = None,
        padx: int = 0,
        pady: int = 0,
    ):
        self.__surface = surface
        self.__rect = rect
        self.__background = background
        self.__foreground = foreground
        self.__activeBackground = activeBackground
        self.__activeForeground = activeForeground
        self.__label = label
        self.__justify = justify
        if font:
            self.__font = font
        else:
            self.__font = pygame.font.SysFont('', 16)
        self.__padx = padx
        self.__pady = pady
        self.__command = command
        self.__radius = 5 if self.__rect.width > 10 and self.__rect.height > 10 else -1
        self.__currentState = BaseButtonAbstract.State.Normal
        self.__lastState = BaseButtonAbstract.State.Disabled
        self.__autoRelease = True
        self.__createButtonSurface()

    def __createButtonSurface(self):
        self.__btnSurface = pygame.Surface(self.__rect.size, pygame.SRCALPHA)

    def setButtonRadius(self, radius: int):
        self.__radius = radius

    def __prepareText(self):
        labelWidth, labelHeight = self.__font.size(self.__label)
        match self.__justify:
            case "RIGHT":
                textX = self.__btnRect.width - labelWidth + self.__padx
            case "CENTER":
                textX = self.__textCenter[0] - labelWidth / 2 + self.__padx
            case _:
                textX = self.__padx
        textY = self.__textCenter[1] - labelHeight / 2 + self.__pady
        return self.__font.render(self.__label, True, self.__textColor), textX, textY

    def update(self):
        if self.__currentState == self.__lastState == BaseButtonAbstract.State.Disabled:
            return
        mouseEvents = pygame.mouse.get_pressed()
        if (
            self.__command
            and mouseEvents[0]
            and self.__rect.collidepoint(pygame.mouse.get_pos())
        ):
            if self.__currentState != BaseButtonAbstract.State.Pressed:
                self.__currentState = BaseButtonAbstract.State.Pressed
                self.__command()
        elif (
            self.__autoRelease
            and self.__currentState
            == self.__lastState
            == BaseButtonAbstract.State.Pressed
        ):
            self.__currentState = BaseButtonAbstract.State.Normal

    def show(self):
        if self.__stateChanged:
            self.__createButtonSurface()
            pygame.draw.rect(
                self.__btnSurface,
                self.__color,
                self.__btnRect,
                0,
                border_radius=self.__radius,
            )
            text, textX, textY = self.__prepareText()
            self.__btnSurface.blit(text, (textX, textY))
        self.__surface.blit(self.__btnSurface, self.__rect)
