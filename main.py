import os
import pygame
import requests
from change_z import change_z
from consts import *


class TextInputBox(pygame.sprite.Sprite):
    def __init__(self, x, y, clr, bg, w, h, text=''):
        super().__init__()
        self.color = clr
        self.bg = bg
        self.pos = (x, y)
        self.font = pygame.font.Font(None, 40)
        self.text = text
        self.rect_ = pygame.rect.Rect(x, y, w, h)

    def render(self, screen):
        screen.blit(self.font.render(self.text, True, self.color, self.bg), self.pos)
        pygame.draw.rect(screen, self.color, self.rect_.inflate(5, 5), 2)


def get_coors(name):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": name,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        print("Ошибка выполнения запроса:")
        print(geocoder_api_server)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        return [0, 0]

    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    return [toponym_longitude, toponym_lattitude]


def request(size, coord):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={coord[0]},{coord[1]}&l=map&z={size}"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        return

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)


def main():
    size = 10
    coord = get_coors('Москва')
    request(size, coord)
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load("map.png"), (0, 0))
    pygame.display.flip()
    run = True
    data = [size, coord[0], coord[1]]
    text_box = TextInputBox(10, 400, (255, 255, 255), (200, 50, 100), 350, 40)
    check_box = TextInputBox(400, 400, (255, 255, 255), (200, 200, 100), 150, 40, text='Искать!')
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                """if event.key == pygame.K_RETURN:
                    if text_box.text != '':
                        request(data[0], text_box.text)"""
                if event.key == pygame.K_BACKSPACE:
                    text_box.text = text_box.text[:-1]
                else:
                    if event.unicode in TO_RUS:
                        text_box.text += TO_RUS[event.unicode]
                    elif event.unicode in TO_RUS_BIG:
                        text_box.text += TO_RUS_BIG[event.unicode]
                    else:
                        text_box.text += event.unicode
                data = list(change_z(event, *data))
                request(data[0], data[1:])
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if check_box.rect_.colliderect(pygame.rect.Rect(*pygame.mouse.get_pos(), 5, 5)):
                    if text_box.text != '':
                        data = [data[0], *get_coors(text_box.text)]
                        request(data[0], data[1:])
        screen.blit(pygame.image.load("map.png"), (0, 0))
        text_box.render(screen)
        check_box.render(screen)
        pygame.display.flip()
    pygame.quit()
    os.remove("map.png")


if __name__ == '__main__':
    main()
