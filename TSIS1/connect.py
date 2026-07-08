import psycopg2
from config import load_config

def get_connection():
    """Connect to PostgreSQL and return connection"""
    config = load_config()
    try:
        conn = psycopg2.connect(**config)
        return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return None

# Оставляем старую функцию для совместимости
def connect(config):
    """Connect to the PostgreSQL database server"""
    try:
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

if __name__ == '__main__':
    config = load_config()
    connect(config)
