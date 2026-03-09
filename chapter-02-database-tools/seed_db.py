"""
seed_db.py — Run this once before starting the Chapter 03 server.
Creates and populates a local SQLite database with sample internal data.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "internal.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


def seed():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # ── Schema ────────────────────────────────────────────────────────────────

    cursor.executescript("""
        DROP TABLE IF EXISTS employees;
        DROP TABLE IF EXISTS projects;
        DROP TABLE IF EXISTS project_members;

        CREATE TABLE employees (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            email       TEXT UNIQUE NOT NULL,
            department  TEXT NOT NULL,
            role        TEXT NOT NULL,
            joined_date TEXT NOT NULL
        );

        CREATE TABLE projects (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            status      TEXT NOT NULL,  -- active | completed | on-hold
            team        TEXT NOT NULL,
            deadline    TEXT
        );

        CREATE TABLE project_members (
            project_id  INTEGER REFERENCES projects(id),
            employee_id INTEGER REFERENCES employees(id),
            PRIMARY KEY (project_id, employee_id)
        );
    """)

    # ── Seed data ─────────────────────────────────────────────────────────────

    employees = [
        ("Ada Lovelace",    "ada@company.com",     "Engineering", "Senior Engineer",  "2021-03-01"),
        ("Alan Turing",     "alan@company.com",    "Engineering", "Staff Engineer",   "2019-07-15"),
        ("Grace Hopper",    "grace@company.com",   "Engineering", "Tech Lead",        "2020-01-10"),
        ("Margaret Hamilton","margaret@company.com","Platform",   "Principal Engineer","2018-05-20"),
        ("Linus Torvalds",  "linus@company.com",   "Platform",    "Senior Engineer",  "2022-02-28"),
        ("Barbara Liskov",  "barbara@company.com", "Data",        "Data Engineer",    "2021-09-01"),
        ("Tim Berners-Lee", "tim@company.com",     "Data",        "Senior Engineer",  "2023-01-15"),
    ]

    cursor.executemany(
        "INSERT INTO employees (name, email, department, role, joined_date) VALUES (?, ?, ?, ?, ?)",
        employees
    )

    projects = [
        ("Internal Developer Portal", "active",    "Platform",    "2024-06-30"),
        ("Data Pipeline Rewrite",     "active",    "Data",        "2024-04-15"),
        ("Auth Service Migration",    "on-hold",   "Engineering", None),
        ("Observability Uplift",      "completed", "Platform",    "2023-12-01"),
        ("ML Feature Store",          "active",    "Data",        "2024-09-01"),
    ]

    cursor.executemany(
        "INSERT INTO projects (name, status, team, deadline) VALUES (?, ?, ?, ?)",
        projects
    )

    project_members = [
        (1, 4), (1, 5),        # Developer Portal: Margaret, Linus
        (2, 6), (2, 7),        # Data Pipeline: Barbara, Tim
        (3, 1), (3, 2),        # Auth Migration: Ada, Alan
        (4, 4), (4, 3),        # Observability: Margaret, Grace
        (5, 6), (5, 3),        # ML Feature Store: Barbara, Grace
    ]

    cursor.executemany(
        "INSERT INTO project_members (project_id, employee_id) VALUES (?, ?)",
        project_members
    )

    conn.commit()
    conn.close()
    print(f"✅ Database seeded at: {DB_PATH}")
    print(f"   {len(employees)} employees, {len(projects)} projects")


if __name__ == "__main__":
    seed()