import asyncio
from reboot.aio.applications import Application
from reboot.mcp.server import DurableContext, DurableMCP
from reboot.std.collections.v1.sorted_map import SortedMap
from reboot.aio.workflows import at_least_once

# Durable MCP server at path "/mcp"
mcp = DurableMCP(path="/mcp", log_level="DEBUG")

@mcp.tool()
async def add(a: int, b: int, context: DurableContext) -> int:
    """Add two numbers and store result in a SortedMap."""

    async def do_side_effect_idempotently() -> int:
        result = a + b
        await SortedMap.ref("adds").Insert(
            context,
            entries={f"{a} + {b}": str(result).encode()},
        )
        return result

    result = await at_least_once(
        "record_add",
        context,
        do_side_effect_idempotently,
        type=int,
    )
    return result

async def main():
    await mcp.application().run()

if __name__ == "__main__":
    asyncio.run(main())

