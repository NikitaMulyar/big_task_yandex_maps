import pygame
from consts import *
import requests


def find_object(z, x, y, pos):
    pygame.init()
    x = float(x)
    y = float(y)
    CONST_X = 4.56555 * 2 ** (z - 2.678)
    CONST_Y = 8 * 2 ** (z - 2.6675)
    obj_x = x + pos[0] / CONST_X - 300 / CONST_X
    obj_y = y - pos[1] / CONST_Y + 225 / CONST_Y
    return z, x, y, (obj_x, obj_y)


def get_org_name(x, y, name):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

    crs = [str(x), str(y)]
    if type(crs) == str:
        address_ll = crs
    else:
        address_ll = ",".join([i.strip(',') for i in crs])

    search_params = {
        "apikey": api_key,
        "text": name,
        "lang": "ru_RU",
        "type": "biz"
    }
    response = requests.get(search_api_server, params=search_params)
    if not response:
        print(1)
        return None, None

    json_response = response.json()
    for organization in json_response["features"]:
        try:
            org_name = organization["properties"]["name"]
            point = organization["geometry"]["coordinates"]
            org_point = "{0},{1}".format(point[0], point[1])
            # print(lonlat_distance((x, y), (float(point[0]), float(point[1]))))
            if lonlat_distance((x, y), (float(point[0]), float(point[1]))) <= 50:
                return org_name, org_point
        except Exception:
            continue
    return None, None


def find_org(z, x, y, pos):
    pygame.init()
    x = float(x)
    y = float(y)
    CONST_X = 4.56555 * 2 ** (z - 2.678)
    CONST_Y = 8 * 2 ** (z - 2.6675)
    obj_x = x + pos[0] / CONST_X - 300 / CONST_X
    obj_y = y - pos[1] / CONST_Y + 225 / CONST_Y
    return get_org_name(obj_x, obj_y, get_toponym((obj_x, obj_y))[0])
