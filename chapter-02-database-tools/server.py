"""
Chapter 02 — Database Tools

Connecting your MCP server to a real SQLite database.
We expose internal HR and project data as MCP tools.

Setup: Run `python seed_db.py` first to create the database.
"""

import sqlite3
import os
from fastmcp import FastMCP

mcp = FastMCP("Internal DB Tools")

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "internal.db")


def get_connection() -> sqlite3.Connection:
    """Return a SQLite connection with row_factory set for dict-like rows."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ── EMPLOYEE TOOLS ────────────────────────────────────────────────────────────

@mcp.tool()
def list_employees(department: str | None = None) -> list[dict]:
    """
    List all employees. Optionally filter by department name.
    Department options: Engineering, Platform, Data
    """
    with get_connection() as conn:
        if department:
            rows = conn.execute(
                "SELECT * FROM employees WHERE department = ? ORDER BY name",
                (department,)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM employees ORDER BY department, name"
            ).fetchall()

    return [dict(row) for row in rows]


@mcp.tool()
def find_employee(name_or_email: str) -> dict | str:
    """
    Find a single employee by their name or email address.
    Returns their full profile including department and role.
    """
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT * FROM employees
            WHERE name LIKE ? OR email = ?
            """,
            (f"%{name_or_email}%", name_or_email)
        ).fetchone()

    if not row:
        return f"No employee found matching '{name_or_email}'"

    return dict(row)


@mcp.tool()
def get_department_summary() -> list[dict]:
    """
    Get a headcount summary grouped by department.
    Useful for understanding team sizes at a glance.
    """
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT
                department,
                COUNT(*) as headcount,
                GROUP_CONCAT(role, ', ') as roles
            FROM employees
            GROUP BY department
            ORDER BY headcount DESC
        """).fetchall()

    return [dict(row) for row in rows]


# ── PROJECT TOOLS ─────────────────────────────────────────────────────────────

@mcp.tool()
def list_projects(status: str | None = None) -> list[dict]:
    """
    List all internal projects. Optionally filter by status.
    Status options: active, completed, on-hold
    """
    with get_connection() as conn:
        if status:
            rows = conn.execute(
                "SELECT * FROM projects WHERE status = ? ORDER BY name",
                (status,)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM projects ORDER BY status, name"
            ).fetchall()

    return [dict(row) for row in rows]


@mcp.tool()
def get_project_team(project_name: str) -> dict | str:
    """
    Get the team members assigned to a project by project name.
    Returns project details and the list of assigned employees.
    """
    with get_connection() as conn:
        project = conn.execute(
            "SELECT * FROM projects WHERE name LIKE ?",
            (f"%{project_name}%",)
        ).fetchone()

        if not project:
            return f"No project found matching '{project_name}'"

        members = conn.execute("""
            SELECT e.name, e.role, e.email, e.department
            FROM employees e
            JOIN project_members pm ON pm.employee_id = e.id
            WHERE pm.project_id = ?
            ORDER BY e.name
        """, (project["id"],)).fetchall()

    return {
        "project": dict(project),
        "members": [dict(m) for m in members],
        "team_size": len(members),
    }


@mcp.tool()
def find_available_engineers(department: str | None = None) -> list[dict]:
    """
    Find engineers who are not currently assigned to any active project.
    Optionally filter by department to find available engineers in a team.
    """
    with get_connection() as conn:
        query = """
            SELECT e.*
            FROM employees e
            WHERE e.id NOT IN (
                SELECT pm.employee_id
                FROM project_members pm
                JOIN projects p ON p.id = pm.project_id
                WHERE p.status = 'active'
            )
        """
        params = []
        if department:
            query += " AND e.department = ?"
            params.append(department)

        query += " ORDER BY e.department, e.name"
        rows = conn.execute(query, params).fetchall()

    return [dict(row) for row in rows]


if __name__ == "__main__":
    print(f"Starting MCP server... (DB: {DB_PATH})")
    mcp.run()