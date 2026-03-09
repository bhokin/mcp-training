import os

# ── Database ──────────────────────────────────────────────────────────────────

DB_PATH: str = os.getenv(
    "DB_PATH",
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "chapter-02-database-tools",
        "data",
        "internal.db",
    ),
)

# ── Auth ──────────────────────────────────────────────────────────────────────

API_KEY: str = os.getenv("MCP_API_KEY", "dev-secret-key")

# ── App metadata ──────────────────────────────────────────────────────────────

APP_TITLE = "Internal MCP Gateway"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "A FastAPI gateway that hosts multiple MCP servers over Streamable HTTP."