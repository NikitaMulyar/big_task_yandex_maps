import pygame


def up_down_map(event, spn, x, y):
    pygame.init()
    spn = float(spn)
    x = float(x)
    y = float(y)
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            y += spn
        elif event.key == pygame.K_RIGHT:
            x += spn
        elif event.key == pygame.K_DOWN:
            y -= spn
        elif event.key == pygame.K_LEFT:
            x -= spn
        if event.key == pygame.K_PAGEUP:
            spn -= 1
        elif event.key == pygame.K_PAGEDOWN:
            spn += 1
    return spn, x, y
