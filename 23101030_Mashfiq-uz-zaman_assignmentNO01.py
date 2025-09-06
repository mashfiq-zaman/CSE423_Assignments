from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random

wi,hi= 600,600
rain=[]
speed=2
bending=6
bg=[0,0,0] 
count=200
length=2
target=bg[:] #night to day
change_speed=0.002
rain_state=0

for i in range(count):
    x=random.uniform(0,wi)
    y=random.uniform(0,hi)
    rain.append([x,y])

def bg1():
    glBegin(GL_TRIANGLES)
    glColor3f(*bg)
    glVertex(0,hi)
    glVertex(hi,wi)   #skyyy
    glVertex(wi,hi/2)
    glVertex(0,hi)
    glVertex(0,hi/2)
    glVertex(wi,hi/2)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 0.6, 0.0)
    glVertex(0,0)
    glVertex(wi,0)   #ground
    glVertex(wi,hi/1.5)
    glVertex(0,0)
    glVertex(0,hi/1.5)
    glVertex(wi,hi/1.5)
    glEnd()

    
def house():
    wallc=(1, 1, 1)
    roofc=(0, 0, 0.5)
    doorc=(0, 0, 0.5)
    windowc=(0, 0, 0.5)
    glColor3f(*wallc)
    glBegin(GL_TRIANGLES)
    glVertex2f(100, 150)
    glVertex2f(400, 150)
    glVertex2f(100, 300)

    glVertex2f(400, 150)
    glVertex2f(400, 300)
    glVertex2f(100, 300)
    glEnd()
 
    
    glColor3f(*roofc)
    glBegin(GL_TRIANGLES)
    glVertex2f(80, 300)
    glVertex2f(250, 450)
    glVertex2f(420, 300)
    glEnd()

    glColor3f(*doorc)
    glBegin(GL_TRIANGLES)
    glVertex2f(220, 150)
    glVertex2f(280, 150)
    glVertex2f(220, 230)

    glVertex2f(280, 150)
    glVertex2f(280, 230)
    glVertex2f(220, 230)
    glEnd()

    glColor3f(1.0, 0.84, 0.0)
    glPointSize(8)
    glBegin(GL_POINTS)  #noob
    glVertex2f(272, 190)
    glEnd()

    glColor3f(*windowc)
    glBegin(GL_TRIANGLES)
    glVertex2f(310, 230)
    glVertex2f(350, 230)
    glVertex2f(310, 270)
    glVertex2f(350, 230)
    glVertex2f(350, 270)
    glVertex2f(310, 270)
    
    glVertex2f(150, 230)
    glVertex2f(190, 230)
    glVertex2f(150, 270)
    glVertex2f(190, 230)
    glVertex2f(190, 270)
    glVertex2f(150, 270)
    glEnd()

    glColor3f(1, 1, 1)
    glLineWidth(2)
    glBegin(GL_LINES)

    glVertex2f(310, 250)
    glVertex2f(350, 250)
    glVertex2f(330, 230)
    glVertex2f(330, 270)     ##window cross

    glVertex2f(150, 250)
    glVertex2f(190, 250)
    glVertex2f(170, 230)
    glVertex2f(170, 270)
    glEnd()
def rains():
    glColor3f(0.6, 0.8, 1.0)
    glBegin(GL_LINES)
    for i in rain:
        glVertex2f(i[0], i[1])
        glVertex2f(i[0] + bending, i[1] - length)
    glEnd()
def change_rain():
    global rain
    for i in rain:
        i[0]+=bending
        i[1]-=speed
        if i[1]<0:
            i[1]=hi
            i[0]-=bending*hi/speed
        if i[0]<0:
            i[0]+=wi
        if i[0]>wi:
            i[0]-=wi

def trees():
    treewi= 30
    treehi = 60
    yvalue = 300
    glColor3f(1.0, 0.8, 0.2)
    glBegin(GL_TRIANGLES)
    for i in range(4):
        a=5 + i *treewi
        glVertex2f(a - treewi / 2, yvalue)
        glVertex2f(a + treewi / 2, yvalue)
        glVertex2f(a, yvalue + treehi)
    for i in range(8):
        a=410 + i *treewi
        glVertex2f(a - treewi / 2, yvalue)
        glVertex2f(a + treewi / 2, yvalue)
        glVertex2f(a, yvalue + treehi)
    glEnd()
def change_bg():
    global bg, target
    for i in range(3):
        if abs(bg[i] - target[i]) > 0.001:
            if bg[i] < target[i]:
                bg[i] += change_speed
            else:
                bg[i] -= change_speed
def mouse(button,state,x,y):
    global rain_state,bending
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        rain_state=(rain_state+1)%3
        if rain_state==0:
            bending=6
        elif rain_state==1:
            bending=-6
        else:
            bending = 0
def keyboard_dn(key, x, y):
    global target
    if key == b"q": 
        target = [1, 1, 1]
    elif key == b"w": 
        target = [0, 0, 0]
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    bg1()
    trees()
    house()
    rains()
    glutSwapBuffers()
def idle():
    change_rain()
    change_bg()
    glutPostRedisplay()
def init():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, wi, 0, hi)

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(wi,hi)
glutCreateWindow(b"yeee bristi")
init()
glutDisplayFunc(display)
glutMouseFunc(mouse)
glutKeyboardFunc(keyboard_dn)
glutIdleFunc(idle)
glutMainLoop()


##task2
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import time

wi,hi=600,600
bg=(0,0,0)
dots=[]
speed=0.0001
state=True
blink=False
blinktime=0.3
b_track=time.time()
def random_color():
    return (random.random(), random.random(), random.random())
def random_direction():
    dx = random.choice([-1, 1])
    dy = random.choice([-1, 1])
    return (dx, dy)

def points(pos,color):
    if blink and not state:
        ptime=time.time()
        if (int(ptime * 3.33) % 2) == 0:
            glColor3f(0,0,0)
        else:
            glColor3f(color)
    else:
        glColor3fv(color)

    glBegin(GL_POINTS)
    glVertex3fv(pos)
    glEnd()
def update():
    if state==False:
        return
    else:
        for i in range(len(dots)):
             x, y, color, direction = dots[i]
             new_x = x + speed * direction[0]
             new_y = y + speed * direction[1]
             if abs(new_x) >= 1:
                direction = (-direction[0], direction[1])
             if abs(new_y) >= 1:
                direction = (direction[0], -direction[1])
             dots[i] = (new_x, new_y, color, direction)


def speed1(key, x, y):
    global speed
    if state:
        if key == GLUT_KEY_UP:
            speed += 0.0005
        elif key == GLUT_KEY_DOWN:
            if speed > 0.00005:
                speed -= 0.0005
def keyboard(key, x, y):
    global state
    if key == b"s":
        state = not state
def mouse(button, states, x, y):
    global blink
    if states == GLUT_DOWN :
        xnew = (x / wi) * 2 - 1
        ynew = -((y / hi) * 2 - 1)

        if button == GLUT_RIGHT_BUTTON:
            color = random_color()
            direction = random_direction()
            dots.append((xnew, ynew, color, direction))
        elif button == GLUT_LEFT_BUTTON:
            blink = not blink

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    update()
    glPointSize(7.0)
    for x, y, color, _ in dots:
        points((x, y, 0), color)
    glutSwapBuffers()

glutInit()
glutInitWindowSize(wi, hi)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutCreateWindow(b"magicc boxx")

glClearColor(*bg, 1.0)
glutDisplayFunc(display)
glutIdleFunc(glutPostRedisplay)
glutMouseFunc(mouse)
glutSpecialFunc(speed1)
glutKeyboardFunc(keyboard)
gluOrtho2D(-1, 1, -1, 1)

glutMainLoop()