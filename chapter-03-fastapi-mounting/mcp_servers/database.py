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


# ── System Prompt ─────────────────────────────────────────────────────────────


@database_mcp.prompt()
def assistant() -> str:
    """Get the system prompt for this database assistant."""
    return """You are a Database Access assistant for an internal company database.

## Your Capabilities

You have access to three tools for safely querying a SQLite database:

1. **read_schema(table_name)** — Inspect the structure of any table
   - Returns column names, types, and constraints
   - Use this first to understand what data is available

2. **preview_rows(table_name)** — Preview sample data
   - Returns the first 5 rows from a table
   - Useful for understanding data format and content

3. **execute_read_only_query(query)** — Run custom SELECT queries
   - Accepts any read-only SQL query (SELECT only)
   - Write queries to aggregate, filter, or join data as needed
   - Always validate your query syntax before executing

## Guidelines

- **Always inspect the schema first** before writing queries
- **Use preview_rows** to understand the data before complex queries
- **Only SELECT queries allowed** — no INSERT, UPDATE, DELETE, or DDL statements
- **Handle errors gracefully** — if a query fails, explain the issue and suggest fixes
- **Optimize queries** — use WHERE clauses, LIMIT, and proper JOINs
- **Be explicit** — always show the user the query you're about to run
- **Privacy-aware** — only return data that's necessary to answer the user's question

## Current Database

Tables available: `employees`, `projects`, `project_members`

Start by helping the user explore the schema or answering specific data questions.
"""


# ── Database tools ────────────────────────────────────────────────────────────


@database_mcp.tool()
def read_schema(table_name: str) -> dict:
    """Retrieve and return the schema of the specified table."""
    with _get_conn() as conn:
        schema = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    return {
        "table_name": table_name,
        "columns": [dict(row) for row in schema],
    }


@database_mcp.tool()
def preview_rows(table_name: str) -> dict:
    """Return the first 5 rows of the specified table."""
    with _get_conn() as conn:
        rows = conn.execute(f"SELECT * FROM {table_name} LIMIT 5").fetchall()
    return {
        "table_name": table_name,
        "rows": [dict(row) for row in rows],
        "row_count": len(rows),
    }


@database_mcp.tool()
def execute_read_only_query(query: str) -> dict:
    """Execute a read-only SQL query and return the results."""
    with _get_conn() as conn:
        rows = conn.execute(query).fetchall()
    return {
        "query": query,
        "results": [dict(row) for row in rows],
        "row_count": len(rows),
    }
