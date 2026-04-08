import sqlite3
from fastmcp import FastMCP
from fastmcp.server.auth.providers.jwt import StaticTokenVerifier
from config import DB_PATH


# ── Authentication ────────────────────────────────────────────────────────────

verifier = StaticTokenVerifier(
    tokens={
        "main-plant-token": {
            "client_id": "alice@company.com",
            "scopes": ["read:data", "write:data", "admin:users"],
        },
        "sub-plant-token": {
            "client_id": "bob@company.com",
            "scopes": [],
        },
    },
    required_scopes=["read:data"],
)

# Each MCP server is its own FastMCP instance with a descriptive name
database_mcp = FastMCP("Database Access", auth=verifier)


def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ── Database tools ────────────────────────────────────────────────────────────


@database_mcp.tool()
def read_schema(table_name: str) -> dict:
    """Retrieve and return the schema of the specified table."""
    with _get_conn() as conn:
        schema = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    return {
        "table_name": table_name,
        "columns": [dict(row) for row in schema]
    }


@database_mcp.tool()
def preview_rows(table_name: str) -> dict:
    """Return the first 5 rows of the specified table."""
    with _get_conn() as conn:
        rows = conn.execute(f"SELECT * FROM {table_name} LIMIT 5").fetchall()
    return {
        "table_name": table_name,
        "rows": [dict(row) for row in rows],
        "row_count": len(rows)
    }


@database_mcp.tool()
def execute_read_only_query(query: str) -> dict:
    """Execute a read-only SQL query and return the results."""
    with _get_conn() as conn:
        rows = conn.execute(query).fetchall()
    return {
        "query": query,
        "results": [dict(row) for row in rows],
        "row_count": len(rows)
    }