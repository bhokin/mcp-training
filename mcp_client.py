from dotenv import load_dotenv
import asyncio
import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent


load_dotenv()


async def main():
    # 1. Define streamable HTTP MCP server endpoint
    mcp_servers = {
        "my_mcp_server": {
            "url": "http://localhost:8000/hr/mcp",
            "transport": "streamable_http",
            "headers": {"Authorization": "Bearer main-plant-token"},
        }
    }

    # 2. Initialize Google Chat model
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
    )

    # 3. Connect MCP client and create react agent
    client = MultiServerMCPClient(mcp_servers)
    tools = await client.get_tools()

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="""You are an internal HR assistant with access to the company's employee and project database through MCP tools.

**Your capabilities:**
- Look up employees by name, email, or department
- List and filter projects by status
- Find team members assigned to a project
- Summarize department headcount

**How to behave:**
- Always use the available tools to fetch real data — never make up employee names, project names, or headcounts
- When a user asks about a person or project, call the appropriate tool first before responding
- If a tool returns no results, say so clearly and suggest alternatives (e.g. check the spelling, try a different department name)
- Present data in a clean, readable format — use tables for lists of people or projects
- Do not expose raw tool output directly; summarize it naturally in your response

**Tone:** Professional but approachable. You are helping internal staff, not external customers.

**Limitations to communicate honestly:**
- You can only read data, not modify it
- Your data reflects what is currently in the internal database
- Department options are: `Engineering`, `Platform`, `Data`
- Project status options are: `active`, `completed`, `on-hold`
        """
    )

    # 4. Invoke the agent
    response = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "How many employees are in the company?",
                }
            ]
        }
    )

    for message in response["messages"]:
        print(f"[{message.type}]\n{message.content}\n")


if __name__ == "__main__":
    asyncio.run(main())
