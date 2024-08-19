from __future__ import annotations

import warnings
from abc import ABC, abstractmethod
from typing import Callable, Literal, Optional, Tuple, Union, overload

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
    __backgroundSurface: pygame.surface.Surface
    __displaySurface: pygame.surface.Surface
    __running: bool
    __fps: int
    __keyCode: int
    __translationMatrix: list[tuple[float, float]] = [(0.0, 0.0)]
    __fill: Optional[_common.ColorValue] = None
    __stroke: Optional[_common.ColorValue] = None
    __strokeWeight: int = 0
    fieldOfView: int = 45
    drawShapes = shapes

    @property
    def BackgroundSurface(self):
        return self.__backgroundSurface

    @property
    def DisplaySurface(self):
        return self.__displaySurface

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

    @property
    def __xTranslation(self) -> float:
        return self.__translationMatrix[self.__translationIndex][0]

    @property
    def __yTranslation(self) -> float:
        return self.__translationMatrix[self.__translationIndex][1]

    @property
    def __translationIndex(self) -> int:
        return len(self.__translationMatrix)-1

    class Button(BaseButtonAbstract):
        def __init__(
            self,
            surface: pygame.Surface,
            rect: pygame.Rect,
            command: Callable[[], None] | None = None,
            label: str = "Button",
            padX: int = 0,
            padY: int = 0,
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
                padX,
                padY,
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
            padX: int = 0,
            padY: int = 0,
        ):
            super(PygameGFX.TextInput, self).__init__(
                surface, rect, text, background, foreground, justify, font, padX, padY
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
            self.__backgroundSurface = pygame.display.set_mode(
                (width, height), self.__flags
            )
            self.__height = height
            self.__width = width
        else:
            self.__backgroundSurface = pygame.display.set_mode(
                (0, 0), self.__flags, pygame.FULLSCREEN
            )
            self.__height = self.__backgroundSurface.get_width()
            self.__width = self.__backgroundSurface.get_height()
        self.__displaySurface = pygame.Surface(self.__backgroundSurface.get_rect().size, pygame.SRCALPHA)
        self.__fps = fps if fps is not None else 60
        self.FramePerSec = pygame.time.Clock()
        if caption:
            pygame.display.set_caption(caption)

    def _checkForEvents(self):
        events = pygame.event.get()
        for event in events:
            match event.type:  # type: ignore
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
        self.__backgroundSurface = pygame.display.set_mode(
            (self.__width, self.__height), pygame.SRCALPHA
        )

    def Stop(self):
        self.__running = False

    def setPerspective(
        self, fieldOfView: Optional[int] = None, near: Optional[float] = 0.1, far: Optional[float] = None
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

    @overload
    def translate(self, x: float, y: float) -> None:
        ...

    @overload
    def translate(self, x: float, y: float, z: float) -> None:
        ...

    def translate(self, x: float, y: float, z: Optional[float] = None) -> None:
        """
        Only for OpenGL now
        """
        if (z is not None):
            glTranslatef(x, y, z)
        newX = self.__xTranslation + x
        newY = self.__yTranslation + y
        self.__translationMatrix[self.__translationIndex] = (newX, newY)

    def push(self):
        self.__translationMatrix.append((self.__xTranslation, self.__yTranslation))

    def pop(self):
        if (self.__translationIndex > 0):
            self.__translationMatrix.pop()

    def fill(self, color: _common.ColorValue):
        self.__fill = color

    def noFill(self):
        self.__fill = None

    def stroke(self, color: _common.ColorValue):
        self.__stroke = color

    def noStroke(self):
        self.__stroke = None

    def strokeWeight(self, value: int):
        self.__strokeWeight = value

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
            self.__translationMatrix[self.__translationIndex] = (0.0, 0.0)
            self.Draw()
            self.BackgroundSurface.blit(self.DisplaySurface, (0, 0))
            pygame.display.flip()
            pygame.time.wait(int(1000 / self.__fps))
            if self.__fps:
                self.FramePerSec.tick(self.__fps)
            else:
                self.FramePerSec.tick()

    def background(self, color: _common.ColorValue):
        def bg_2d(r: int, g: int, b: int):
            self.__backgroundSurface.fill((r, g, b))
            self.__displaySurface = pygame.Surface(self.__backgroundSurface.get_rect().size, pygame.SRCALPHA)

        def bg_3d(r: int, g: int, b: int, a: int):
            glClearColor(r / 255, g / 255, b / 255, a / 255)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # type: ignore
            glEnable(GL_LINE_SMOOTH)  # type: ignore
            glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)  # type: ignore

        r, g, b, a = getColor_Int(color)  # type: ignore

        if pygame.OPENGL & self.__flags == pygame.OPENGL:
            bg_3d(r, g, b, a)
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

    def rect(self,
             rect: pygame._RectValue,
             borderRadius: int = -1,
             borderTopLeftRadius: int = -1,
             borderTopRightRadius: int = -1,
             borderBottomLeftRadius: int = -1,
             borderBottmRightRadius: int = -1,
             ):
        color: _common.ColorValue = (255, 255, 255) if (
            self.__stroke is None and self.__fill is None) else self.__fill if (self.__fill is not None) else self.__stroke if (self.__stroke is not None) else (255, 255, 255)
        width = 1 if self.__fill is None and self.__strokeWeight == 0 else self.__strokeWeight if self.__fill is None else 0
        newRect = pygame.Rect(self.__xTranslation+rect.left, self.__yTranslation+rect.top, rect.width, rect.height)
        pygame.draw.rect(
            self.DisplaySurface,
            color,  # type: ignore
            newRect,
            width,
            borderRadius,
            borderTopLeftRadius,
            borderTopRightRadius,
            borderBottomLeftRadius,
            borderBottmRightRadius,
        )

    def ellipse(self,
                rect: pygame._RectValue):
        color: _common.ColorValue = (255, 255, 255) if (
            self.__stroke is None and self.__fill is None) else self.__fill if (self.__fill is not None) else self.__stroke if (self.__stroke is not None) else (255, 255, 255)
        width = 1 if self.__fill is None and self.__strokeWeight == 0 else self.__strokeWeight if self.__fill is None else 0
        newRect = pygame.Rect(self.__xTranslation+rect[0]-rect[2]/2,
                              self.__yTranslation+rect[1]-rect[3] / 2, rect[2], rect[3])
        pygame.draw.ellipse(
            self.DisplaySurface,
            color,  # type: ignore
            newRect,
            width
        )

    def circle(self,
               center: _common.Coordinate,
               radius: float,
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
        color: _common.ColorValue = (255, 255, 255) if (
            self.__stroke is None and self.__fill is None) else self.__fill if (self.__fill is not None) else self.__stroke if (self.__stroke is not None) else (255, 255, 255)
        width = 1 if self.__fill is None and self.__strokeWeight == 0 else self.__strokeWeight if self.__fill is None else 0
        pygame.draw.circle(self.DisplaySurface,
                           color,  # type: ignore
                           (vect.x+self.__xTranslation, vect.y+self.__yTranslation),
                           radius,
                           width)

    def line(self,
             startPos: _common.Coordinate,
             endPos: _common.Coordinate,
             ):
        def getVector2d(Pos: _common.Coordinate):
            if isinstance(Pos, tuple) and len(Pos) >= 2:
                v1 = pygame.Vector2(Pos[0], Pos[1])
            elif isinstance(Pos, pygame.Vector2):
                v1 = Pos
            else:
                v1 = pygame.Vector2(0, 0)
            return v1
        start = getVector2d(startPos)
        end = getVector2d(endPos)
        color: _common.ColorValue = (255, 255, 255) if (
            self.__stroke is None and self.__fill is None) else self.__fill if (self.__fill is not None) else self.__stroke if (self.__stroke is not None) else (255, 255, 255)
        width = 1 if self.__strokeWeight == 0 else self.__strokeWeight
        pygame.draw.line(self.DisplaySurface,
                         color,  # type: ignore
                         (self.__xTranslation + start.x, self.__yTranslation + start.y),
                         (self.__xTranslation + end.x, self.__yTranslation + end.y),
                         width)

    def point(self, pos: _common.Coordinate):
        def getVector2d(Pos: _common.Coordinate):
            if isinstance(Pos, tuple) and len(Pos) >= 2:
                v1 = pygame.Vector2(Pos[0], Pos[1])
            elif isinstance(Pos, pygame.Vector2):
                v1 = Pos
            else:
                v1 = pygame.Vector2(0, 0)
            return v1
        vector = getVector2d(pos)
        color: _common.ColorValue = (255, 255, 255) if (
            self.__stroke is None and self.__fill is None) else self.__fill if (self.__fill is not None) else self.__stroke if (self.__stroke is not None) else (255, 255, 255)
        width = 1 if self.__strokeWeight == 0 else self.__strokeWeight
        pygame.draw.circle(self.DisplaySurface,
                           color,  # type: ignore
                           (vector.x+self.__xTranslation, vector.y+self.__yTranslation),
                           width,
                           width)

    def polygon(self, points: Union[list[_common.Coordinate], list[tuple[float, float]]]):
        def getVector2d(Pos: _common.Coordinate):
            if isinstance(Pos, tuple) and len(Pos) >= 2:
                v1 = pygame.Vector2(Pos[0], Pos[1])
            elif isinstance(Pos, pygame.Vector2):
                v1 = Pos
            else:
                v1 = pygame.Vector2(0, 0)
            return v1
        if (len(points) > 2):
            newPoints = [getVector2d(x) for x in points]
            translatedPoints = [pygame.Vector2(x.x + self.__xTranslation, x.y + self.__yTranslation) for x in newPoints]
            color: _common.ColorValue = (255, 255, 255) if (
                self.__stroke is None and self.__fill is None) else self.__fill if (self.__fill is not None) else self.__stroke if (self.__stroke is not None) else (255, 255, 255)
            width = 1 if self.__fill is None and self.__strokeWeight == 0 else self.__strokeWeight if self.__fill is None else 0
            pygame.draw.aalines(self.DisplaySurface, color, False, translatedPoints)  # type: ignore
        elif (len(points) == 2):
            self.line(points[0], points[1])
        elif (len(points) == 1):
            self.point(points[0])

    @abstractmethod
    def Setup(self):
        ...

    @abstractmethod
    def Draw(self):
        ...
