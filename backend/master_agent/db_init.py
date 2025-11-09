# run: python db_init.py
import sqlite3
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "mocks"
CUSTOMERS_JSON = DATA_DIR / "customers.json"

DB_PATH = Path(__file__).resolve().parent / "db.sqlite3"

schema = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS customers (
    id TEXT PRIMARY KEY,
    name TEXT,
    age INTEGER,
    city TEXT,
    phone TEXT,
    email TEXT,
    current_loans INTEGER,
    credit_score INTEGER,
    preapproved_limit INTEGER
);

CREATE TABLE IF NOT EXISTS offers (
    offer_id TEXT PRIMARY KEY,
    customer_id TEXT,
    amount INTEGER,
    tenure_months INTEGER,
    rate_annual_percent REAL,
    FOREIGN KEY(customer_id) REFERENCES customers(id)
);

CREATE TABLE IF NOT EXISTS interactions (
    session_id TEXT,
    customer_id TEXT,
    start_ts TEXT,
    end_ts TEXT,
    final_decision TEXT,
    note TEXT
);

CREATE TABLE IF NOT EXISTS uploads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    customer_id TEXT,
    filename TEXT,
    uploaded_at TEXT
);
"""

seed_offer_template = {
    # default sample offer; will be adjusted per customer
    "tenure_months": 24,
    "rate_annual_percent": 12.5
}

def load_customers():
    with open(CUSTOMERS_JSON, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    if not CUSTOMERS_JSON.exists():
        raise SystemExit(f"Missing {CUSTOMERS_JSON} — put customers.json in backend/mocks/")
    customers = load_customers()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript(schema)
    # seed customers
    for c in customers:
        cur.execute("""
            INSERT OR REPLACE INTO customers (id,name,age,city,phone,email,current_loans,credit_score,preapproved_limit)
            VALUES (?,?,?,?,?,?,?,?,?)
        """, (c["id"], c["name"], c["age"], c["city"], c["phone"], c["email"], c["current_loans"], c["credit_score"], c["preapproved_limit"]))
        # seed a matching offer row
        offer_id = f"O_{c['id']}"
        cur.execute("""
            INSERT OR REPLACE INTO offers (offer_id, customer_id, amount, tenure_months, rate_annual_percent)
            VALUES (?,?,?,?,?)
        """, (offer_id, c["id"], c["preapproved_limit"], seed_offer_template["tenure_months"], seed_offer_template["rate_annual_percent"]))
    conn.commit()
    conn.close()
    print(f"DB created at {DB_PATH}")

if __name__ == "__main__":
    main()
