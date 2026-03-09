import sqlite3
from fastmcp import FastMCP
from config import DB_PATH

# Each MCP server is its own FastMCP instance with a descriptive name
hr_mcp = FastMCP("HR & Projects")


def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ── Employee tools ────────────────────────────────────────────────────────────


@hr_mcp.tool()
def list_employees(department: str | None = None) -> list[dict]:
    """
    List all employees. Optionally filter by department.
    Department options: Engineering, Platform, Data
    """
    with _get_conn() as conn:
        if department:
            rows = conn.execute(
                "SELECT * FROM employees WHERE department = ? ORDER BY name",
                (department,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM employees ORDER BY department, name"
            ).fetchall()
    return [dict(row) for row in rows]


@hr_mcp.tool()
def find_employee(name_or_email: str) -> dict | str:
    """Find a single employee by name or email address."""
    with _get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM employees WHERE name LIKE ? OR email = ?",
            (f"%{name_or_email}%", name_or_email),
        ).fetchone()
    if not row:
        return f"No employee found matching '{name_or_email}'"
    return dict(row)


@hr_mcp.tool()
def get_department_summary() -> list[dict]:
    """Get headcount summary grouped by department."""
    with _get_conn() as conn:
        rows = conn.execute("""
            SELECT department, COUNT(*) as headcount
            FROM employees
            GROUP BY department
            ORDER BY headcount DESC
        """).fetchall()
    return [dict(row) for row in rows]


# ── Project tools ─────────────────────────────────────────────────────────────


@hr_mcp.tool()
def list_projects(status: str | None = None) -> list[dict]:
    """
    List all projects. Optionally filter by status.
    Status options: active, completed, on-hold
    """
    with _get_conn() as conn:
        if status:
            rows = conn.execute(
                "SELECT * FROM projects WHERE status = ? ORDER BY name", (status,)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM projects ORDER BY status, name"
            ).fetchall()
    return [dict(row) for row in rows]


@hr_mcp.tool()
def get_project_team(project_name: str) -> dict | str:
    """Get the members assigned to a project by project name."""
    with _get_conn() as conn:
        project = conn.execute(
            "SELECT * FROM projects WHERE name LIKE ?", (f"%{project_name}%",)
        ).fetchone()
        if not project:
            return f"No project found matching '{project_name}'"
        members = conn.execute(
            """
            SELECT e.name, e.role, e.email, e.department
            FROM employees e
            JOIN project_members pm ON pm.employee_id = e.id
            WHERE pm.project_id = ?
            ORDER BY e.name
        """,
            (project["id"],),
        ).fetchall()
    return {
        "project": dict(project),
        "members": [dict(m) for m in members],
        "team_size": len(members),
    }
