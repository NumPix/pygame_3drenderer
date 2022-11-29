import numpy as np
from numpy import sin, cos, tan
import pygame


def clamp(value, min_v, max_v):
    return min(max(value, min_v), max_v)


def ctg(x):
    return 1 / tan(x)


def projection_matrix(far, near, aspect, fov):
    return np.array([
        [ctg(fov * 0.5) / aspect, 0, 0, 0],
        [0, ctg(fov * 0.5), 0, 0],
        [0, 0, (far + near) / (far - near), 1],
        [0, 0, -2 * far * near / (far - near), 0]
    ])


def translation_matrix(x, y, z):
    return np.array([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ])


def rotation_matrix(a, b, y):
    return np.array([
        [cos(b) * cos(y), -sin(y) * cos(b), sin(b), 0],
        [sin(a) * sin(b) * cos(y) + sin(y) * cos(a), -sin(a) * sin(b) * sin(y) + cos(a) * cos(y), -sin(a) * cos(b), 0],
        [sin(a) * sin(y) - sin(b) * cos(a) * cos(y), sin(a) * cos(y) + sin(b) * sin(y) * cos(a), cos(a) * cos(b), 0],
        [0, 0, 0, 1]
    ])


def scaling_matrix(x, y, z):
    return np.array([
        [x, 0, 0, 0],
        [0, y, 0, 0],
        [0, 0, z, 0],
        [0, 0, 0, 1]
    ])


def model_matrix(position, rotation, scaling):
    return np.matmul(np.matmul(translation_matrix(*position), rotation_matrix(*rotation)), scaling_matrix(*scaling))


def view_matrix(position, rotation):
    return np.linalg.inv(np.matmul(translation_matrix(*position), rotation_matrix(*rotation)))


def dekart_to_homogeneous(point):
    return np.array([point[0], point[1], point[2], 1])


def homogeneous_to_dekart(point):
    return (point / point[3])[:3]


def project_point(point, far, near, aspect, fov, world_position, world_rotation, world_scaling, camera_position,
                  camera_rotation):
    p = dekart_to_homogeneous(point)
    model = model_matrix(world_position, world_rotation, world_scaling)
    m1 = np.matmul(p, model)
    view = view_matrix(camera_position, camera_rotation)
    m2 = np.matmul(m1, view)
    projection = projection_matrix(far, near, aspect, fov)
    m3 = np.matmul(m2, projection)
    print(p, m1, m2, m3, sep='\n')
    print('\n\n')
    return homogeneous_to_dekart(m3)


def normal_by_point_normals(normals):
    n1, n2, n3 = normals
    return np.array(n1) + np.array(n2) + np.array(n3)


def normal_by_3_points(p1, p2, p3):
    v1 = np.array(p1)
    v2 = np.array(p2)
    v3 = np.array(p3)
    ab = v1 - v2
    ac = v3 - v2
    return np.cross(ab, ac)


def draw_triangle(screen, points, far, near, aspect, fov, world_position, world_rotation, world_scaling,
                  camera_position, camera_rotation):
    p1, p2, p3 = points

    p1 = project_point(p1, far, near, aspect, fov, world_position, world_rotation, world_scaling, camera_position,
                       camera_rotation)
    p2 = project_point(p2, far, near, aspect, fov, world_position, world_rotation, world_scaling, camera_position,
                       camera_rotation)
    p3 = project_point(p3, far, near, aspect, fov, world_position, world_rotation, world_scaling, camera_position,
                       camera_rotation)

    pygame.draw.polygon(screen, (255, 255, 255), [p1.tolist()[:2], p2.tolist()[:2], p3.tolist()[:2]])
