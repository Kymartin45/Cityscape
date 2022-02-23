from dotenv import dotenv_values
from random import choice
import urllib.parse
import webbrowser
import requests
import json

config = dotenv_values('.env')
OPENCAGEDATA_API_KEY = config.get('OPENCAGEDATA_API_KEY')
GEOAPIFY_API_KEY = config.get('GEOAPIFY_API_KEY')

class City:
    def __init__(self, name, coords):
        self.name = name 
        self.coords = coords 

def getRandomCityName():
    with open('city_data/worldCities.json', 'r', encoding='UTF-8') as r:
        data = json.loads(r.read())
        rand_city = choice(data)
        
        city = str(rand_city['city']).replace('"', '')
        return city 

def getCityCoordinatesByName(cityName):
    geo_url = 'https://api.opencagedata.com/geocode/v1/json'
    params = {
        'q': cityName,
        'key': OPENCAGEDATA_API_KEY
    }
    r = requests.get(geo_url, params=params)
    res = json.loads(r.text)['results'][0]['geometry']
    
    lat = res['lat']
    lon = res['lng']
    
    # with open('city_data/testData.json', 'w', encoding='UTF-8') as f:
    #     json.dump(res, f, ensure_ascii=False, indent=4)
    return (lon, lat)

def getRandomCity():
    cityName = getRandomCityName()
    cityCoords = getCityCoordinatesByName(cityName)
    cityObj = City(cityName, cityCoords)
    print(f'{cityObj.name} : {cityObj.coords}')
    
    return {
        'name': cityObj.name,
        'coordinates': cityObj.coords,
    }

def showMap(cityObj):
    city = { 'coordinates': cityObj['coordinates'] }
    lon, lat = city.get('coordinates')
    url = 'https://maps.geoapify.com/v1/staticmap?'
    params = {
        'style': 'osm-bright',
        'width': '1920',  
        'height': '1080',
        'center': f'lonlat:{lon},{lat}',
        'zoom': '6.5',
        'marker': f'lonlat:{lon},{lat};color:#ff0000;size:medium',
        'apiKey': GEOAPIFY_API_KEY
    }    
    full_url = f'{url}{urllib.parse.urlencode(params)}'
    webbrowser.open(full_url)
    
if __name__ == '__main__':
    city1 = getRandomCity()
    city2 = getRandomCity()
    city3 = getRandomCity()
    city4 = getRandomCity()
    showMap(city1)
    print(f'\nLoading {city1["name"]}!')
    
