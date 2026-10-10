"""SQLite persistence for SmartBill orders"""
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "smartbill.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT,
            items_json TEXT,
            subtotal REAL,
            discount REAL,
            vat REAL,
            total REAL,
            split_n INTEGER,
            note TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_order(items, subtotal, discount, vat, total, split_n, note=""):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO orders (created_at, items_json, subtotal, discount, vat, total, split_n, note) VALUES (?,?,?,?,?,?,?,?)",
        (datetime.now().isoformat(), str(items), subtotal, discount, vat, total, split_n, note)
    )
    conn.commit()
    order_id = c.lastrowid
    conn.close()
    return order_id

def load_orders(limit=50):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, created_at, items_json, subtotal, discount, vat, total, split_n, note FROM orders ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    orders = []
    for r in rows:
        try:
            items = eval(r[2]) if r[2] else []
        except Exception:
            items = []
        orders.append({
            "id": r[0], "time": r[1], "items": items,
            "subtotal": r[3], "discount": r[4], "vat": r[5],
            "total": r[6], "split": r[7], "note": r[8] or ""
        })
    return orders

def delete_order(order_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM orders WHERE id=?", (order_id,))
    conn.commit()
    conn.close()

def clear_all_orders():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM orders")
    conn.commit()
    conn.close()

init_db()
