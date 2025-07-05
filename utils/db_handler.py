import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager

DB_CONFIG = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'sasi1234',
    'host': 'localhost',
    'port': '5432'
}

@contextmanager
def get_db_connection():
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        yield conn
    finally:
        if conn is not None:
            conn.close()

def get_urls():
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT u.*, i.title, i.thumbnail 
                FROM tbl_urlqueue u 
                LEFT JOIN tbl_urlqueue_info i ON u.urlid = i.urlid 
                WHERE u.ismoved = true
                ORDER BY u.createdate DESC
            """)
            return cur.fetchall()

def get_queue():
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT u.*, i.title, i.thumbnail 
                FROM tbl_urlqueue u 
                LEFT JOIN tbl_urlqueue_info i ON u.urlid = i.urlid 
                WHERE u.ismoved = false
                ORDER BY u.createdate DESC
            """)
            return cur.fetchall()
