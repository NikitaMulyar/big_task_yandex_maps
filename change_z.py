import pygame


def change_z(event, z):
    pygame.init()
    z = int(z)
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_PAGEUP:
            z += 1
        elif event.key == pygame.K_PAGEDOWN:
            z -= 1
    return z
