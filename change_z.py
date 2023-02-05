import pygame


def change_z(event, z, x, y):
    pygame.init()
    z = int(z)
    x = float(x)
    y = float(y)
    CONST_X = 4.56555 * 2 ** (z - 2.678)
    CONST_Y = 8 * 2 ** (z - 2.6675)
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_PAGEUP:
            if z < 16:
                z += 1
        elif event.key == pygame.K_PAGEDOWN:
            if z > 2:
                z -= 1
        if event.key == pygame.K_UP:
            y += 450 / CONST_Y
        elif event.key == pygame.K_RIGHT:
            x += 600 / CONST_X
        elif event.key == pygame.K_DOWN:
            y -= 450 / CONST_Y
        elif event.key == pygame.K_LEFT:
            x -= 600 / CONST_X
    global metka
    if x > 180:
        x = - (180 - x % 180)
    if x < -180:
        x = abs(x) % 180
    if y > 90:
        y = - (90 - y % 90)
    if y < -90:
        y = 90 - abs(y) % 90
    metka = [x, y]
    return z, x, y
