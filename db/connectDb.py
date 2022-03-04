from dotenv import dotenv_values
import psycopg2

config = dotenv_values('.env')
POSTGRESQL_PASSWORD = config.get('POSTGRESQL_PASSWORD')
POSTGRES_HOST = config.get('POSTGRES_HOST')

def connectToDb():
    try:
        conn = psycopg2.connect(
            host= POSTGRES_HOST,
            database='postgres',
            user='postgres',
            password=POSTGRESQL_PASSWORD
        )
        print('Connection established with DB')
        conn.close()
        return True 
    except: 
        return False

if __name__ == '__main__':
    connectToDb()

    