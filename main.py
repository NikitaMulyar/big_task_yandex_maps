import os
import pygame
import requests
from up_down_map import up_down_map


def request(coord, spn):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={coord[0]},{coord[1]}&l=map&spn={spn},{spn}"
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
    request(coord, size)
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load("map.png"), (0, 0))
    pygame.display.flip()
    run = True
    data = [size, coord[0], coord[1]]
    while run:
        for event in pygame.event.get():
            data = list(up_down_map(event, *data))
            print(data)
        request(data[1:], data[0])
        screen.blit(pygame.image.load("map.png"), (0, 0))
        pygame.display.flip()
    pygame.quit()
    os.remove("map.png")


if __name__ == '__main__':
    coord = input('Введите координаты через пробел (широта, долгота): ').split()[::-1]
    spn = input('Введите масштаб карты (от 0 до 17): ')
    main(coord, spn)
