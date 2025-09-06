from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
import math
import random


player_pos = [0, 0, 0]
player_angle = 0
camera_mode = "third"    #gamestat
game_over = False
bullets = [] 

camera_pos = (0, 500, 500)
fovY = 120
GRID_LENGTH = 95
GRID_SIZE = 22

life = 6
missed_bullets = 0
score = 0
left_bound = -GRID_SIZE * GRID_LENGTH // 2
right_bound = GRID_SIZE * GRID_LENGTH // 2   #playerstate

enemies = []
num_of_enemies = 10

cheat = False
gun = False
can_fire = True
cheat_move_angle = 0
cheat_cam_view = [-90, 30, 60]  #cheat
cheat_rotation = 0

auto_gun_follow = False

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()

    gluOrtho2D(0, 1000, 0, 600)  # left, right, bottom, top

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for i in text:
        glutBitmapCharacter(font, ord(i))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_grid(GRID_SIZE):
    half_size = GRID_SIZE // 2
    glBegin(GL_QUADS)
    for i in range(-half_size, half_size + 1):
        for j in range(-half_size, half_size + 1):
            if (i + j) % 2 == 0:
                glColor3f(1, 1, 1)
            else:
                glColor3f(0.7, 0.5, 0.95)

            x_left = i * GRID_LENGTH
            x_right = (i + 1) * GRID_LENGTH
            y_bottom = j * GRID_LENGTH            ## corner coordinates
            y_top = (j + 1) * GRID_LENGTH

            glVertex3f(x_left, y_bottom, 0)
            glVertex3f(x_right, y_bottom, 0)
            glVertex3f(x_right, y_top, 0)
            glVertex3f(x_left, y_top, 0)

    glEnd()
def border_walls():
    wall_height = 120
    barricade = GRID_LENGTH * GRID_SIZE // 2

    glBegin(GL_QUADS)

    # Top wall
    glColor3f(1, 1, 1)
    glVertex3f(-barricade, barricade, 0)
    glVertex3f(barricade, barricade, 0)
    glVertex3f(barricade, barricade, wall_height)
    glVertex3f(-barricade, barricade, wall_height)
    # Right wall
    glColor3f(0.01, 0.9, 0.01)
    glVertex3f(barricade, -barricade, 0)
    glVertex3f(barricade, barricade, 0)
    glVertex3f(barricade, barricade, wall_height)
    glVertex3f(barricade, -barricade, wall_height)
    # Left wall
    glColor3f(0, 0, 1)
    glVertex3f(-barricade, -barricade, 0)
    glVertex3f(-barricade, barricade, 0)
    glVertex3f(-barricade, barricade, wall_height)
    glVertex3f(-barricade, -barricade, wall_height)
    # Bottom wall
    glColor3f(0.01, 0.9, 1)
    glVertex3f(-barricade, -barricade, 0)
    glVertex3f(barricade, -barricade, 0)
    glVertex3f(barricade, -barricade, wall_height)
    glVertex3f(-barricade, -barricade, wall_height)
    glEnd()

def draw_bullets():
    glColor3f(1, 0, 0)
    for i in bullets:
        glPushMatrix()
        glTranslatef(*i['bullet_pos'])
        glutSolidCube(18)
        glPopMatrix()

def draw_enemy(a):
    glPushMatrix()
    glTranslatef(*a['enemy_pos'])

    #  body 
    glColor3f(1, 0, 0)
    gluSphere(gluNewQuadric(), 40 * a["scale"], 20, 20)

    # head 
    glColor3f(0, 0, 0)
    glTranslatef(0, 0, 40)
    gluSphere(gluNewQuadric(), 30 * a["scale"], 20, 20)

    glPopMatrix()

def spawn_enemy():
    x = random.randint(-650, 550)
    y = random.randint(-650, 550)
    return {'enemy_pos': [x, y, 0], 'scale': 1.0, 'scale_dir': 0.005}

def player():
    glPushMatrix()
    glTranslatef(*player_pos)
    glRotatef(player_angle, 0, 0, 1)

    if game_over:
        glRotatef(90, 0, 1, 0)

    # Left foot
    glColor3f(0, 0, 1)
    glTranslatef(0, -40, -100)
    glRotatef(90, 0, 1, 0)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 12, 6, 70, 10, 10)

    # Right foot
    glColor3f(0, 0, 1)
    glTranslatef(0, -90, 0)
    gluCylinder(gluNewQuadric(), 12, 6, 70, 10, 10)

    # Body
    glColor3f(0.4, 0.5, 0)
    glTranslatef(0, 40, -45)
    glutSolidCube(85)

    # Gun
    glColor3f(0.82, 0.82, 0.82)
    glTranslatef(0, 0, 40)
    glTranslatef(40, 0, -90)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 25, 10, 100, 10, 10)

    # Left Hand
    glColor3f(.94, 0.75, 0.62)
    glTranslatef(0, -25, 0)
    gluCylinder(gluNewQuadric(), 15, 6, 60, 10, 10)

    # Right Hand
    glColor3f(.94, 0.75, 0.62)
    glTranslatef(0, 50, 0)
    gluCylinder(gluNewQuadric(), 15, 6, 60, 10, 10)

    # Head
    glColor3f(0, 0, 0)
    glTranslatef(40, -25, -25)
    gluSphere(gluNewQuadric(), 35, 12, 10)

    glPopMatrix()

for i in range(num_of_enemies):   ##starting enemy
    enemies.append(spawn_enemy())


def fire_bullet(fire_pos=None, enemy=None):
    if fire_pos is None:                               # Normal firing mode
        rad = math.radians(player_angle)
        dir_x = -math.cos(rad)
        dir_y = -math.sin(rad)

        gun_length = 150
        gun_right = 75
        gun_up = 12

        bullet_start = [
            player_pos[0] + gun_right * math.sin(rad) + dir_x * gun_length,
            player_pos[1] - gun_right * math.cos(rad) + dir_y * gun_length, 
            player_pos[2] + gun_up
        ]
        bullet_dir = [dir_x, dir_y, 0]
    else:                                                                             # Cheat mode firing
        dx = enemy["enemy_pos"][0] - fire_pos[0]
        dy = enemy["enemy_pos"][1] - fire_pos[1]
        dz = enemy["enemy_pos"][2] - fire_pos[2]
        dist = math.sqrt(dx * dx + dy * dy + dz * dz)
        bullet_dir = [dx / dist, dy / dist, dz / dist]
        bullet_start = fire_pos.copy()

    bullets.append({
        'bullet_pos': bullet_start,
        'dir': bullet_dir
    })
def toggle_camera_mode():
    global camera_mode
    if camera_mode == "third" :
         camera_mode = "first"
    else :
       camera_mode =  "third"
    print(f"Switched to {camera_mode}-person mode")

def mouseListener(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not game_over:
        fire_bullet()  # Normal firing
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN and not game_over:
        toggle_camera_mode()
    glutPostRedisplay()

def toggle_cheat_mode():
    global cheat, gun
    cheat = not cheat
    gun = False


def toggle_automatic_gun():
    global auto_gun_follow, gun
    if camera_mode == "first" and cheat:  
        auto_gun_follow = not auto_gun_follow
        gun = auto_gun_follow
    else:
        auto_gun_follow = False
        gun = False

def move_player(direction):
    global player_pos, cheat_cam_view

    angle = math.radians(player_angle)
    speed = 50 if cheat else 20
    new_x = -math.cos(angle) * speed if direction == 'w' else math.cos(angle) * speed
    new_y = -math.sin(angle) * speed if direction == 'w' else math.sin(angle) * speed

    new_x = player_pos[0] + new_x
    new_y = player_pos[1] + new_y

    if left_bound <= new_x <= right_bound and left_bound <= new_y <= right_bound:
        player_pos[0] = new_x
        player_pos[1] = new_y

        if camera_mode == "first" and cheat and not gun:
            cheat_cam_view[0] += new_x
            cheat_cam_view[1] += new_y
def rotate_player(rotation_direction):
    global player_angle
    angle_step = 4
    player_angle += angle_step if rotation_direction == 'a' else -angle_step

def restart_game():
    global game_over, player_pos, player_angle, life, score, missed_bullets, bullets, enemies

    bullets.clear()
    enemies.clear()
    for i in range(num_of_enemies):
        enemies.append(spawn_enemy())

    score = 0 
    missed_bullets = 0
    life = 6
    game_over = False
    player_pos[:] = [0, 0, 0]
    player_angle = 0
    glutPostRedisplay()

def keyboardListener(key, x, y):
    global cheat
    if not game_over:
        if key == b'w' or key == b's':
            move_player('w' if key == b'w' else 's')
        elif key == b'a' or key == b'd':
            rotate_player('a' if key == b'a' else 'd')
        elif key == b"c":
            toggle_cheat_mode()
        elif key == b"v":
            toggle_automatic_gun()  

    if key == b'r' and game_over:
        restart_game()

def specialKeyListener(key, x, y):
    global camera_pos
    x, y, z = camera_pos
    if not game_over:
        if key == GLUT_KEY_UP:
            y += 1.5
        if key == GLUT_KEY_DOWN:
            y -= 1.5
        if key == GLUT_KEY_RIGHT:
            x += 1.5
        if key == GLUT_KEY_LEFT:
            x -= 1.5
    camera_pos = (x, y, z)

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.2, 2000)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if camera_mode == "third":
        setup_third_person_camera()
    elif camera_mode == "first":
        setup_first_person_camera()


def setup_third_person_camera():
    x, y, z = camera_pos
    gluLookAt(x, y, z, 0, 0, 0, 0, 0, 1)


def setup_first_person_camera():
    global player_angle, auto_gun_follow

    angle = math.radians(player_angle)

    # Base camera position relative to player
    cam_pos = [
        player_pos[0] + 40 * math.sin(angle) - math.cos(angle) * 60,
        player_pos[1] - 40 * math.cos(angle) - math.sin(angle) * 60,
        player_pos[2] + 40
    ]


    if auto_gun_follow:  # Auto-follow the gun
        look_at = [
            cam_pos[0] + (-math.cos(angle)) * 100,
            cam_pos[1] + (-math.sin(angle)) * 100,
            cam_pos[2]
        ]
    else:  # Normal first-person look
        look_at = [
            cam_pos[0] + (-math.cos(angle)) * 100,
            cam_pos[1] + (-math.sin(angle)) * 100,
            cam_pos[2]
        ]

    gluLookAt(*cam_pos, *look_at, 0, 0, 1)


def fight_PE():
    global life, game_over

    player_x, player_y, player_z = player_pos
    any_collision = False

    player_radius = 50     
    enemy_radius = 40      
    for e in enemies:
    
        diff_x = player_x - e['enemy_pos'][0]
        diff_y = player_y - e['enemy_pos'][1]
        dist_sq = diff_x * diff_x + diff_y * diff_y

        if dist_sq > 1:
            inv_dist = 0.05 / math.sqrt(dist_sq)
            e['enemy_pos'][0] += diff_x * inv_dist
            e['enemy_pos'][1] += diff_y * inv_dist

     
        e['scale'] = e['scale'] + e['scale_dir']
        if not 0.8 <= e['scale'] <= 1.2:
            e['scale_dir'] *= -1
            e['scale'] = min(max(e['scale'], 0.8), 1.2)

        # Collision detection 
        dist = math.sqrt((player_x - e['enemy_pos'][0])**2 +
                         (player_y - e['enemy_pos'][1])**2 +
                         (player_z - e['enemy_pos'][2])**2)

        if not any_collision and not game_over and dist < player_radius + enemy_radius:
            life -= 1
            enemies.remove(e)
            enemies.append(spawn_enemy())

            if life <= 0:
                game_over = True
                enemies.clear()
                return

            any_collision = True



def shoot():
    global bullets, missed_bullets, game_over

    for bullet in bullets[:]:
        # Move the bullet
        bullet['bullet_pos'][0] += bullet['dir'][0] * 10
        bullet['bullet_pos'][1] += bullet['dir'][1] * 10
        bullet['bullet_pos'][2] += bullet['dir'][2] * 10

        # Check if out of bounds
        if (abs(bullet['bullet_pos'][0]) > 800 or
                abs(bullet['bullet_pos'][1]) > 800 or
                bullet['bullet_pos'][2] > 800 or
                bullet['bullet_pos'][2] < 0):
            bullets.remove(bullet)
            missed_bullets += 1

    if missed_bullets >= 10 or life == 0:
        game_over = True
        enemies.clear()


def hit_enemy():
    global bullets, score

    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if check_collision(bullet, enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                enemies.append(spawn_enemy())
                score += 1
                break


def check_collision(bullet, enemy):
    bx, by, bz = bullet['bullet_pos']
    ex, ey, ez = enemy['enemy_pos']
    return ((bx - ex) ** 2 + (by - ey) ** 2 + (bz - ez) ** 2) < 2500  # 50 units radius


def cheating():
    global player_angle, cheat_rotation, can_fire

    if not (cheat and not game_over):
        return

    # Auto-rotation
    rotate_speed = 1.5
    player_angle = (player_angle + rotate_speed) % 360
    cheat_rotation += rotate_speed

    if cheat_rotation >= 30:
        cheat_rotation = 0
        can_fire = True

    if not can_fire:
        glutPostRedisplay()
        return

    # Calculate firing position
    rad = math.radians(player_angle)
    fire_pos = [
        player_pos[0] + 40 * math.sin(rad) - math.cos(rad) * 60,
        player_pos[1] - 40 * math.cos(rad) - math.sin(rad) * 60,
        player_pos[2] + 40
    ]

    # Find and shoot at first enemy in firing arc
    for enemy in enemies:
        dx = enemy["enemy_pos"][0] - fire_pos[0]
        dy = enemy["enemy_pos"][1] - fire_pos[1]
        dist_xy = math.hypot(dx, dy)

        if dist_xy == 0:
            continue

        angle_to_enemy = math.atan2(dy, dx)
        angle_diff = abs(((angle_to_enemy - rad) + math.pi) % (2 * math.pi) - math.pi)

        if angle_diff < math.acos(0.998):  
            fire_bullet(fire_pos, enemy)
            can_fire = False
            break

    glutPostRedisplay()




def idle():
    shoot()
    hit_enemy()
    fight_PE()
    cheating()
    glutPostRedisplay()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 700)

    setupCamera()

    draw_grid(GRID_SIZE)
    border_walls()


    if not game_over:
        draw_text(10, 450, f"Player Life Remaining: {life} ")
        draw_text(10, 430, f"Game Score: {score}")
        draw_text(10, 410, f"Player Bullet Missed: {missed_bullets}")
    else:
        draw_text(10, 460, f"Game is Over. Your score now is {score}.")
        draw_text(10, 440, f'Press "R" to RESTART the Game.')

    player()
    draw_bullets()
    for enemy in enemies:
        draw_enemy(enemy)

    glutSwapBuffers()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 700)
    glutInitWindowPosition(150, 0)
    glutCreateWindow(b"Assignment 3 Bullet Frenzy")

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)

    glutMainLoop()
if __name__ == "__main__":
    main()