import os
import pygame
import requests
from change_z import change_z
from change_coors import *
from consts import *


class TextInputBox(pygame.sprite.Sprite):
    def __init__(self, x, y, clr, bg, w, h, size, text=''):
        super().__init__()
        self.color = clr
        self.bg = bg
        self.pos = (x, y)
        self.font = pygame.font.Font(None, size)
        self.text = text
        self.rect_ = pygame.rect.Rect(x, y, w, h)

    def render(self, screen):
        screen.blit(self.font.render(self.text, True, self.color, self.bg), self.pos)
        pygame.draw.rect(screen, self.color, self.rect_.inflate(5, 5), 2)


class IndexBox(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.color = (255, 255, 255)
        self.bg = (200, 0, 0)
        self.pos = (x, y)
        self.font = pygame.font.Font(None, 30)
        self.text = 'ind'
        self.rect_ = pygame.rect.Rect(x, y, 30, 30)

    def on_off(self):
        return self.bg == (0, 200, 0)

    def change_clr(self):
        if self.bg == (200, 0, 0):
            self.bg = (0, 200, 0)
        else:
            self.bg = (200, 0, 0)

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
        return [None, None], '', ''

    try:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        adrs = toponym['metaDataProperty']['GeocoderMetaData']['AddressDetails']['Country'][
            'AddressLine']
        index = toponym['metaDataProperty']['GeocoderMetaData']['Address'].get('postal_code', '')
        toponym_coodrinates = toponym["Point"]["pos"]
        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    except Exception:
        index = ''
        adrs = ''
        toponym_longitude, toponym_lattitude = [None, None]
    return [toponym_longitude, toponym_lattitude], adrs, index


def request(size, coord, pt=None, pt2=None):
    pts = []
    if pt is not None:
        pts.append(f"{pt[0]},{pt[1]},pm2dbm")
    if pt2 is not None:
        pts.append(f"{pt2},pm2rdm")
    if pt is None and pt2 is None:
        pts.append(f"{coord[0]},{coord[1]},pm2dgm")
    pts = "pt=" + "~".join(pts)
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={coord[0]},{coord[1]}&l=map&z={size}&{pts}"
    response = requests.get(map_request)

    if not response:
        return

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)


def main():
    size = 10
    coord = get_coors('Москва')[0]
    request(size, coord)
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load("map.png"), (0, 0))
    pygame.display.flip()
    run = True
    data = [size, coord[0], coord[1]]
    text_box = TextInputBox(10, 400, (255, 255, 255), (200, 50, 100), 350, 40, 40)
    check_box = TextInputBox(400, 400, (255, 255, 255), (200, 200, 100), 150, 40, 40, text='Искать!')
    address_box = TextInputBox(10, 10, (255, 255, 255), (0, 50, 100), 540, 20, 20)
    index_box = IndexBox(560, 10)
    data2 = [None]  # z, x, y, (obj_x, obj_y)
    data3 = [None]  # org_name, org_point
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
                request(data[0], data[1:], pt=data2[-1], pt2=data3[-1])
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if index_box.rect_.collidepoint(*pos):
                    index_box.change_clr()
                    if text_box.text != '':
                        if data2[0] is None:
                            res = get_coors(text_box.text)
                        else:
                            res = get_coors(get_toponym(data2[-1]))
                        if res[0][0] is None:
                            continue
                        if index_box.on_off():
                            address_box.text = res[2] + ' ' + res[1]
                        else:
                            address_box.text = res[1]
                elif check_box.rect_.collidepoint(*pos):
                    if text_box.text != '':
                        res = get_coors(text_box.text)
                        if res[0][0] is None:
                            continue
                        data2 = [None]
                        data3 = [None]
                        data = [data[0], *res[0]]
                        request(data[0], data[1:], pt=data2[-1], pt2=data3[-1])
                        if index_box.on_off():
                            address_box.text = res[2] + ' ' + res[1]
                        else:
                            address_box.text = res[1]
                elif event.button == 1:
                    data2 = list(find_object(*data, pos))
                    data3 = [None]
                    request(data2[0], data2[1:3], pt=data2[-1], pt2=data3[-1])
                    tmp = get_toponym(data2[3])
                    if index_box.on_off():
                        address_box.text = tmp[1] + ' ' + tmp[0]
                    else:
                        address_box.text = tmp[0]
                elif event.button == 3:
                    data3 = list(find_org(*data, pos))
                    data2 = [None]
                    if data3[0] != '':
                        request(data[0], data[1:3], pt=data2[-1], pt2=data3[-1])
                        address_box.text = data3[0]
        screen.blit(pygame.image.load("map.png"), (0, 0))
        text_box.render(screen)
        check_box.render(screen)
        address_box.render(screen)
        index_box.render(screen)
        pygame.display.flip()
    pygame.quit()
    os.remove("map.png")


if __name__ == '__main__':
    main()
