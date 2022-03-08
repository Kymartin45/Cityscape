from flask import Flask, render_template
from dotenv import dotenv_values
from db import connectDb
from random import choice
import urllib.parse
import requests
import json

app = Flask(__name__)

config = dotenv_values('.env')
OPENCAGEDATA_API_KEY = config.get('OPENCAGEDATA_API_KEY')
GEOAPIFY_API_KEY = config.get('GEOAPIFY_API_KEY')
SECRET_KEY = config.get('SECRET_KEY')

POPULATION_THRESHHOLD = 1000000

class City:
    def __init__(self, name, coords):
        self.name = name 
        self.coords = coords 

def getRandomCityName(populationThreshold):
    filteredCities = connectDb.filteredCitiesByPopulation(populationThreshold)
    city = choice(filteredCities)
    return city

def getCityCoordinatesByName(cityName):
    geoUrl = 'https://api.opencagedata.com/geocode/v1/json'
    params = {
        'q': cityName,
        'key': OPENCAGEDATA_API_KEY
    }
    r = requests.get(geoUrl, params=params)
    res = json.loads(r.text)['results'][0]['geometry']
    
    lat = res['lat']
    lon = res['lng']
    
    return (lon, lat)

def getRandomCity():
    cityName = getRandomCityName(POPULATION_THRESHHOLD)
    cityCoords = getCityCoordinatesByName(cityName)
    city = City(cityName, cityCoords)
    print(f'{city.name} : {city.coords}')
    
    return city 

def showMap(city):
    lon, lat = city.coords
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
    fullUrl = f'{url}{urllib.parse.urlencode(params)}'
    
    return fullUrl

@app.route('/', methods=['GET', 'POST'])
def index():
    city = getRandomCity()
    mapOfCity = showMap(city)
    return render_template('index.html', mapOfCity=mapOfCity)
    
if __name__ == '__main__':
    app.secret_key = SECRET_KEY
    app.run(debug=True, port=8000)
    
