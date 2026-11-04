
import re
import sqlite3
from pathlib import Path

from datasets import load_dataset


# Project directories
BASE_DIR = Path(__file__).resolve().parent
DATABASE_DIR = BASE_DIR / "databases"

DATABASE_DIR.mkdir(exist_ok=True)


# Hugging Face datasets and their corresponding databases
DATASETS = {
    "institutions": {
        "repository": "Mahadih534/Institutional-Information-of-Bangladesh",
        "database": "institutions.db",
        "table": "institutions"
    },
    "hospitals": {
        "repository": "Mahadih534/all-bangladeshi-hospitals",
        "database": "hospitals.db",
        "table": "hospitals"
    },
    "restaurants": {
        "repository": "Mahadih534/Bangladeshi-Restaurant-Data",
        "database": "restaurants.db",
        "table": "restaurants"
    }
}


def normalize_column_name(column):
    """Convert column names into snake_case."""
    column = column.strip().lower()
    column = re.sub(r"[^a-z0-9]+", "_", column)
    return column.strip("_")


def create_database(name, config):
    print(f"\nCreating {name} database...")

    # Load dataset from Hugging Face
    dataset = load_dataset(config["repository"])

    # Convert the training split to Pandas DataFrame
    df = dataset["train"].to_pandas()

    # Normalize column names
    df.columns = [
        normalize_column_name(column)
        for column in df.columns
    ]

    # Create SQLite database
    db_path = DATABASE_DIR / config["database"]

    with sqlite3.connect(db_path) as connection:

        # Insert DataFrame into SQLite table
        df.to_sql(
            config["table"],
            connection,
            if_exists="replace",
            index=False
        )

        # Verify record count
        cursor = connection.cursor()

        cursor.execute(
            f"SELECT COUNT(*) FROM {config['table']}"
        )

        record_count = cursor.fetchone()[0]

        # Display database schema
        cursor.execute(
            f"PRAGMA table_info({config['table']})"
        )

        columns = cursor.fetchall()

    print(f"Database created: {db_path.name}")
    print(f"Table name: {config['table']}")
    print(f"Total records: {record_count}")

    print("\nTable columns:")

    for column in columns:
        print(f"- {column[1]} ({column[2]})")


def main():
    print("Starting Bangladesh AI Agent database creation...")

    for name, config in DATASETS.items():
        create_database(name, config)

    print("\nAll databases created successfully!")


if __name__ == "__main__":
    main()
