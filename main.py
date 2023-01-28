import os
import sys
import pygame
import requests
from change_z import change_z


def request(coord, size):
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


def main(coord, size):
    request(coord, size)
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load("map.png"), (0, 0))
    pygame.display.flip()
    run = True
    while run:
        for event in pygame.event.get():
            size = change_z(event, size)
        request(coord, size)
        screen.blit(pygame.image.load("map.png"), (0, 0))
        pygame.display.flip()
    pygame.quit()
    os.remove(map_file)


if __name__ == '__main__':
    coord = input('Введите координаты через пробел: ').split()
    size = input('Введите масштаб карты: ')
    main(coord, size)
