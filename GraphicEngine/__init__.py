from __future__ import annotations
from math import ceil
from typing import Callable, Literal, Optional, Tuple
from abc import ABC, abstractmethod
import pygame
from GraphicEngine.constrain import constrain
from GraphicEngine.mathMap import mathMap
from GraphicEngine.random2DVector import random2DVector
from GraphicEngine._baseButton import _BaseButton
import GraphicEngine.shapes as shapes
from OpenGL.GL import (
    glClearColor,
    glClear,
    glEnable,
    glHint,
    glClearDepth,
    glDepthFunc,
    glShadeModel,
    glRotatef,
    glTranslatef,
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_LINE_SMOOTH,
    GL_LINE_SMOOTH_HINT,
    GL_NICEST,
    GL_LESS,
    GL_SMOOTH,
    GL_DEPTH_TEST,
)
from OpenGL.GLU import gluPerspective

from GraphicEngine._textInput import _TextInput


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
        x: Literal[-1, 0, 1],
        y: Literal[-1, 0, 1],
        z: Literal[-1, 0, 1],
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

    def background(self, r: int, g: int = None, b: int = None, a: int = None):
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

        if pygame.OPENGL & self.__flags == pygame.OPENGL:
            if g and b and not a:
                bg_3d(r, g, b, 0)
            elif g and b and a:
                bg_3d(r, g, b, a)
            elif g:
                bg_3d(r, r, r, a)
            else:
                bg_3d(r, r, r, 0)
        else:
            if g and b and not a:
                bg_2d(r, g, b)
            elif g and b and a:
                bg_2d_transparent(r, g, b, a)
            elif g:
                bg_2d_transparent(r, r, r, g)
            else:
                bg_2d(r, r, r)

    def setFont(self, fontName: str | None = None, fontSize: int = 24):
        self.__font = pygame.font.SysFont(fontName, fontSize)

    def drawText(
        self,
        text: str,
        color: pygame._common._ColorValue,
        position: pygame._common._Coordinate = (20, 20),
        allowedWidth: int = None,
    ):
        if allowedWidth is None:
            allowedWidth = self.Width - position[0] - 10
        words = text.split()
        lines = []
        while len(words) > 0:
            line_words = []
            while len(words) > 0:
                line_words.append(words.pop(0))
                fontWidth, _ = self.__font.size(" ".join(line_words + words[:1]))
                if fontWidth > allowedWidth:
                    break
            lines.append(" ".join(line_words))
        y_offset = 0
        for line in lines:
            fontWidth, fontHeight = self.__font.size(line)
            textX = position[0]  # - fontWidth/2 Center
            textY = position[1] + y_offset
            self.DisplaySurface.blit(
                self.__font.render(line, True, color), (textX, textY)
            )
            y_offset += fontHeight
        return position[1] + y_offset

    def drawPixel(self, color: pygame.Color, pos: Tuple[int, int]):
        if isinstance(color, float):
            constcolor = constrain(color, 0, 255)
            tuplecolor = (int(constcolor), int(constcolor), int(constcolor))
        else:
            tuplecolor = color
        self.DisplaySurface.set_at(pos, tuplecolor)

    def drawArc(
        self,
        rect: pygame.Rect,
        color: pygame.Color,
        startAngle: float,
        stopAngle: float,
        width: int = 1,
    ):
        surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.arc(
            surface, color, surface.get_rect(), startAngle, stopAngle, width
        )
        self.DisplaySurface.blit(surface, rect)

    def drawCircle(
        self, center: pygame.Vector2, radius: float, color: pygame.Color, width: int = 0
    ):
        surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, color, (radius, radius), radius, width)
        self.DisplaySurface.blit(surface, (center.x - radius, center.y - radius))

    def drawEllipse(self, rect: pygame.Rect, color: pygame.Color, width: int = 0):
        surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.ellipse(
            surface, color, pygame.Rect(0, 0, rect.size[0], rect.size[1]), width
        )
        self.DisplaySurface.blit(surface, rect)

    def drawLine(
        self,
        startPos: pygame.Vector2,
        endPos: pygame.Vector2,
        color: pygame.Color,
        width: int = 1,
    ):
        rectWidth = ceil(abs(startPos.x - endPos.x))
        rectHeight = ceil(abs(startPos.y - endPos.y))
        if rectWidth == 0:
            rectWidth = 1
        if rectHeight == 0:
            rectHeight = 1
        surface = pygame.Surface((rectWidth, rectHeight), pygame.SRCALPHA)
        pygame.draw.line(surface, color, (0, 0), (surface.get_rect().size), width)
        self.DisplaySurface.blit(surface, startPos)

    def drawPolygon(self):
        raise NotImplementedError()

    def drawRect(
        self,
        rect: pygame.Rect,
        color: pygame.Color,
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
        self.DisplaySurface.blit(surface, rect)

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


if __name__ == "__main__":
    help(constrain)
    help(mathMap)
    help(random2DVector)
