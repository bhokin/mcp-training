from fastapi import APIRouter

router = APIRouter(tags=["System"])


@router.get("/health")
def health_check():
    """Health check endpoint for load balancers and uptime monitors."""
    return {"status": "ok"}


@router.get("/info")
def server_info():
    """Lists all mounted MCP servers and their endpoints."""
    return {
        "service": "Internal MCP Gateway",
        "mcp_servers": [
            {
                "name": "HR & Projects",
                "endpoint": "/hr/mcp",
                "tools": ["list_employees", "find_employee", "get_department_summary",
                          "list_projects", "get_project_team"],
            },
            {
                "name": "Utility Tools",
                "endpoint": "/utility/mcp",
                "tools": ["get_current_datetime"],
            },
            # Add your new server info here
        ],
    }