from typing import Tuple, List
from OpenGL.GL import (
    glBegin,
    glEnd,
    glShadeModel,
    glVertex3f,
    glColor3f,
    glLineWidth,
    GL_LINES,
    GL_QUADS,
    GL_FLAT,
)


def Cube(
    position: Tuple[int, int, int] | int,
    size: Tuple[int, int, int] | int,
    colors: List[Tuple[int, int, int]] | Tuple[int, int, int] | int,
    border: float = 0.0
):
    def CalculateVertices(cubePositon: Tuple[int, int, int], cubeSize: Tuple[int, int, int]):
        px, py, pz = cubePositon
        lx = cubeSize[0] / 2
        ly = cubeSize[1] / 2
        lz = cubeSize[2] / 2
        vertices = (
            (px + +1 * lx, py + -1 * ly, pz + -1 * lz),
            (px + +1 * lx, py + +1 * ly, pz + -1 * lz),
            (px + -1 * lx, py + +1 * ly, pz + -1 * lz),
            (px + -1 * lx, py + -1 * ly, pz + -1 * lz),
            (px + +1 * lx, py + -1 * ly, pz + +1 * lz),
            (px + +1 * lx, py + +1 * ly, pz + +1 * lz),
            (px + -1 * lx, py + -1 * ly, pz + +1 * lz),
            (px + -1 * lx, py + +1 * ly, pz + +1 * lz),
        )
        return vertices
    edges = ((0, 1), (0, 3), (0, 4), (2, 1), (2, 3), (2, 7), (6, 3), (6, 4), (6, 7), (5, 1), (5, 4), (5, 7),)
    surfaces = ((0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4), (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6),)
    cubeSize = (size if isinstance(size, tuple) and len(size) == 3 else (size, size, size))
    cubePositon = (
        position
        if isinstance(position, tuple) and len(position) == 3
        else (position, 0, 0)
    )
    cubeColors: List[Tuple[float, float, float]] = [(0.0, 0.0, 0.0)]*6
    if isinstance(colors, list):
        for i, color in enumerate(colors):
            cubeColors[i] = [(
                (color[0] / 255, color[1] / 255, color[2] / 255)
                if isinstance(color, tuple) and len(color) == 3
                else (color / 255, color / 255, color / 255)
            )]
    else:
        cubeColors = [(
            (colors[0] / 255, colors[1] / 255, colors[2] / 255)
            if isinstance(colors, tuple) and len(colors) == 3
            else (colors / 255, colors / 255, colors / 255)
        )]*6
    vertices = CalculateVertices(cubePositon, cubeSize)
    if not border:
        glShadeModel(GL_FLAT)
        glBegin(GL_QUADS)
        for i, surface in enumerate(surfaces):
            for vertex in surface:
                glColor3f(*cubeColors[i])
                glVertex3f(*vertices[vertex])
        glEnd()
    else:
        glLineWidth(border)
        glBegin(GL_LINES)
        glColor3f(*cubeColors[0])
        for edge in edges:
            for vertex in edge:
                glVertex3f(*vertices[vertex])
        glEnd()
