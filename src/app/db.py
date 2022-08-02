"""DB module to retrieve db connection."""

import psycopg2  # type: ignore
from os import getenv
from .exceptions import DBConnectionException

params = {
    'database': getenv("PG_DB"),
    'user': getenv("PG_USER"),
    'host': getenv("PG_HOST"),
    'password': getenv("PG_PASSWORD"),
    'port': getenv("PG_PORT"),
}


def get_connection():
    """Retrieve the psycopg connection handler."""
    try:
        conn = psycopg2.connect(**params)
        yield conn
    except psycopg2.OperationalError as e:
        raise DBConnectionException(f"Issue with DB Connection :-> {str(e)} ")
    except Exception as e:
        raise e
    finally:
        conn.close()
