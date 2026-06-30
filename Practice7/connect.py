import psycopg2
from config import load_config

def connect(config):
    try:
        conn = psycopg2.connect(**config)
        print("Connected to PostgreSQL.")
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == "__main__":
    config = load_config()
    conn = connect(config)
    if conn:
        conn.close()