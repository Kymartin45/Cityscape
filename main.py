from flask import Flask, jsonify, make_response, render_template, request
from dotenv import dotenv_values
from db.queries import query
from db import connectDb
import urllib.parse
import requests
import json

app = Flask(__name__)

config = dotenv_values('.env')
OPENCAGEDATA_API_KEY = config.get('OPENCAGEDATA_API_KEY')
GEOAPIFY_API_KEY = config.get('GEOAPIFY_API_KEY')
SECRET_KEY = config.get('SECRET_KEY')

POPULATION_THRESHHOLD = 1000000

class CityInfo:
    def __init__(self, name, coords, country, cityId):
        self.name = name 
        self.coords = coords 
        self.country = country
        self.cityId = cityId

def getRandomCityName(populationThreshold):
    city = connectDb.getCitiesByPopulation(populationThreshold)

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
    cityInfo = getRandomCityName(POPULATION_THRESHHOLD)
    
    return cityInfo

def showMap(cityInfo):
    lon, lat = cityInfo.coords
    url = 'https://maps.geoapify.com/v1/staticmap?'
    params = {
        'style': 'klokantech-basic',
        'scaleFactor': 2,
        'width': '800',  
        'height': '600',
        'center': f'lonlat:{lon},{lat}',
        'zoom': '8',
        'marker': f'lonlat:{lon},{lat};color:#ff0000;size:medium',
        'apiKey': GEOAPIFY_API_KEY
    }    
    fullUrl = f'{url}{urllib.parse.urlencode(params)}'
    
    return fullUrl

@app.route('/', methods=['GET', 'POST'])
def index():
    city = getRandomCity()
    mapOfCity = showMap(city)
    cityId = city.cityId

    return render_template('index.html', mapOfCity=mapOfCity, cityId=cityId, GEOAPIFY_API_KEY=GEOAPIFY_API_KEY)

@app.route('/guess', endpoint='guess', methods=['POST'])
def getCountryByCityID(): 
    req = request.get_json()
    guessObj = dict(req)

    visitorId = guessObj['visitorId']

    cur = connectDb.CONN.cursor()
    isCorrect =  str(req['attempt']).strip().lower() == connectDb.checkAnswer(req['cityId'])

    cur.execute(query['checkIfIdExists'], [visitorId])

    if not cur.fetchone()[0]:
        cur.execute(query['createUser'])

    if isCorrect:
        cur.execute(query['updateStatsIfCorrect'], [visitorId])
    
    cur.execute(query['updateStatsIfIncorrect'], [visitorId])

    connectDb.CONN.commit()

    return make_response(jsonify(isCorrect), 200)

@app.route('/leaderboard', methods=['GET'])
def getGlobalStats():
    cur = connectDb.CONN.cursor()

    cur.execute(query['showGlobalStats'])
    globalUserStats = cur.fetchall()

    allStats = []
    for row in globalUserStats:
        totalUserStats = {
            'gamesPlayed': row[0],
            'gamesWon': row[1],
        }
    
        allStats.append(totalUserStats)
        showUserStats = {
            'totalPlayers': len(globalUserStats),
            'leaderboard': allStats,
        }

    return make_response(jsonify(showUserStats), 200)

if __name__ == '__main__':
    app.secret_key = SECRET_KEY
    app.run(debug=True, port=8000)
    
