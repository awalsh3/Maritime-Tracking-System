import os
import logging
from contextlib import contextmanager
from sqlmodel import create_engine, Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_db_url() -> str:
    """Constructs the database URL from environment variables."""
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql+psycopg2://", 1)
        return db_url
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "password")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "maritime_db")
    return (
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )


DATABASE_URL = get_db_url()
engine = create_engine(DATABASE_URL)


@contextmanager
def get_session():
    """Context manager for providing a database session for read-only queries."""
    session = None
    try:
        with Session(engine) as session:
            session.exec("SET default_transaction_read_only = on;")
            yield session
    except Exception as e:
        logger.exception(f"Database session error: {e}")
        if session:
            session.rollback()
        raise
    finally:
        if session:
            session.close()