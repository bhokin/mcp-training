from datetime import datetime, timezone
from fastmcp import FastMCP

utility_mcp = FastMCP("Utility Tools")


@utility_mcp.tool()
def get_current_datetime() -> dict:
    """Get the current date and time in UTC."""
    now = datetime.now(timezone.utc)
    return {
        "utc": now.isoformat(),
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "weekday": now.strftime("%A"),
    }
