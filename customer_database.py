"""A small SQLite-backed customer database.

Customer IDs use two initials followed by a six-digit sequence (for example,
CP000001). Run this file to create/migrate ``customers.db``, seed five random
sample customers if the table is empty, and print the customers:
    python customer_database.py
"""

import random
import sqlite3
import uuid
from pathlib import Path
from typing import Optional

DATABASE_PATH = Path(__file__).with_name("customers.db")


def get_connection() -> sqlite3.Connection:
    """Open a connection and return rows with column-name access."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def make_customer_id(customer_name: str, sequence: int) -> str:
    """Build an ID from first/last initials and a six-digit sequence."""
    name_parts = customer_name.split()
    if len(name_parts) < 2:
        raise ValueError("Customer name must include a first and last name.")
    if not 1 <= sequence <= 999999:
        raise ValueError("Customer ID sequence must be between 1 and 999999.")
    initials = f"{name_parts[0][0]}{name_parts[-1][0]}".upper()
    return f"{initials}{sequence:06d}"


def next_customer_id(connection: sqlite3.Connection, customer_name: str) -> str:
    """Generate the next ID, using a sequence unique across the whole table."""
    max_sequence = 0
    for row in connection.execute("SELECT customer_id FROM customers"):
        customer_id = str(row[0])
        suffix = customer_id[2:]
        if len(customer_id) == 8 and suffix.isdigit():
            max_sequence = max(max_sequence, int(suffix))
    return make_customer_id(customer_name, max_sequence + 1)


def initialize_database() -> None:
    """Create the table, or migrate an older integer-ID table to the new format."""
    with get_connection() as connection:
        table_exists = connection.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'customers'"
        ).fetchone()

        if not table_exists:
            connection.execute(
                """CREATE TABLE customers (
                    customer_id TEXT PRIMARY KEY,
                    customer_name TEXT NOT NULL,
                    customer_email TEXT NOT NULL UNIQUE,
                    phone_number TEXT
                )"""
            )
            return

        columns = connection.execute("PRAGMA table_info(customers)").fetchall()
        id_column = next(column for column in columns if column["name"] == "customer_id")
        if id_column["type"].upper() == "TEXT":
            return

        # Preserve existing records while replacing the old integer primary key.
        old_customers = connection.execute(
            "SELECT customer_name, customer_email, phone_number "
            "FROM customers ORDER BY customer_id"
        ).fetchall()
        connection.execute(
            """CREATE TABLE customers_new (
                customer_id TEXT PRIMARY KEY,
                customer_name TEXT NOT NULL,
                customer_email TEXT NOT NULL UNIQUE,
                phone_number TEXT
            )"""
        )
        for sequence, customer in enumerate(old_customers, start=1):
            customer_id = make_customer_id(customer["customer_name"], sequence)
            connection.execute(
                """INSERT INTO customers_new
                   (customer_id, customer_name, customer_email, phone_number)
                   VALUES (?, ?, ?, ?)""",
                (
                    customer_id,
                    customer["customer_name"],
                    customer["customer_email"],
                    customer["phone_number"],
                ),
            )
        connection.execute("DROP TABLE customers")
        connection.execute("ALTER TABLE customers_new RENAME TO customers")


def add_customer(customer_name: str, customer_email: str, phone_number: str = "") -> str:
    """Add a customer and return the new eight-character customer_id."""
    with get_connection() as connection:
        customer_id = next_customer_id(connection, customer_name)
        connection.execute(
            """INSERT INTO customers (customer_id, customer_name, customer_email, phone_number)
               VALUES (?, ?, ?, ?)""",
            (customer_id, customer_name, customer_email, phone_number),
        )
        return customer_id


def seed_random_customers() -> None:
    """Insert five random sample customers, but only into an empty table."""
    first_names = ["Avery", "Jordan", "Morgan", "Riley", "Taylor", "Casey"]
    last_names = ["Carter", "Lee", "Patel", "Rivera", "Kim", "Brooks"]

    with get_connection() as connection:
        existing_count = connection.execute(
            "SELECT COUNT(*) FROM customers"
        ).fetchone()[0]
        if existing_count:
            return

        for _ in range(5):
            name = f"{random.choice(first_names)} {random.choice(last_names)}"
            email_id = uuid.uuid4().hex[:10]
            phone = f"555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
            customer_id = make_customer_id(name, _ + 1)
            connection.execute(
                """INSERT INTO customers
                   (customer_id, customer_name, customer_email, phone_number)
                   VALUES (?, ?, ?, ?)""",
                (customer_id, name, f"customer_{email_id}@example.com", phone),
            )


def get_customer(customer_id: str) -> Optional[sqlite3.Row]:
    """Return one customer, or None if the ID does not exist."""
    with get_connection() as connection:
        return connection.execute(
            "SELECT * FROM customers WHERE customer_id = ?", (customer_id,)
        ).fetchone()


def list_customers() -> list[sqlite3.Row]:
    """Return all customers ordered by ID."""
    with get_connection() as connection:
        return connection.execute(
            "SELECT * FROM customers ORDER BY customer_id"
        ).fetchall()


def update_customer(
    customer_id: str,
    customer_name: str,
    customer_email: str,
    phone_number: str = "",
) -> bool:
    """Update a customer; return False if the ID does not exist."""
    with get_connection() as connection:
        cursor = connection.execute(
            """UPDATE customers
               SET customer_name = ?, customer_email = ?, phone_number = ?
               WHERE customer_id = ?""",
            (customer_name, customer_email, phone_number, customer_id),
        )
        return cursor.rowcount > 0


def delete_customer(customer_id: str) -> bool:
    """Delete a customer; return False if the ID does not exist."""
    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM customers WHERE customer_id = ?", (customer_id,)
        )
        return cursor.rowcount > 0


if __name__ == "__main__":
    initialize_database()
    seed_random_customers()
    print(f"Customer database ready: {DATABASE_PATH}")
    for customer in list_customers():
        print(dict(customer))
