import os
import pygame
import requests
from change_z import change_z


def request(size, coord1, coord2):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={coord1},{coord2}&l=map&z={size}"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        return

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)


def main(coord, size):
    request(size, *coord)
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load("map.png"), (0, 0))
    pygame.display.flip()
    run = True
    data = [size, coord[0], coord[1]]
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            data = list(change_z(event, *data))
        request(*data)
        screen.blit(pygame.image.load("map.png"), (0, 0))
        pygame.display.flip()
    pygame.quit()
    os.remove("map.png")


if __name__ == '__main__':
    coord = input('Введите координаты через пробел (долгота, широта): ').split()
    size = input('Введите масштаб карты: ')
    main(coord, size)
