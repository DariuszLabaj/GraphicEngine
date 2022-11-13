from __future__ import annotations

import warnings
from abc import ABC, abstractmethod
from typing import Callable, Literal, Optional, Tuple

import pygame
from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_TEST,
    GL_LESS,
    GL_LINE_SMOOTH,
    GL_LINE_SMOOTH_HINT,
    GL_NICEST,
    GL_SMOOTH,
    glClear,
    glClearColor,
    glClearDepth,
    glDepthFunc,
    glEnable,
    glHint,
    glRotatef,
    glShadeModel,
    glTranslatef,
)
from OpenGL.GLU import gluPerspective

import GraphicEngine.shapes as shapes
from GraphicEngine._baseButton import _BaseButton
from GraphicEngine._common import _Direction, deprecate
from GraphicEngine._textInput import _TextInput
from GraphicEngine._processColor import getColor_Int

warnings.simplefilter("once", category=(PendingDeprecationWarning, DeprecationWarning))


class PygameGFX(ABC):
    __height: int
    __width: int
    __mousePosition: Tuple[int, int]
    __displaySufrace: pygame.Surface
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

    class Button(_BaseButton):
        def __init__(
            self,
            surface: pygame.Surface,
            rect: pygame._common._RectValue,
            command: Callable[[], None] | None = None,
            label: str = "Button",
            padx: int = 0,
            pady: int = 0,
            font: str = None,
            background: pygame._common._ColorValue = (0xEF, 0xEF, 0xEF),
            foreground: pygame._common._ColorValue = (0x00, 0x00, 0x00),
            activeBackground: pygame._common._ColorValue = (0x8D, 0x8D, 0x8D),
            activeForeground: pygame._common._ColorValue = (0x00, 0x00, 0x00),
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

    class TextInput(_TextInput):
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
        self, fieldOfView: int = None, near: float = 0.1, far: float = 100.0
    ):
        """
        Only for OpenGL
        """
        if pygame.OPENGL & self.__flags != pygame.OPENGL:
            return
        if fieldOfView:
            self.fieldOfView = fieldOfView
        nearVal = 0.1 if near is None else near
        farVal = 100 if far is None else far
        gluPerspective(self.fieldOfView, self.aspectRatio, nearVal, farVal)

    def translate(self, x: float, y: float, z: float):
        """
        Only for OpenGL now
        """
        glTranslatef(x, y, z)

    def rotate(
        self,
        angle: float,
        x: _Direction,
        y: _Direction,
        z: _Direction,
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
            glDepthFunc(GL_LESS)
            glEnable(GL_DEPTH_TEST)
            glShadeModel(GL_SMOOTH)
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

    def background(self, color: pygame._common._ColorValue):
        def bg_2d(r: int, g: int, b: int):
            self.__displaySufrace.fill((r, g, b))

        def bg_2d_transparent(r: int, g: int, b: int, a: int):
            surface = pygame.Surface((self.Width, self.Height), pygame.SRCALPHA)
            pygame.draw.rect(
                surface,
                (r, g, b, g),
                pygame.Rect(0, 0, self.Width, self.Height),
            )
            self.__displaySufrace.blit(surface, (0, 0))

        def bg_3d(r: int, g: int, b: int, a: int):
            glClearColor(r / 255, g / 255, b / 255, a / 255)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glEnable(GL_LINE_SMOOTH)
            glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

        r, g, b, a = getColor_Int(color)

        if pygame.OPENGL & self.__flags == pygame.OPENGL:
            bg_3d(r, g, b, a)
        elif a != 0:
            bg_2d_transparent(r, g, b, a)
        else:
            bg_2d(r, g, b)

    def setFont(self, fontName: str | None = None, fontSize: int = 24):
        self.__font = pygame.font.SysFont(fontName, fontSize)

    @deprecate("This function will be deprecated in the future. Use drawShapes.Text().")
    def drawText(
        self,
        text: str,
        color: pygame._common._ColorValue,
        position: pygame._common._Coordinate = (20, 20),
        allowedWidth: int = None,
    ):
        return self.drawShapes.Text(
            self.DisplaySurface, self.__font, text, color, position, allowedWidth
        )

    @deprecate(
        "This function will be deprecated in the future. Use drawShapes.Pixel()."
    )
    def drawPixel(
        self, color: pygame._common._ColorValue | float, pos: pygame._common._Coordinate
    ):
        self.drawShapes.Pixel(self.DisplaySurface, color, pos)

    @deprecate("This function will be deprecated in the future. Use drawShapes.Arc().")
    def drawArc(
        self,
        rect: pygame.Rect,
        color: pygame._common._ColorValue,
        startAngle: float,
        stopAngle: float,
        width: int = 1,
    ):
        self.drawShapes.Arc(
            self.DisplaySurface, rect, color, startAngle, stopAngle, width
        )

    @deprecate(
        "This function will be deprecated in the future. Use drawShapes.Circle()."
    )
    def drawCircle(
        self,
        center: pygame._common._Coordinate,
        radius: float,
        color: pygame._common._ColorValue,
        width: int = 0,
    ):
        self.drawShapes.Circle(self.DisplaySurface, center, radius, color, width)

    @deprecate(
        "This function will be deprecated in the future. Use drawShapes.Ellipse()."
    )
    def drawEllipse(
        self, rect: pygame.Rect, color: pygame._common._ColorValue, width: int = 0
    ):
        self.drawShapes.Ellipse(self.DisplaySurface, rect, color, width)

    @deprecate("This function will be deprecated in the future. Use drawShapes.Line().")
    def drawLine(
        self,
        startPos: pygame._common._Coordinate,
        endPos: pygame._common._Coordinate,
        color: pygame._common._ColorValue,
        width: int = 1,
    ):
        self.drawShapes.Line(self.DisplaySurface, startPos, endPos, color, width)

    @deprecate("This function will be deprecated in the future. Use drawShapes.Rect().")
    def drawRect(
        self,
        rect: pygame.Rect,
        color: pygame._common._ColorValue,
        width: int = 0,
        borderRadius: int = -1,
        borderTopLeftRadius: int = -1,
        borderTopRightRadius: int = -1,
        borderBottomLeftRadius: int = -1,
        borderBottmRightRadius: int = -1,
    ):
        self.drawShapes.Rect(
            self.DisplaySurface,
            rect,
            color,
            width,
            borderRadius,
            borderTopLeftRadius,
            borderTopRightRadius,
            borderBottomLeftRadius,
            borderBottmRightRadius,
        )

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
