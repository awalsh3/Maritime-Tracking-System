import os
import logging
from contextlib import contextmanager
from psycopg2 import pool
from psycopg2.extras import RealDictCursor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
connection_pool = None


def get_db_url() -> str:
    """Constructs the database URL from environment variables."""
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        return db_url
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "password")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "maritime_db")
    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


def init_connection_pool(min_conn=1, max_conn=10):
    """Initializes the connection pool."""
    global connection_pool
    if connection_pool is None:
        try:
            db_url = get_db_url()
            connection_pool = pool.SimpleConnectionPool(min_conn, max_conn, dsn=db_url)
            logger.info("Database connection pool initialized successfully.")
        except Exception as e:
            logger.exception(f"Error initializing connection pool: {e}")
            connection_pool = None


@contextmanager
def get_db_connection():
    """
    A context manager to get a connection from the pool and automatically release it.
    """
    if connection_pool is None:
        init_connection_pool()
    if connection_pool is None:
        raise ConnectionError("Database connection pool is not available.")
    conn = None
    try:
        conn = connection_pool.getconn()
        yield conn
    except Exception as e:
        logger.exception(f"Database connection error: {e}")
        raise
    finally:
        if conn:
            connection_pool.putconn(conn)


def execute_query(query: str, params: tuple | None = None) -> list[dict]:
    """
    Executes a SQL query and fetches all results.
    Returns a list of dictionaries where keys are column names.
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params or ())
                if cursor.description:
                    results = cursor.fetchall()
                    return results
                else:
                    conn.commit()
                    return []
    except Exception as e:
        logger.exception(f"Error executing query: {e}")
        return []


def fetch_one(query: str, params: tuple | None = None) -> dict | None:
    """
    Executes a SQL query and fetches the first result.
    Returns a single dictionary or None.
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params or ())
                if cursor.description:
                    return cursor.fetchone()
                else:
                    conn.commit()
                    return None
    except Exception as e:
        logger.exception(f"Error fetching one record: {e}")
        return None


init_connection_pool()