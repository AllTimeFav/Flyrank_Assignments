import os
import time
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()
POSTGRES_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    conn = psycopg.connect(POSTGRES_URL, row_factory=dict_row)
    return conn

class PostgresRepository:
    def __init__(self, connection_url: str):
        self.connection_url = connection_url
        self._init_db()

    def _init_db(self):
        max_retries = 5
        for i in range(max_retries):
            try:
                with psycopg.connect(self.connection_url) as conn:
                    with conn.cursor() as cur:
                        # Create table if missing
                        cur.execute("""
                            CREATE TABLE IF NOT EXISTS tasks (
                                id SERIAL PRIMARY KEY,
                                title TEXT NOT NULL,
                                done BOOLEAN DEFAULT FALSE
                            );
                        """)
                        
                        # Check row count
                        cur.execute("SELECT COUNT(*) FROM tasks;")
                        count = cur.fetchone()[0]
                        
                        # Seed only if table is empty
                        if count == 0:
                            cur.execute("""
                                INSERT INTO tasks (title, done) VALUES 
                                ('Book 1', true),
                                ('Book 2', false),
                                ('Book 3', false);
                            """)
                        conn.commit()
                break
            except psycopg.OperationalError as e:
                if i < max_retries - 1:
                    print(f"Database connection failed. Retrying in 2 seconds... ({i+1}/{max_retries})")
                    time.sleep(2)
                else:
                    raise e
