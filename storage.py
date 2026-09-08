import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent / "falcon_ai.db"


def _connect():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with _connect() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS diagnoses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                farmer_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                status TEXT NOT NULL,
                disease_name TEXT NOT NULL,
                confidence REAL NOT NULL,
                damage_percent REAL NOT NULL,
                action TEXT NOT NULL
            )
            """
        )
        connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_diagnoses_phone_created ON diagnoses(phone, created_at DESC)"
        )


def save_diagnosis(farmer_name, phone, result):
    if not farmer_name or not phone:
        return
    recommendation = result.get("recommendation") or {}
    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO diagnoses
                (farmer_name, phone, status, disease_name, confidence, damage_percent, action)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                farmer_name.strip(),
                phone.strip(),
                str(result.get("status", "Unavailable")),
                str(result.get("disease_name", "Unknown")),
                float(result.get("confidence", 0) or 0),
                float(result.get("damage_percent", 0) or 0),
                str(recommendation.get("action", "No action recorded")),
            ),
        )


def get_diagnoses(phone, limit=20):
    if not phone:
        return []
    with _connect() as connection:
        rows = connection.execute(
            """
            SELECT created_at, status, disease_name, confidence, damage_percent, action
            FROM diagnoses
            WHERE phone = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (phone.strip(), limit),
        ).fetchall()
    return [dict(row) for row in rows]
