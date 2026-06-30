import psycopg2
from config import load_config

def create_table():
    config = load_config()

    command = """
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        phone VARCHAR(20)
    );
    """

    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:
            cur.execute(command)

if __name__ == "__main__":
    create_table()