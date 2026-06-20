"""
Initializes and loads mock data into PostgreSQL from mock_data.json.

- Creates all required tables if they do not exist.
- Loads data from /docker-entrypoint-initdb.d/data/mock_data.json into each table.
- Uses psycopg2 for database operations.

Author: Mews.FnO.Data
"""

import json
from typing import Any, List

import psycopg2

DB_HOST: str = "localhost"
DB_PORT: int = 5432
DB_NAME: str = "proddb"
DB_USER: str = "produser"
DB_PASS: str = "prodpassword"

DATA_PATH: str = "/docker-entrypoint-initdb.d/data/mock_data.json"

print("Initializing PostgreSQL database with mock data...")


def get_conn() -> psycopg2.extensions.connection:
    """Establish a connection to the PostgreSQL database."""
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS
    )


def create_tables(cur: psycopg2.extensions.cursor) -> None:
    """Create all required tables if they do not exist."""
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS salesforce_customers (
        id VARCHAR(64) PRIMARY KEY,
        is_deleted BOOLEAN,
        account_number INTEGER,
        name TEXT,
        billing_country VARCHAR(2),
        capacity_s INTEGER,
        capacity_m INTEGER,
        capacity_l INTEGER
    );
    """
    )
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS business_central_global_customers (
        id UUID PRIMARY KEY,
        account_number INTEGER,
        currency VARCHAR(3),
        country_code VARCHAR(2)
    );
    """
    )
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS ledger (
        id VARCHAR(64) PRIMARY KEY,
        journal_id VARCHAR(64),
        account_number INTEGER,
        account_code VARCHAR(16),
        date DATE,
        currency VARCHAR(3),
        amount FLOAT,
        ix_code FLOAT,
        entity_code VARCHAR(16),
        territory VARCHAR(8),
        business_unit VARCHAR(16),
        consolidation_group VARCHAR(16),
        is_adjustment_entry BOOLEAN,
        is_manual BOOLEAN
    );
    """
    )
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS fx_rates (
        month VARCHAR(7),
        currency VARCHAR(3),
        rate_to_eur FLOAT
    );
    """
    )
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS journal_entries (
        journal_id VARCHAR(64) PRIMARY KEY,
        source_system VARCHAR(32),
        posted_by VARCHAR(32),
        status VARCHAR(16),
        posted_at TIMESTAMP
    );
    """
    )
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS accounts (
        account_code VARCHAR(16) PRIMARY KEY,
        account_name TEXT,
        account_type VARCHAR(32),
        reporting_group VARCHAR(32),
        is_pl_account BOOLEAN
    );
    """
    )
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS entity_codes (
        entity_code VARCHAR(16) PRIMARY KEY,
        description TEXT,
        created_at DATE
    );
    """
    )
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS territories (
        territory VARCHAR(8) PRIMARY KEY,
        description TEXT,
        region VARCHAR(16),
        country_group VARCHAR(16)
    );
    """
    )
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS business_units (
        business_unit VARCHAR(16) PRIMARY KEY,
        description TEXT,
        unit_type VARCHAR(32),
        manager VARCHAR(32)
    );
    """
    )
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS consolidation_groups (
        consolidation_group VARCHAR(16) PRIMARY KEY,
        description TEXT,
        group_type VARCHAR(32),
        lead_entity VARCHAR(16)
    );
    """
    )
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS ix_codes (
        ix_code FLOAT PRIMARY KEY,
        description TEXT,
        category VARCHAR(32),
        is_active BOOLEAN,
        created_date DATE
    );
    """
    )


def insert_many(
    cur: psycopg2.extensions.cursor, table: str, rows: List[dict], columns: List[str]
) -> None:
    """Insert multiple rows into a table."""
    if not rows:
        return
    cols = ", ".join(columns)
    placeholders = ", ".join(["%s"] * len(columns))
    sql = f"INSERT INTO {table} ({cols}) VALUES ({placeholders}) ON CONFLICT DO NOTHING"
    for row in rows:
        values = [row.get(col) for col in columns]
        if all(v is None for v in values):
            continue
        cur.execute(sql, values)


def insert_dimension(cur, table: str, column: str, values: list[str]) -> None:
    """Insert unique values into a dimension table."""
    sql = f"INSERT INTO {table} ({column}) VALUES (%s) ON CONFLICT DO NOTHING"
    for v in set(values):
        cur.execute(sql, (v,))


def main() -> None:
    """Main routine to load all tables from mock_data.json into PostgreSQL."""
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data: dict[str, Any] = json.load(f)

    conn = get_conn()
    cur = conn.cursor()
    create_tables(cur)

    # Insert salesforce_customers
    sf_rows = data["salesforce"]["customers"]
    sf_cols = [
        "id",
        "is_deleted",
        "account_number",
        "name",
        "billing_country",
        "capacity_s",
        "capacity_m",
        "capacity_l",
    ]
    insert_many(cur, "salesforce_customers", sf_rows, sf_cols)

    # Insert business_central_global_customers
    bc_rows = data["business_central"]["global_customers"]
    bc_cols = ["id", "account_number", "currency", "country_code"]
    insert_many(cur, "business_central_global_customers", bc_rows, bc_cols)

    # Insert ledger
    ledger_rows = data["ledger"]["lines"]
    ledger_cols = [
        "id",
        "journal_id",
        "account_number",
        "account_code",
        "date",
        "currency",
        "amount",
        "ix_code",
        "entity_code",
        "territory",
        "business_unit",
        "consolidation_group",
        "is_adjustment_entry",
        "is_manual",
    ]
    insert_many(cur, "ledger", ledger_rows, ledger_cols)

    # Insert fx_rates
    fx_rows = data["fx_rates"]["rates"]
    fx_cols = ["month", "currency", "rate_to_eur"]
    insert_many(cur, "fx_rates", fx_rows, fx_cols)

    # Insert journal_entries
    je_rows = data["journal_entries"]["entries"]
    je_cols = ["journal_id", "source_system", "posted_by", "status", "posted_at"]
    insert_many(cur, "journal_entries", je_rows, je_cols)

    # Insert accounts
    acc_rows = data["accounts"]["dimension"]
    acc_cols = [
        "account_code",
        "account_name",
        "account_type",
        "reporting_group",
        "is_pl_account",
    ]
    insert_many(cur, "accounts", acc_rows, acc_cols)

    # Insert entity_codes, territories, business_units, consolidation_groups with metadata
    entity_codes_rows = data["entity_codes"]
    entity_codes_cols = [
        "entity_code",
        "description",
        "created_at",
    ]
    insert_many(cur, "entity_codes", entity_codes_rows, entity_codes_cols)

    territories_rows = data["territories"]
    territories_cols = ["territory", "description", "region", "country_group"]
    insert_many(cur, "territories", territories_rows, territories_cols)

    business_units_rows = data["business_units"]
    business_units_cols = [
        "business_unit",
        "description",
        "unit_type",
        "manager",
    ]
    insert_many(cur, "business_units", business_units_rows, business_units_cols)

    consolidation_groups_rows = data["consolidation_groups"]
    consolidation_groups_cols = [
        "consolidation_group",
        "description",
        "group_type",
        "lead_entity",
    ]
    insert_many(
        cur,
        "consolidation_groups",
        consolidation_groups_rows,
        consolidation_groups_cols,
    )

    # Insert ix_codes
    ix_codes_rows = data["ix_codes"]
    ix_codes_cols = [
        "ix_code",
        "description",
        "category",
        "is_active",
        "created_date",
    ]
    insert_many(cur, "ix_codes", ix_codes_rows, ix_codes_cols)

    conn.commit()
    cur.close()
    conn.close()
    print("All tables loaded.")


if __name__ == "__main__":
    main()
