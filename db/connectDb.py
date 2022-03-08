from main import POPULATION_THRESHHOLD
from dotenv import dotenv_values
import psycopg2

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
    cur = CONN.cursor()

    cur.execute(''' 
                    SELECT city, country FROM worldwidecities
                    WHERE population >= %s
                    ORDER BY random() LIMIT 1;  ''', [populationThreshold])

    cityAndCountry = list(cur.fetchall())
    CONN.commit()
    CONN.close()

    return cityAndCountry

if __name__ == '__main__':
    getCitiesByPopulation(POPULATION_THRESHHOLD)

    