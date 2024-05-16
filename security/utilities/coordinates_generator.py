import pycristoforo as pyc
import random
import string
from shapely.geometry import Polygon


#   Este módulo hace que demore en cargar manage.py


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


#   country = pyc.get_shape("Italy")

def get_points():
    city = Polygon([(-33.589250348502624, -70.8224464358841), (-33.36740257983577, -70.76488963175699),
                    (-33.596472516594396, -70.5506150033027), (-33.37710774471859, -70.51380419061522)])

    country = pyc.get_shape("Chile")

    points = pyc.geoloc_generation(country, 150, "Chile")

    coord = []

    for p in points:
        lat = (p['geometry']['coordinates'])[1]
        lon = (p['geometry']['coordinates'])[0]
        name = get_random_string(8)
        point = []
        point = [round(lat, 2), round(lon, 2), 4]
        coord.append(point)

    return coord
