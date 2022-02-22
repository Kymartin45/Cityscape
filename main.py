from dotenv import dotenv_values
from random import choice
import urllib.parse
import webbrowser
import requests
import json

config = dotenv_values('.env')
OPENCAGEDATA_API_KEY = config.get('OPENCAGEDATA_API_KEY')
GEOAPIFY_API_KEY = config.get('GEOAPIFY_API_KEY')

def getRandomCityName():
    with open('city_data/worldCities.json', 'r', encoding='UTF-8') as r:
        data = json.loads(r.read())
        rand_city = choice(data)
        
        city = str(rand_city['city']).replace('"', '')
        print(f"\n{city}'s population is {rand_city['population']}\n")
        print(f"Country: {rand_city['country']}\n\nState/Region/Province: {rand_city['admin_name']}")
        
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
    
    with open('city_data/testData.json', 'w', encoding='UTF-8') as f:
        json.dump(res, f, ensure_ascii=False, indent=4)
    
    return (lon, lat)

def getRandomCity():
    cityName = getRandomCityName()
    cityCoords = getCityCoordinatesByName(cityName)
    return {
        'name': cityName,
        'coordinates': cityCoords,
    }

def showMap(cityCoords):
    cityLon, cityLat = cityCoords['coordinates'][0], cityCoords['coordinates'][1]
    url = 'https://maps.geoapify.com/v1/staticmap?'
    params = {
        'style': 'osm-bright',
        'width': '1920',  
        'height': '1080',
        'center': f'lonlat:{cityLon},{cityLat}',
        'zoom': '6.5',
        'marker': f'lonlat:{cityLon},{cityLat};color:#ff0000;size:medium',
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
        
