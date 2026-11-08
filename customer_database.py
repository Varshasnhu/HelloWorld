"""SQLite-backed customer database.

Customer IDs use first/last initials plus a six-digit sequence (for example,
CP000001). Dates of joining are stored as ISO dates (YYYY-MM-DD).
Run with: python customer_database.py
"""

import random
import sqlite3
import uuid
from datetime import date, timedelta
from pathlib import Path
from typing import Optional

DATABASE_PATH = Path(__file__).with_name("customers.db")


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def random_join_date() -> str:
    """Return a random date in the last 10 years."""
    days_back = random.randint(1, 3650)
    return (date.today() - timedelta(days=days_back)).isoformat()


def make_customer_id(customer_name: str, sequence: int) -> str:
    """Return initials followed by a six-digit sequence, e.g. CP000001."""
    parts = customer_name.split()
    if len(parts) < 2:
        raise ValueError("Customer name must include a first and last name.")
    if not 1 <= sequence <= 999999:
        raise ValueError("Customer ID sequence must be between 1 and 999999.")
    initials = f"{parts[0][0]}{parts[-1][0]}".upper()
    return f"{initials}{sequence:06d}"


def _next_customer_id(connection: sqlite3.Connection, customer_name: str) -> str:
    max_sequence = 0
    for row in connection.execute("SELECT customer_id FROM customers"):
        value = str(row[0])
        suffix = value[2:]
        if len(value) == 8 and suffix.isdigit():
            max_sequence = max(max_sequence, int(suffix))
    return make_customer_id(customer_name, max_sequence + 1)


def initialize_database() -> None:
    """Create the table or migrate the previous schema without losing rows."""
    with get_connection() as connection:
        exists = connection.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='customers'"
        ).fetchone()
        if not exists:
            connection.execute(
                """CREATE TABLE customers (
                    customer_id TEXT PRIMARY KEY,
                    customer_name TEXT NOT NULL,
                    customer_email TEXT NOT NULL UNIQUE,
                    phone_number TEXT,
                    date_of_joining TEXT
                )"""
            )
            return

        columns = connection.execute("PRAGMA table_info(customers)").fetchall()
        column_names = {column["name"] for column in columns}
        id_column = next(column for column in columns if column["name"] == "customer_id")

        if id_column["type"].upper() != "TEXT":
            old_rows = connection.execute(
                "SELECT customer_name, customer_email, phone_number FROM customers ORDER BY customer_id"
            ).fetchall()
            connection.execute(
                """CREATE TABLE customers_new (
                    customer_id TEXT PRIMARY KEY,
                    customer_name TEXT NOT NULL,
                    customer_email TEXT NOT NULL UNIQUE,
                    phone_number TEXT,
                    date_of_joining TEXT
                )"""
            )
            for sequence, row in enumerate(old_rows, start=1):
                connection.execute(
                    """INSERT INTO customers_new
                       (customer_id, customer_name, customer_email, phone_number, date_of_joining)
                       VALUES (?, ?, ?, ?, NULL)""",
                    (
                        make_customer_id(row["customer_name"], sequence),
                        row["customer_name"],
                        row["customer_email"],
                        row["phone_number"],
                    ),
                )
            connection.execute("DROP TABLE customers")
            connection.execute("ALTER TABLE customers_new RENAME TO customers")
        elif "date_of_joining" not in column_names:
            connection.execute("ALTER TABLE customers ADD COLUMN date_of_joining TEXT")


def assign_random_join_dates() -> None:
    """Fill in NULL or empty DOJ values with random dates across recent years."""
    with get_connection() as connection:
        for row in connection.execute(
            "SELECT customer_id FROM customers WHERE date_of_joining IS NULL OR date_of_joining = ''"
        ):
            connection.execute(
                "UPDATE customers SET date_of_joining = ? WHERE customer_id = ?",
                (random_join_date(), row["customer_id"]),
            )


def add_customer(
    customer_name: str,
    customer_email: str,
    phone_number: str = "",
    date_of_joining: Optional[str] = None,
) -> str:
    """Add a customer; date_of_joining should be YYYY-MM-DD (defaults to today)."""
    joining_date = date_of_joining or date.today().isoformat()
    with get_connection() as connection:
        customer_id = _next_customer_id(connection, customer_name)
        connection.execute(
            """INSERT INTO customers
               (customer_id, customer_name, customer_email, phone_number, date_of_joining)
               VALUES (?, ?, ?, ?, ?)""",
            (customer_id, customer_name, customer_email, phone_number, joining_date),
        )
        return customer_id


def seed_random_customers() -> None:
    """Insert five fictional sample customers with random DOJ values if the table is empty."""
    first_names = ["Avery", "Jordan", "Morgan", "Riley", "Taylor", "Casey"]
    last_names = ["Carter", "Lee", "Patel", "Rivera", "Kim", "Brooks"]
    with get_connection() as connection:
        if connection.execute("SELECT COUNT(*) FROM customers").fetchone()[0]:
            return
        for sequence in range(1, 6):
            name = f"{random.choice(first_names)} {random.choice(last_names)}"
            email = f"customer_{uuid.uuid4().hex[:10]}@example.com"
            phone = f"555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
            joined = random_join_date()
            connection.execute(
                """INSERT INTO customers
                   (customer_id, customer_name, customer_email, phone_number, date_of_joining)
                   VALUES (?, ?, ?, ?, ?)""",
                (make_customer_id(name, sequence), name, email, phone, joined),
            )


def get_customer(customer_id: str) -> Optional[sqlite3.Row]:
    with get_connection() as connection:
        return connection.execute(
            "SELECT * FROM customers WHERE customer_id = ?", (customer_id,)
        ).fetchone()


def list_customers() -> list[sqlite3.Row]:
    with get_connection() as connection:
        return connection.execute(
            "SELECT * FROM customers ORDER BY customer_id"
        ).fetchall()


def update_customer(
    customer_id: str,
    customer_name: str,
    customer_email: str,
    phone_number: str = "",
    date_of_joining: Optional[str] = None,
) -> bool:
    with get_connection() as connection:
        cursor = connection.execute(
            """UPDATE customers
               SET customer_name = ?, customer_email = ?, phone_number = ?, date_of_joining = ?
               WHERE customer_id = ?""",
            (customer_name, customer_email, phone_number, date_of_joining, customer_id),
        )
        return cursor.rowcount > 0


def delete_customer(customer_id: str) -> bool:
    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM customers WHERE customer_id = ?", (customer_id,)
        )
        return cursor.rowcount > 0


if __name__ == "__main__":
    initialize_database()
    seed_random_customers()
    assign_random_join_dates()
    print(f"Customer database ready: {DATABASE_PATH}")
    for customer in list_customers():
        print(dict(customer))
