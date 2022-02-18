from dotenv import dotenv_values
from random import choice
import urllib.parse
import webbrowser
import requests
import json

config = dotenv_values('.env')
OPENCAGEDATA_API_KEY = config.get('OPENCAGEDATA_API_KEY')
GEOAPIFY_API_KEY = config.get('GEOAPIFY_API_KEY')

def randomCity():
    with open('city_data/worldCities.json', 'r', encoding='UTF-8') as r:
        data = json.loads(r.read())
        rand_city = choice(data)
        
        randomCity.city = str(rand_city['city']).replace('"', '')
        print(f"\n{randomCity.city}'s population is {rand_city['population']}\n")
        print(f"Country: {rand_city['country']}\n\nState/Region/Province: {rand_city['admin_name']}")

def searchCity():
    geo_url = 'https://api.opencagedata.com/geocode/v1/json'
    params = {
        'q': randomCity.city,
        'key': OPENCAGEDATA_API_KEY
    }
    r = requests.get(geo_url, params=params)
    res = json.loads(r.text)
    
    searchCity.lat = res['results'][0]['geometry']['lat']
    searchCity.lon = res['results'][0]['geometry']['lng']
    
    with open('city_data/testData.json', 'w', encoding='UTF-8') as f:
        json.dump(res, f, ensure_ascii=False, indent=4)

def showMap():
    url = 'https://maps.geoapify.com/v1/staticmap?'
    params = {
        'style': 'osm-bright',
        'width': '1920',  
        'height': '1080',
        'center': f'lonlat:{searchCity.lon},{searchCity.lat}',
        'zoom': '6.5',
        'marker': f'lonlat:{searchCity.lon},{searchCity.lat};color:#ff0000;size:medium',
        'apiKey': GEOAPIFY_API_KEY
    }    
    full_url = f'{url}{urllib.parse.urlencode(params)}'
    webbrowser.open(full_url)
    
if __name__ == '__main__':
    randomCity()
    searchCity()
    showMap()
        
