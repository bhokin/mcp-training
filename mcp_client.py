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
            "url": "http://localhost:8000/database/mcp",
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

    # 4. Fetch system prompt from MCP server
    try:
        prompt = await client.get_prompt("my_mcp_server", "assistant")
        system_prompt = prompt[0].content
    except Exception:
        system_prompt = "You are a helpful assistant."

    agent = create_agent(model=llm, tools=tools, system_prompt=system_prompt)

    # 5. Invoke the agent
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
