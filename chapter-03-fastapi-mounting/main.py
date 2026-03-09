"""
main.py — FastAPI application entry point.

HOW TO REGISTER MULTIPLE MCP SERVERS:
    1. Create each FastMCP instance in mcp_servers/
    2. Call http_app(path="/mcp", stateless_http=True) on each
    3. Pass all their lifespans to FastAPI via combine_lifespans()
    4. Mount each app at its own prefix — final endpoint = /prefix/mcp

    Example result:
        /hr/mcp       → HR & Projects MCP server
        /utility/mcp  → Utility Tools MCP server

TO ADD A NEW MCP SERVER:
    Step 1: Create mcp_servers/your_server.py with a FastMCP instance
    Step 2: Import it here and call http_app(path="/mcp", stateless_http=True)
    Step 3: Add its lifespan to combine_lifespans()
    Step 4: Mount it with app.mount("/your-prefix", your_app)
    Step 5: Update routers/health.py /info with the new endpoint

Run with:
    uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI
from fastmcp.utilities.lifespan import combine_lifespans

from config import APP_TITLE, APP_DESCRIPTION, APP_VERSION
from routers.health import router as health_router
from mcp_servers.hr import hr_mcp
from mcp_servers.utility import utility_mcp


# ── Build MCP ASGI apps ───────────────────────────────────────────────────────

hr_app = hr_mcp.http_app(stateless_http=True)
utility_app = utility_mcp.http_app(stateless_http=True)


# ── FastAPI app ───────────────────────────────────────────────────────────────
# combine_lifespans wires all MCP session managers into FastAPI's lifespan.

app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    lifespan=combine_lifespans(
        hr_app.lifespan,
        utility_app.lifespan,
    ),
)

# ── REST routers ──────────────────────────────────────────────────────────────

app.include_router(health_router)

# ── Mount MCP servers ─────────────────────────────────────────────────────────
# MCP path patterns: {host}:{port}/{path}/mcp
#   http://localhost:8000/hr/mcp
#   http://localhost:8000/utility/mcp

app.mount("/hr", hr_app)
app.mount("/utility", utility_app)
