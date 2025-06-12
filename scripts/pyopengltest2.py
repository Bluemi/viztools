#!/usr/bin/env python3


from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import math

width, height = 800, 600
circle_texture = None
fbo = None

def init_fbo():
    global circle_texture, fbo
    size = 128
    circle_texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, circle_texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, size, size, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    fbo = glGenFramebuffers(1)
    glBindFramebuffer(GL_FRAMEBUFFER, fbo)
    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, circle_texture, 0)
    if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
        print("FBO incomplete")

    glViewport(0, 0, size, size)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix(); glLoadIdentity(); gluOrtho2D(-1, 1, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix(); glLoadIdentity()

    glClearColor(0, 0, 0, 0); glClear(GL_COLOR_BUFFER_BIT)
    glEnable(GL_BLEND); glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(1, 0, 0, 0.5)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(0, 0)
    for i in range(0, 361, 10):
        theta = math.radians(i)
        glVertex2f(math.cos(theta), math.sin(theta))
    glEnd()
    glDisable(GL_BLEND)

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    glBindFramebuffer(GL_FRAMEBUFFER, 0)
    glViewport(0, 0, width, height)

def display():
    glClear(GL_COLOR_BUFFER_BIT)

    # line
    glColor3f(0, 1, 0)
    glBegin(GL_LINES)
    glVertex2f(-0.8, -0.8)
    glVertex2f(0.8, 0.8)
    glEnd()

    # text
    glColor3f(1, 1, 1)
    glRasterPos2f(-0.9, 0.9)
    for c in b"Hello, PyOpenGL!":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, c)

    # two circles from texture
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, circle_texture)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    for x in [-0.3, 0.3]:
        glPushMatrix()
        glTranslatef(x, 0, 0)
        glScalef(0.5, 0.5, 1)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(-1, -1)
        glTexCoord2f(1, 0); glVertex2f(1, -1)
        glTexCoord2f(1, 1); glVertex2f(1, 1)
        glTexCoord2f(0, 1); glVertex2f(-1, 1)
        glEnd()
        glPopMatrix()
    glDisable(GL_BLEND)
    glDisable(GL_TEXTURE_2D)

    glutSwapBuffers()

def reshape(w, h):
    global width, height
    width, height = w, h
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1, 1, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"Buffered Circles")
    init_fbo()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glClearColor(0, 0, 0, 1)
    glutMainLoop()

if __name__ == "__main__":
    main()
