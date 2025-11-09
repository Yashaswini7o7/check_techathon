-- same schema as in db_init.py; save and run: sqlite3 db.sqlite3 < init.sql
PRAGMA foreign_keys = ON;
CREATE TABLE customers ( id TEXT PRIMARY KEY, name TEXT, age INTEGER, city TEXT, phone TEXT, email TEXT, current_loans INTEGER, credit_score INTEGER, preapproved_limit INTEGER );
CREATE TABLE offers ( offer_id TEXT PRIMARY KEY, customer_id TEXT, amount INTEGER, tenure_months INTEGER, rate_annual_percent REAL, FOREIGN KEY(customer_id) REFERENCES customers(id) );
CREATE TABLE interactions ( session_id TEXT, customer_id TEXT, start_ts TEXT, end_ts TEXT, final_decision TEXT, note TEXT );
CREATE TABLE uploads ( id INTEGER PRIMARY KEY AUTOINCREMENT, session_id TEXT, customer_id TEXT, filename TEXT, uploaded_at TEXT );
