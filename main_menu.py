import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import subprocess
import sys

# Definisi verteks-verteks untuk membuat kubus 3D
verticies = (
    (0.6, 0.2, 0.2),   # 0
    (-0.6, 0.2, 0.2),  # 1
    (-0.6, -0.2, 0.2),  # 2
    (0.6, -0.2, 0.2),  # 3
    (0.6, 0.2, -0.2),  # 4
    (-0.6, 0.2, -0.2),  # 5
    (-0.6, -0.2, -0.2),  # 6
    (0.6, -0.2, -0.2),  # 7
)

# Definisi permukaan (surfaces) kubus
surfaces = (
    (0, 1, 2, 3),  # surface 0
    (4, 5, 6, 7),  # surface 1
    (0, 3, 7, 4),  # surface 2
    (1, 2, 6, 5),  # surface 3
    (0, 1, 5, 4),  # surface 4
    (3, 2, 6, 7),  # surface 5
)

# Normal vektor untuk masing-masing permukaan kubus
normals = [
    (0, 0, -1),  # surface 0
    (0, 0, 1),   # surface 1
    (-1, 0, 0),  # surface 2
    (1, 0, 0),   # surface 3
    (0, -1, 0),  # surface 4
    (0, 1, 0)    # surface 5
]

# Koordinat tekstur untuk masing-masing verteks
coords = [
    (0, 0), #0
    (1, 0), #1
    (1, 1), #2
    (0, 1) #3
]

display = (1000, 820)
WHITE = (255, 255, 255)
Start = "images/play_button.png"
How_to_play = "images/Bantuan_button.png"
Quit = "images/quit_button.png"
Background = "images/Sakura.jpg"
Logo = "images/logo.png"

def cube(texture):
    glBindTexture(GL_TEXTURE_2D, texture)                   # mengikat ID tekstur yang akan digunakan saat menggambar kubus dengan tekstur.
    glBegin(GL_QUADS)                                       # Memulai menggambar dengan jenis poligon GL_QUADS
    for i_surface, surface in enumerate(surfaces):          # Loop melalui permukaan (surfaces) kubus
        glNormal3fv(normals[i_surface])                     # Mengatur vektor normal untuk permukaan saat ini
        for vertex in surface:                              # Loop melalui verteks-verteks dalam permukaan saat ini
            glTexCoord2fv(coords[surface.index(vertex)])    # Mengatur koordinat tekstur untuk verteks saat ini
            glVertex3fv(verticies[vertex])                  # Menggambar verteks dalam koordinat 3D
    glEnd()
    
# Load the texture
def load_texture(image):
    textureSurface = pygame.image.load(image)                                                # Memuat gambar tekstur dari file 'texture_mipmap.png'
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)                                          # Mengambil data tekstur sebagai string dengan format RGBA

    # Mendapatkan lebar dan tinggi tekstur
    width = textureSurface.get_width()
    height = textureSurface.get_height()

    glEnable(GL_TEXTURE_2D)                                                                                 # Mengaktifkan penggunaan tekstur dalam mode OpenGL
    textureId = glGenTextures(1)                                                                            # Membuat ID tekstur
    glBindTexture(GL_TEXTURE_2D, textureId)                                                                 # mengikat ID tekstur yang baru dibuat (textureId) ke target GL_TEXTURE_2D.
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)       # Mengisi data tekstur ke dalam buffer OpenGL
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)  # Pengaturan filter magnifikasi
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)  # Pengaturan filter minifikasi
    return textureId

def draw_plane(texture):
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(-1.6, -1, 0)
    glTexCoord2f(1, 0)
    glVertex3f(1.6, -1, 0)
    glTexCoord2f(1, 1)
    glVertex3f(1.6, 1, 0)
    glTexCoord2f(0, 1)
    glVertex3f(-1.6, 1, 0)
    glEnd()
    
    
def play_action():
    # Menjalankan permainan.py secara asynchronous
    subprocess.Popen(["python", "permainan.py"])
    
    # Menutup jendela Pygame
    pygame.quit()
    
    # Keluar dari program
    sys.exit()
    
    
def how_to_play_action():
    # Menjalankan permainan.py secara asynchronous
    subprocess.Popen(["python", "howToPlay.py"])
    
    # Menutup jendela Pygame
    pygame.quit()
    
    # Keluar dari program
    sys.exit()
    
    
def quit_action():
    pygame.quit()
    sys.exit()
    
def show(Texture1, Texture2, Texture3, Texture4, Texture5):                  
    glPushMatrix()
    cube(Texture1)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0,0.75,0)
    glScalef(1.2,1,1)
    cube(Texture2)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0,1.5,0)
    cube(Texture3)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-1,0,-0.5)
    glScalef(3,3,1)
    glRotatef(180,0,0,1)
    draw_plane(Texture4)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.1,-1,0)
    glScalef(0.7,0.5,0.5)
    glRotatef(180,0,0,1)
    draw_plane(Texture5)
    glPopMatrix()
    
def main_menu():
    material_ambient = (0.1, 0.1, 0.1, 1.0)  # Sifat ambient material
    material_diffuse = (0.7, 0.7, 0.7, 1.0)  # Sifat diffuse material
    material_specular = (0.5, 0.5, 0.5, 1)  # Sifat specular material

    pygame.init()  # Inisialisasi modul Pygame
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)  # Membuat jendela OpenGL
    pygame.display.set_caption("Sakura Goban")  # Menetapkan judul jendela
    # Add this at the beginning of your script
    pygame.mixer.init()
    pygame.mixer.music.load('musik/Sakura_music.mp3')
    pygame.mixer.music.play(-1)  # The '-1' means the music will loop indefinitely

    glEnable(GL_DEPTH_TEST)  # Mengaktifkan uji kedalaman
    glEnable(GL_COLOR_MATERIAL)  # Mengaktifkan bahan warna
    glEnable(GL_LIGHTING)  # Mengaktifkan pencahayaan
    glEnable(GL_LIGHT0)  # Mengaktifkan cahaya 0
    glEnable(GL_BLEND)  # Mengaktifkan blending
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Mengatur properti material
    glMaterialfv(GL_FRONT, GL_AMBIENT, material_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)  # Mengatur perspektif
    glTranslatef(0.0, 0.0, -5.0)  # Menggeser objek dalam sumbu Z negatif
    glRotatef(180,1,0,0)
    glRotatef(180,0,1,0)
    glLightfv(GL_LIGHT0, GL_POSITION, (-1, 1, 1, 0))  # Mengatur posisi cahaya

    # Memuat tekstur
    start = load_texture(Start)
    how_to_play = load_texture(How_to_play)
    exit_ = load_texture(Quit)
    background =  load_texture(Background)
    logo =  load_texture(Logo)
    # Define the area for interaction
    play_area = pygame.Rect(300, 400, 200, 100)  # (x, y, width, height)
    bantuan_area = pygame.Rect(300, 600, 300, 100)  # (x, y, width, height)
    quit_area = pygame.Rect(300, 700, 200, 100)  # (x, y, width, height)

    while True:
        pygame.event.pump()  # Menjalankan pompa event untuk meningkatkan responsivitas
        for event in pygame.event.get():
            if event.type == QUIT:
                quit_action()
            elif event.type == MOUSEBUTTONDOWN:
                # Get the mouse position when a mouse button is clicked
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print(f"Mouse Clicked at Position: ({mouse_x}, {mouse_y})")
                            # Check if the click is within the interaction area
                if play_area.collidepoint(mouse_x, mouse_y):
                    play_action()
                if bantuan_area.collidepoint(mouse_x, mouse_y):
                    how_to_play_action()
                if quit_area.collidepoint(mouse_x, mouse_y):
                    quit_action()
                    
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Menghapus buffer warna dan kedalaman
        show(start, how_to_play, exit_, background, logo)  # Menampilkan objek kubus dengan tekstur
        pygame.display.flip()  # Memperbarui tampilan
        pygame.time.wait(10)  # Menunggu 10 milidetik

if __name__ == "__main__":
    main_menu()