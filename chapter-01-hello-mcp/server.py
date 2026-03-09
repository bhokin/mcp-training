"""
Chapter 01 — Hello MCP

Your first FastMCP server. We define two simple tools and run the server.

Key concepts:
- What is a Tool in MCP?
- How FastMCP maps Python functions to MCP tools
- How to run and test with MCP Inspector
"""

from fastmcp import FastMCP

# 1. Create the MCP server instance with a name
mcp = FastMCP("Hello MCP")


# 2. Use @mcp.tool() to register a function as an MCP tool.
#    - The function name becomes the tool name
#    - The docstring becomes the tool description (LLMs read this!)
#    - Type hints define the input schema automatically

@mcp.tool()
def greet(name: str) -> str:
    """Greet someone by name. Use this when you want to say hello to a person."""
    return f"Hello, {name}! Welcome to the MCP workshop 👋"


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers together and return the result."""
    return a + b


@mcp.tool()
def reverse_string(text: str) -> str:
    """Reverse the characters in a string."""
    return text[::-1]


# 3. Run the server using stdio transport (default for local/Claude Desktop use)
if __name__ == "__main__":
    mcp.run()
