import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import subprocess

# Definisi verteks-verteks untuk membuat bidang 2D
vertices = (
    (-1, -1),
    (1, -1),
    (1, 1),
    (-1, 1)
)

# Koordinat tekstur untuk masing-masing verteks
tex_coords = [
    (0, 0),
    (1, 0),
    (1, 1),
    (0, 1)
]

# ganti bg 
background_texture = "images/Sakura.jpg"

def load_texture(image):
    texture_surface = pygame.image.load(image)
    texture_data = pygame.image.tostring(texture_surface, "RGB", 1)

    width = texture_surface.get_width()
    height = texture_surface.get_height()

    glEnable(GL_TEXTURE_2D)
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    return texture_id

def draw_background(texture):
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
    for i in range(4):
        glTexCoord2fv(tex_coords[i])
        glVertex2fv(vertices[i])
    glEnd()

def draw_button():
    glBegin(GL_QUADS)
    glVertex2f(0.6, 0.6)
    glVertex2f(0.8, 0.6)
    glVertex2f(0.8, 0.8)
    glVertex2f(0.6, 0.8)
    glEnd()

def main():
    pygame.init()
    display = (1000, 820)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Background Window")

    gluOrtho2D(-1, 1, -1, 1)
    glTranslatef(0.0, 0.0, 0.0)

    background_texture_id = load_texture(background_texture)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Check if the click is within the button area
                if 0.6 <= (mouse_x / 400.0) <= 0.8 and 0.6 <= (1 - mouse_y / 300.0) <= 0.8:
                    # If clicked, close the current window and return to menu_utama.py
                    subprocess.Popen(['python', 'main_menu.py'])
                    pygame.quit()
                    exit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_background(background_texture_id)
        draw_button()

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
