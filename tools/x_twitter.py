import os
from google.adk.tools import MCPToolset
from google.adk.tools.mcp_tool import StdioConnectionParams
from mcp import StdioServerParameters
from utilities import _env_only_str

twitter_env = _env_only_str({
    "PYTHONUNBUFFERED": "1",
    "TWITTER_API_KEY": os.getenv("TWITTER_API_KEY"),
    "TWITTER_API_SECRET": os.getenv("TWITTER_API_SECRET"),
    "TWITTER_ACCESS_TOKEN": os.getenv("TWITTER_ACCESS_TOKEN"),
    "TWITTER_ACCESS_TOKEN_SECRET": os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
    "TWITTER_BEARER_TOKEN": os.getenv("TWITTER_BEARER_TOKEN"),
})

x_toolset = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="uv",
            args=[
                "--directory",
                ".venv/bin/",
                "run",
                "x-twitter-mcp-server"
            ],
            env=twitter_env,
        )
    ),
)
