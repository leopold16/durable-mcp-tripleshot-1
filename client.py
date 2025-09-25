import asyncio
from reboot.mcp.client import connect

URL = "http://localhost:9991"  # use the port from rbt logs

async def main():
    async with connect(URL + "/mcp") as (session, session_id, version):
        print(await session.list_tools())
        print(await session.call_tool("add", arguments={"a": 5, "b": 3}))

if __name__ == "__main__":
    asyncio.run(main())
