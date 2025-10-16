from google.adk.tools import MCPToolset
from google.adk.tools.mcp_tool import StdioConnectionParams
from mcp import StdioServerParameters


reddit_toolset = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="uvx",
            args=["--from", "git+https://github.com/adhikasp/mcp-reddit.git", "mcp-reddit"]
        )
    )
)