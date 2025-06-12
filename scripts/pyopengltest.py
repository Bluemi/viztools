#!/usr/bin/env python3


from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import math

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # draw line
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex2f(-0.8, -0.8)
    glVertex2f(0.8, 0.8)
    glEnd()

    # draw text
    glColor3f(1.0, 1.0, 1.0)
    glRasterPos2f(-0.9, 0.9)
    for c in b"Hello, PyOpenGL!":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, c)

    # draw transparent circle
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(1.0, 0.0, 0.0, 0.5)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(0.0, 0.0)
    for i in range(0, 361, 60):
        theta = math.radians(i)
        x = 0.5 * math.cos(theta)
        y = 0.5 * math.sin(theta)
        glVertex2f(x, y)
    glEnd()
    glDisable(GL_BLEND)

    glutSwapBuffers()

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1, 1, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Line, Text, Transparent Circle")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glutMainLoop()

if __name__ == "__main__":
    main()
