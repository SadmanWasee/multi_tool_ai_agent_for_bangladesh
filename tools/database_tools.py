
import sqlite3
from pathlib import Path

from langchain_core.tools import tool


# Locate the database directory
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = BASE_DIR / "databases"


def execute_query(database_name: str, query: str) -> str:
    """Execute a read-only SQL SELECT query."""

    # Allow only SELECT statements
    cleaned_query = query.strip().rstrip(";").strip()

    if not cleaned_query.upper().startswith("SELECT "):
        return "Error: Only SELECT queries are allowed."

    if ";" in cleaned_query:
        return "Error: Multiple SQL statements are not allowed."

    db_path = DATABASE_DIR / database_name

    try:
        # Open database in read-only mode
        connection = sqlite3.connect(
            f"{db_path.as_uri()}?mode=ro",
            uri=True
        )

        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()
        cursor.execute(cleaned_query)

        results = cursor.fetchmany(20)

        if not results:
            return "No matching records found."

        # Convert query results into readable dictionaries
        records = [dict(row) for row in results]

        return str(records)

    except sqlite3.Error as error:
        return f"Database query error: {error}"

    finally:
        if "connection" in locals():
            connection.close()


@tool
def institutions_db_tool(query: str) -> str:
    """
    Query the institutions database.

    Use this tool for questions about universities, colleges,
    schools, madrasahs, EIIN, education levels, and institutional
    locations in Bangladesh.

    Input must be a valid SQLite SELECT query.
    Table name: institutions.
    """

    return execute_query("institutions.db", query)


@tool
def hospitals_db_tool(query: str) -> str:
    """
    Query the hospitals database.

    Use this tool for questions about healthcare organizations,
    hospital names, agencies, types, and locations in Bangladesh.

    Input must be a valid SQLite SELECT query.
    Table name: hospitals.
    """

    return execute_query("hospitals.db", query)


@tool
def restaurants_db_tool(query: str) -> str:
    """
    Query the restaurants database.

    Use this tool for questions about restaurant names, locations,
    addresses, ratings, reviews, and geographical coordinates.

    Input must be a valid SQLite SELECT query.
    Table name: restaurants.
    """

    return execute_query("restaurants.db", query)
