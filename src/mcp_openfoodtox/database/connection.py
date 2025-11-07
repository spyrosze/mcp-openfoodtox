import sqlite3
from pathlib import Path


def get_db_path():
    """Get the absolute path to the OpenFoodTox database."""
    # Get the project root (parent of src/)
    project_root = Path(__file__).parent.parent.parent.parent
    return project_root / "database" / "openfoodtox.db"


def get_connection():
    """
    Get a connection to the OpenFoodTox database.

    The connection supports the context manager protocol, so it can be used with 'with':

        with get_connection() as conn:
            # use conn
            pass

    Returns:
        sqlite3.Connection: Database connection object (supports context manager)
    """
    db_path = get_db_path()
    return sqlite3.connect(str(db_path))
