import pygame


def change_z(event, z):
    pygame.init()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            z += 1
        elif event.key == pygame.K_DOWN:
            z -= 1
    return z
