import os
from google.adk.tools import MCPToolset
from google.adk.tools.mcp_tool import StdioConnectionParams
from mcp import StdioServerParameters

from utilities import _env_only_str

ghost_env = _env_only_str({
    "GHOST_API_URL": os.getenv("GHOST_API_URL"),
    "GHOST_ADMIN_API_KEY": os.getenv("GHOST_ADMIN_API_KEY"),
    "GHOST_API_VERSION": "v5.0",
})

ghost_toolset = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=["-y", "@fanyangmeng/ghost-mcp"],
            env=ghost_env,
        ),
    )
)
