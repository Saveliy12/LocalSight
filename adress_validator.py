import requests
import json
from decimal import Decimal
from yandex_geocoder import Client

'''
Yandex API
https://github.com/sivakov512/yandex-geocoder
'''

client = Client("cd0b5a9e-e507-4169-9779-dcba427a8812")

def get_coords(adress: str):
    if str(adress):
        try:
            demical_coordinates = client.coordinates(str(adress))
        except Exception as e:
            print("yandex_geocoder: ", e)
            return None
        if demical_coordinates:
            coords = f'{demical_coordinates[0]},{demical_coordinates[1]}'
            return coords
    else:
        return None


def get_adress(coords: str):
    coords = coords.split(",")
    if coords:
        try:
            address = client.address(Decimal(f"{coords[0]}"), Decimal(f"{coords[1]}"))  
        except Exception as e:
            print("yandex_geocoder: ", e)
            return None
        return address
    else:
        return None


# get_coords("амкм")
# get_adress("48.382816, 54.312585")