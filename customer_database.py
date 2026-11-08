"""A small SQLite-backed customer database.

Run this file directly to create ``customers.db``, seed five random sample
customers if the table is empty, and print the customers:
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


def initialize_database() -> None:
    """Create the customers table if it does not already exist."""
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                customer_email TEXT NOT NULL UNIQUE,
                phone_number TEXT
            )
            """
        )


def add_customer(customer_name: str, customer_email: str, phone_number: str = "") -> int:
    """Add a customer and return the new customer_id."""
    with get_connection() as connection:
        cursor = connection.execute(
            """INSERT INTO customers (customer_name, customer_email, phone_number)
               VALUES (?, ?, ?)""",
            (customer_name, customer_email, phone_number),
        )
        return int(cursor.lastrowid)


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

        customers = []
        for _ in range(5):
            name = f"{random.choice(first_names)} {random.choice(last_names)}"
            email_id = uuid.uuid4().hex[:10]
            phone = f"555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
            customers.append((name, f"customer_{email_id}@example.com", phone))

        connection.executemany(
            """INSERT INTO customers (customer_name, customer_email, phone_number)
               VALUES (?, ?, ?)""",
            customers,
        )


def get_customer(customer_id: int) -> Optional[sqlite3.Row]:
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
    customer_id: int,
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


def delete_customer(customer_id: int) -> bool:
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
