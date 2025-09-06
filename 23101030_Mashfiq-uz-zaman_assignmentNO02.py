from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

w,h=800,600
mid=w//2
bar=400
ball_x,ball_y=random.randint(100,700), 550
bar_h=15
bar_w=60
pause=False
game_over=False
score=0
fall=5

def pixels(x,y):
    glVertex2i(int(x),int(y))
def midpoint(x1,y1,x2,y2):
    glBegin(GL_POINTS)
    dy=y2-y1
    dx=x2-x1
    if dy >=0:
        y_value=1
    else:
        y_value=-1
    if dx >=0:
        x_value=1
    else:
        x_value=-1
    dx=abs(dx)
    dy=abs(dy)
    x,y=x1,y1
    if dx>dy:
        d=2*dy-dx
        east=2*dy
        northeast=2*(dy-dx)
        while x!=x2:
            pixels(x, y)
            if d<=0:
                d+=east
            else:
                d+=northeast
                y+=y_value
            x+=x_value
    else:
        d=2*dx-dy
        east=2*dx
        northeast=2*(dx-dy)
        while y!=y2:
            pixels(x, y)
            if d<=0:
                d+=east
            else:
                d+=northeast
                x+=x_value
            y+=y_value
    pixels(x2,y2)
    glEnd()
def bar(x):
    y=12
    if game_over==False:
        glColor3f(1,0,1)
    else:
        glColor3f(1,0,0)
    midpoint(x-bar_w,y+bar_h, x+bar_w,y+bar_h)
    midpoint(x+bar_w//2 ,y , x+bar_w,y+bar_h)
    midpoint(x-bar_w,y+bar_h,x-bar_w//2 ,y)
    midpoint(x-bar_w//2,y,x+bar_w//2 ,y)

def ball(x,y):
    size=10
    r=random.uniform(0.6,1)
    g=random.uniform(0.6,1)
    b=random.uniform(0.6,1)
    glColor3f(r,g,b)
    midpoint(x, y + size, x + size, y)
    midpoint(x + size, y, x, y - size)
    midpoint(x, y - size, x - size, y)
    midpoint(x - size, y, x, y + size)

def control():
    glColor3f(0,1,1)
    midpoint(50, h - 50, 30, h - 40)
    midpoint(30, h - 40, 30, h - 60)
    midpoint(30, h - 60, 50, h - 50)

    glColor3f(1,0.6,0)
    if pause:
        midpoint(400, h  - 60, 400 + 20, h - 50)
        midpoint(400 + 20, h  - 50, 400, h  - 40)
        midpoint(400, h  - 40, 400, h  - 60)
    else:
        midpoint(400, h - 60, 400,h - 40)
        midpoint(400 + 20,h- 60, 400 + 20, h - 40)

    glColor3f(1,0,0)
    midpoint(w-50,h-60,w-30,h-40)
    midpoint(w-30,h-60,w-50,h-40)

def draw_text(x, y, text, r=1, g=1, b=1):
    from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
    glColor3f(r, g, b)
    glRasterPos2i(x, y)
    for i in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(i))
def crash():
    bottom=12
    bar_top=bottom+bar_h
    bar_left = mid - bar_w
    bar_right = mid + bar_w
    ball_bot=ball_y-10
    return(bar_left <= ball_x <= bar_right and
           bottom <= ball_bot <= bar_top)   

def draw_scene():
    glClearColor(0, 0, 0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, w, 0, h)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    bar(mid)
    ball(ball_x, int(ball_y))
    control()
    draw_text(20, h - 30, f"Score: {score}", 1, 1, 1)
    if game_over:
        draw_text(w // 2 - 50, h // 2, "Game Over", 1, 0, 0)
        draw_text(w // 2 - 70, h// 2 - 30, f" Final Score: {score}", 1, 1, 1)
    glutSwapBuffers() 
def update():
    global ball_x,ball_y,fall,score,game_over
    if not pause and not game_over:
        ball_y-=fall
        if crash():
            score+=1
            ball_y=h-50
            ball_x=random.randint(100,w-100)
            fall+=0.7
        elif ball_y <0:
            game_over=True
    glutPostRedisplay()
    time.sleep(1 / 60) 

def keyboard(key, x, y):
    global mid
    if not game_over and not pause:
        if key == b'a' and mid - bar_w // 2 > 0:
            mid-= 25
        elif key == b'd' and mid + bar_w // 2 < w:
            mid += 25
def mouse(button, state, x, y):
    global pause, game_over, ball_x, ball_y, score, fall
    y = h - y
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if 30 <= x <= 50 and h - 60 <= y <= h - 40:
            pause = False
            game_over = False
            score = 0
            fall = 5
            ball_y = h - 50
            ball_x = random.randint(100, w - 100)
        elif (w // 2)<= x <= (w // 2)+20 and h - 60 <= y <= h - 40:
            pause = not pause
        elif (w - 50) <= x <= (w - 30) and h - 60 <= y <= h - 40:
            glutLeaveMainLoop()
            

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(w, h)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Catch the ball")
    glutDisplayFunc(draw_scene)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutIdleFunc(update)
    glutMainLoop()

if __name__ == '__main__':
    main()