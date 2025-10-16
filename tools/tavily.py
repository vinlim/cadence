import os

from google.adk.tools import MCPToolset
from google.adk.tools.mcp_tool import StreamableHTTPConnectionParams

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

tavily_toolset = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=f"https://mcp.tavily.com/mcp/?tavilyApiKey={TAVILY_API_KEY}",
        timeout=30,
    )
)