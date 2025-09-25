import asyncio
from reboot.mcp.client import connect

URL = "http://127.0.0.1:9991"  # make sure this matches your rbt output

async def run_client():
    async with connect(URL + "/mcp") as (session, session_id, version):
        print(f"\n✅ Connected to MCP server at {URL}/mcp\n")

        # Show available tools once
        tools = await session.list_tools()
        print("Available tools:")
        for t in tools.tools:
            print(f"- {t.name}")
        print("\n")

        while True:
            print("\n--- What do you want to do? ---")
            print("1) list_communities")
            print("2) search_prompts")
            print("3) get_prompt")
            print("4) trending_prompts")
            print("5) featured_prompts")
            print("6) render_prompt")
            print("0) quit")

            choice = input("> ").strip()
            if choice == "0":
                print("👋 Bye!")
                break

            try:
                if choice == "1":
                    result = await session.call_tool("list_communities")
                    print(result)

                elif choice == "2":
                    q = input("Search term: ").strip()
                    limit = input("Limit (default 5): ").strip()
                    limit = int(limit) if limit else 5
                    result = await session.call_tool("search_prompts", arguments={"q": q, "limit": limit})
                    print(result)

                elif choice == "3":
                    pid = int(input("Prompt ID: "))
                    result = await session.call_tool("get_prompt", arguments={"id": pid})
                    print(result)

                elif choice == "4":
                    result = await session.call_tool("trending_prompts")
                    print(result)

                elif choice == "5":
                    limit = input("Limit (default 5): ").strip()
                    limit = int(limit) if limit else 5
                    result = await session.call_tool("featured_prompts", arguments={"limit": limit})
                    print(result)

                elif choice == "6":
                    pid = int(input("Prompt ID: "))
                    variables = {}
                    while True:
                        k = input("Variable key (leave blank to stop): ").strip()
                        if not k:
                            break
                        v = input(f"Value for {k}: ").strip()
                        variables[k] = v
                    result = await session.call_tool("render_prompt", arguments={"id": pid, "variables": variables})
                    print(result)

                else:
                    print("❌ Invalid choice.")

            except Exception as e:
                print(f"❌ Error calling tool: {e}")

async def main():
    await run_client()

if __name__ == "__main__":
    asyncio.run(main())
