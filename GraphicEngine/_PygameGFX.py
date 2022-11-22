from __future__ import annotations

import warnings
from abc import ABC, abstractmethod
from typing import Callable, Literal, Optional, Tuple

import pygame
from OpenGL.GL import glTranslatef  # type: ignore
from OpenGL.GL import (GL_COLOR_BUFFER_BIT,  # type: ignore
                       GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST, GL_LESS,  # type: ignore
                       GL_LINE_SMOOTH, GL_LINE_SMOOTH_HINT, GL_NICEST,  # type: ignore
                       GL_SMOOTH, glClear, glClearColor, glClearDepth,  # type: ignore
                       glDepthFunc, glEnable, glHint, glRotatef, glShadeModel)  # type: ignore
from OpenGL.GLU import gluPerspective  # type: ignore

import GraphicEngine._common as _common
import GraphicEngine.shapes as shapes
from GraphicEngine._baseButton import BaseButtonAbstract
from GraphicEngine._processColor import getColor_Int
from GraphicEngine._textInput import TextInputAbstract

warnings.simplefilter("once", category=(PendingDeprecationWarning, DeprecationWarning))  # type: ignore


class PygameGFX(ABC):
    __height: int
    __width: int
    __mousePosition: Tuple[int, int]
    __displaySufrace: pygame.surface.Surface
    __running: bool
    __fps: int
    __keyCode: int
    fieldOfView: int = 45
    drawShapes = shapes

    @property
    def DisplaySurface(self):
        return self.__displaySufrace

    @property
    def Width(self):
        return self.__width

    @property
    def Height(self):
        return self.__height

    @property
    def Font(self):
        return self.__font

    @property
    def IsRunning(self):
        return self.__running

    @property
    def keyCode(self) -> int:
        return self.__keyCode

    @property
    def mousePosition(self):
        self.__mousePosition = pygame.mouse.get_pos()
        return self.__mousePosition

    @property
    def aspectRatio(self):
        return self.Width / self.Height

    class Button(BaseButtonAbstract):
        def __init__(
            self,
            surface: pygame.Surface,
            rect: pygame.Rect,
            command: Callable[[], None] | None = None,
            label: str = "Button",
            padx: int = 0,
            pady: int = 0,
            font: Optional[pygame.font.Font] = None,
            background: _common.ColorValue = (0xEF, 0xEF, 0xEF),
            foreground: _common.ColorValue = (0x00, 0x00, 0x00),
            activeBackground: _common.ColorValue = (0x8D, 0x8D, 0x8D),
            activeForeground: _common.ColorValue = (0x00, 0x00, 0x00),
            justify: Literal["LEFT"] | Literal["CENTER"] | Literal["RIGHT"] = "CENTER",
        ):
            super(PygameGFX.Button, self).__init__(
                surface,
                rect,
                command,
                background,
                foreground,
                activeBackground,
                activeForeground,
                label,
                justify,
                font,
                padx,
                pady,
            )

        def update(self):
            super().update()

        def show(self):
            super().show()

    class TextInput(TextInputAbstract):
        def __init__(
            self,
            surface: pygame.Surface,
            rect: pygame.Rect,
            text: str,
            background: _common.ColorValue = (255, 255, 255),
            foreground: _common.ColorValue = (0, 0, 0),
            justify: Literal["LEFT"] | Literal["CENTER"] | Literal["RIGHT"] = "CENTER",
            font: Optional[pygame.font.Font] = None,
            padx: int = 0,
            pady: int = 0,
        ):
            super(PygameGFX.TextInput, self).__init__(
                surface, rect, text, background, foreground, justify, font, padx, pady
            )

    def __init__(
        self,
        width: int = 0,
        height: int = 0,
        caption: Optional[str] = None,
        fps: Optional[int] = None,
        flags: int = pygame.SRCALPHA,
    ) -> None:
        self.__running = True
        self.__flags = pygame.DOUBLEBUF | flags
        if height and width:
            self.__displaySufrace = pygame.display.set_mode(
                (width, height), self.__flags
            )
            self.__height = height
            self.__width = width
        else:
            self.__displaySufrace = pygame.display.set_mode(
                (0, 0), self.__flags, pygame.FULLSCREEN
            )
            self.__height = self.__displaySufrace.get_width()
            self.__width = self.__displaySufrace.get_height()
        self.__fps = fps if fps is not None else 60
        self.FramePerSec = pygame.time.Clock()
        if caption:
            pygame.display.set_caption(caption)

    def _checkForEvents(self):
        events = pygame.event.get()
        for event in events:
            match event.type:
                case pygame.QUIT:
                    self.__running = False
                case pygame.KEYDOWN:
                    self.__keyCode = event.key
                    self.keyPressed()
                case pygame.KEYUP:
                    self.__keyCode = event.key
                    self.keyReleased()
                case pygame.MOUSEBUTTONDOWN:
                    self.__mousePosition = pygame.mouse.get_pos()
                    self.mousePressed()
                case pygame.MOUSEBUTTONUP:
                    self.__mousePosition = pygame.mouse.get_pos()
                    self.mouseReleased()

    def setCanvasSize(self, width: int, height: int):
        self.__height = height
        self.__width = width
        self.__displaySufrace = pygame.display.set_mode(
            (self.__width, self.__height), pygame.SRCALPHA
        )

    def Stop(self):
        self.__running = False

    def setPerspective(
        self, fieldOfView: Optional[int] = None, near: float = 0.1, far: Optional[float] = None
    ):
        """
        Only for OpenGL
        """
        if pygame.OPENGL & self.__flags != pygame.OPENGL:
            return
        if fieldOfView:
            self.fieldOfView = fieldOfView
        nearVal = 0.1 if near is None else near
        farVal = max([self.Width, self.Height]) * 2 if far is None else far
        gluPerspective(self.fieldOfView, self.aspectRatio, nearVal, farVal)

    def translate(self, x: float, y: float, z: float):
        """
        Only for OpenGL now
        """
        glTranslatef(x, y, z)

    def rotate(
        self,
        angle: float,
        x: _common.Direction,
        y: _common.Direction,
        z: _common.Direction,
    ):
        """
        Only for OpenGL now
        """
        if pygame.OPENGL & self.__flags != pygame.OPENGL:
            return
        glRotatef(angle, x, y, z)

    def Run(self):
        pygame.init()
        self.setFont()
        if pygame.OPENGL & self.__flags == pygame.OPENGL:
            glClearDepth(1.0)
            glDepthFunc(GL_LESS)  # type: ignore
            glEnable(GL_DEPTH_TEST)  # type: ignore
            glShadeModel(GL_SMOOTH)  # type: ignore
            self.setPerspective()
        self.Setup()
        while self.IsRunning:
            self._checkForEvents()
            self.Draw()
            pygame.display.flip()
            pygame.time.wait(int(1000 / self.__fps))
            if self.__fps:
                self.FramePerSec.tick(self.__fps)
            else:
                self.FramePerSec.tick()

    def background(self, color: _common.ColorValue):
        def bg_2d(r: int, g: int, b: int):
            self.__displaySufrace.fill((r, g, b))

        def bg_2d_transparent(r: int, g: int, b: int, a: int):
            surface = pygame.Surface((self.Width, self.Height), pygame.SRCALPHA)
            pygame.draw.rect(
                surface,
                (r, g, b, a),
                pygame.Rect(0, 0, self.Width, self.Height),
            )
            self.__displaySufrace.blit(surface, (0, 0))

        def bg_3d(r: int, g: int, b: int, a: int):
            glClearColor(r / 255, g / 255, b / 255, a / 255)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # type: ignore
            glEnable(GL_LINE_SMOOTH)  # type: ignore
            glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)  # type: ignore

        r, g, b, a = getColor_Int(color)  # type: ignore

        if pygame.OPENGL & self.__flags == pygame.OPENGL:
            bg_3d(r, g, b, a)
        elif a != 0:
            bg_2d_transparent(r, g, b, a)
        else:
            bg_2d(r, g, b)

    def setFont(self, fontName: str = '', fontSize: int = 24):
        self.__font = pygame.font.SysFont(fontName, fontSize)

    def keyPressed(self):
        pass

    def keyReleased(self):
        pass

    def mousePressed(self):
        pass

    def mouseReleased(self):
        pass

    @abstractmethod
    def Setup(self):
        ...

    @abstractmethod
    def Draw(self):
        ...
