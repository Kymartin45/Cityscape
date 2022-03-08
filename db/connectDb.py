from main import POPULATION_THRESHHOLD
from dotenv import dotenv_values
import psycopg2

config = dotenv_values('.env')
POSTGRESQL_PASSWORD = config.get('POSTGRESQL_PASSWORD')
POSTGRES_HOST = config.get('POSTGRES_HOST')

CONN = psycopg2.connect(
    host=POSTGRES_HOST,
    database='postgres',
    user='postgres',
    password=POSTGRESQL_PASSWORD
)

def filteredCitiesByPopulation(populationThreshold):
    cur = CONN.cursor()
    cur.execute(''' 
                    SELECT city, population FROM worldwidecities
                    WHERE population >= %s
                    ORDER BY population DESC; ''', [populationThreshold])
    filteredCities = list(cur.fetchall())
    CONN.commit()
    CONN.close()
    return filteredCities

if __name__ == '__main__':
    filteredCitiesByPopulation(POPULATION_THRESHHOLD)

    