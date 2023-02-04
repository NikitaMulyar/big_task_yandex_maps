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


class MapType(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.color = (255, 255, 255)
        self.bg = (100, 100, 100)
        self.pos = (x, y)
        self.font = pygame.font.Font(None, 30)
        self.text = 'Тип карты'
        self.types = ['map', 'sat', 'sat,skl']
        self.ind = 0
        self.rect_ = pygame.rect.Rect(x, y, 100, 20)

    def change_type(self):
        self.ind = (self.ind + 1) % 3

    def curr_type(self):
        return self.types[self.ind]

    def render(self, screen):
        pygame.draw.rect(screen, self.bg, self.rect_)
        screen.blit(self.font.render(self.text, True, self.color), self.pos)


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
        print(geocoder_params)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        return [0, 0]

    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    return [toponym_longitude, toponym_lattitude]


metka = get_coors('Москва')


def request(size, coord, map_type):
    global metka
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={coord[0]},{coord[1]}&l={map_type}&z={size}&pt={metka[0]},{metka[1]},pm2dgm"
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
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    map_type_box = MapType(10, 50)
    size = 10
    coord = get_coors('Москва')
    request(size, coord, map_type_box.curr_type())
    screen.blit(pygame.image.load("map.png"), (0, 0))
    pygame.display.flip()
    run = True
    data = [size, coord[0], coord[1]]
    text_box = TextInputBox(10, 400, (255, 255, 255), (200, 50, 100), 330, 25)
    check_box = TextInputBox(350, 370, (255, 255, 255), (200, 200, 100), 100, 25, text='Искать!')
    check_box2 = TextInputBox(350, 400, (255, 255, 255), (200, 200, 100), 270, 25, text='Сбросить данные')
    while run:
        for event in pygame.event.get():
            global metka
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
                request(data[0], data[1:], map_type_box.curr_type())
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if map_type_box.rect_.collidepoint(*pygame.mouse.get_pos()):
                    map_type_box.change_type()
                    txt = 'Москва' if not text_box.text else text_box.text
                    metka = get_coors(txt)
                    request(data[0], data[1:], map_type_box.curr_type())
                if check_box.rect_.collidepoint(*pygame.mouse.get_pos()):
                    if text_box.text != '':
                        data = [data[0], *get_coors(text_box.text)]
                        metka = get_coors(text_box.text)
                        request(data[0], data[1:], map_type_box.curr_type())
                if check_box2.rect_.collidepoint(*pygame.mouse.get_pos()):
                    metka = get_coors('Москва')
                    text_box.text = ''
                    request(data[0], metka, map_type_box.curr_type())
        screen.blit(pygame.image.load("map.png"), (0, 0))
        text_box.render(screen)
        check_box.render(screen)
        check_box2.render(screen)
        map_type_box.render(screen)
        pygame.display.flip()
    pygame.quit()
    os.remove('map.png')


if __name__ == '__main__':
    main()
