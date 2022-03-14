from main import POPULATION_THRESHHOLD, CityInfo
from dotenv import dotenv_values
import psycopg2.extras


config = dotenv_values('.env')
POSTGRESQL_PASSWORD = config.get('POSTGRESQL_PASSWORD')
POSTGRES_HOST = config.get('POSTGRES_HOST')
POSTGRESQL_USERNAME = config.get('POSTGRESQL_USERNAME')

CONN = psycopg2.connect(
    host=POSTGRES_HOST,
    database='postgres',
    user=POSTGRESQL_USERNAME,
    password=POSTGRESQL_PASSWORD
)

def getCitiesByPopulation(populationThreshold):
    cur = CONN.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute(''' 
                    SELECT city, country, lng, lat, city_id FROM worldwidecities
                    WHERE population >= %s
                    ORDER BY random() LIMIT 1;  
                ''', [populationThreshold])

    city = cur.fetchall()
    for col in city:
        city, country, lng, lat, cityId = col['city'], col['country'], col['lng'], col['lat'], col['city_id']
    
    cityInfo = CityInfo(city, (lng, lat), country, cityId)
        
    CONN.commit()
    CONN.close()

    return cityInfo

def checkAnswer(cityId): 
    cur = CONN.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    cur.execute('''
                    SELECT country FROM worldwidecities
                    WHERE city_id = %s;
                    ''', [cityId])
    
    correctAns = cur.fetchall()
    for col in correctAns:
        country = col['country']

    ans = country

    CONN.commit()
    CONN.close()

    return ans

if __name__ == '__main__':
    getCitiesByPopulation(POPULATION_THRESHHOLD)

    