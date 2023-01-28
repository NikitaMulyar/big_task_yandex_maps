import pygame


def change_z():
    pygame.init()
    z = 0
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                z += 1
            elif event.key == pygame.K_DOWN:
                z -= 1
    return z
