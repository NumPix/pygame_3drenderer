import pygame
from pygame.locals import *

from functions import *
from obj_parser import parse_obj

np.set_printoptions(suppress=True)

vertices = []
vertex_normals = []
textures = []
surfaces = []

parse_obj("cat.obj", vertices, vertex_normals, textures, surfaces)

RESOLUTION = WIDTH, HEIGHT = 1920, 1080
PIXEL_SIZE = 1
SIZE = WIDTH * PIXEL_SIZE, HEIGHT * PIXEL_SIZE
ASPECT = WIDTH / HEIGHT

FAR = 100
NEAR = 1
FOV = 100 / 180 * np.pi

ROTATION_SPEED = 0.3
MOVING_SPEED = 40

screen = pygame.display.set_mode(SIZE, DOUBLEBUF, 16)

light = np.array([0, 5, -30])

camera_position = np.array([-500., 0, 0.])
camera_rotation = np.array([0., 0., 0.])

object_position = np.array([0., 100., 0.])
object_rotation = np.array([0., 0., 0.])
object_scaling = np.array([.1, .1, .1])


def draw(scr):
    for face in surfaces:
        p1 = vertices[int(face[0][0]) - 1]
        p2 = vertices[int(face[1][0]) - 1]
        p3 = vertices[int(face[2][0]) - 1]

        draw_triangle(scr, [p1, p2, p3], FAR, NEAR, ASPECT, FOV, object_position, object_rotation,
                      object_scaling, camera_position, camera_rotation)

    pygame.display.flip()


if __name__ == "__main__":

    pygame.init()
    while True:
        pygame.Surface.fill(screen, (0, 0, 0))
        draw(screen)
        print(camera_position)
        for evt in pygame.event.get():
            if evt.type == QUIT:
                pygame.quit()

        if pygame.key.get_pressed()[pygame.K_q]:
            camera_rotation[1] = camera_rotation[1] + ROTATION_SPEED
        elif pygame.key.get_pressed()[pygame.K_e]:
            camera_rotation[1] = camera_rotation[1] - ROTATION_SPEED

        if pygame.key.get_pressed()[pygame.K_w]:
            camera_rotation[2] = camera_rotation[2] + ROTATION_SPEED
        elif pygame.key.get_pressed()[pygame.K_s]:
            camera_rotation[2] = camera_rotation[2] - ROTATION_SPEED

        if pygame.key.get_pressed()[pygame.K_d]:
            camera_rotation[0] = camera_rotation[0] + ROTATION_SPEED
        elif pygame.key.get_pressed()[pygame.K_a]:
            camera_rotation[0] = camera_rotation[0] - ROTATION_SPEED
