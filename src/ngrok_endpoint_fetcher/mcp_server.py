"""MCP server that exposes a run_command tool to execute shell commands."""
import subprocess
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("command-executor")


@server.list_tools()
async def list_tools():
    """List available tools."""
    return [
        Tool(
            name="run_command",
            description="Execute a shell command and return the output. Use this to run curl, touch, or any other shell command.",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The command to execute (e.g., 'curl https://example.com', 'touch /tmp/test.txt')"
                    }
                },
                "required": ["command"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    """Execute a tool."""
    if name == "run_command":
        command = arguments.get("command", "")
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            output = f"Exit code: {result.returncode}\n"
            if result.stdout:
                output += f"Stdout:\n{result.stdout[:1000]}\n"
            if result.stderr:
                output += f"Stderr:\n{result.stderr[:500]}"
            return [TextContent(type="text", text=output)]
        except subprocess.TimeoutExpired:
            return [TextContent(type="text", text="Error: Command timed out after 30 seconds")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
