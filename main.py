import os
import sys
import pygame
import requests


def main(coord, size):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={coord[1]},{coord[0]}&l=map&z={size}"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
    os.remove(map_file)


if __name__ == '__main__':
    coord = input('Введите координаты через пробел: ').split()
    size = input('Введите масштаб карты: ')
    main(coord, size)
