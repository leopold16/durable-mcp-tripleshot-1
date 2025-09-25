import asyncio, os, re, json
import httpx
from reboot.mcp.server import DurableContext, DurableMCP
from reboot.aio.workflows import at_least_once

BASE = os.getenv("TRIPLESHOT_BASE", "https://api.tripleshot.ai")
TIMEOUT = float(os.getenv("HTTP_TIMEOUT_MS", "15"))  # seconds
MCP_TOKEN = os.getenv("MCP_TOKEN")  # optional

mcp = DurableMCP(path="/mcp", log_level="DEBUG")

async def http_get(path: str, params: dict | None = None):
    async with httpx.AsyncClient(base_url=BASE, timeout=TIMEOUT) as client:
        r = await client.get(path, params=params, headers={"accept": "application/json"})
        r.raise_for_status()
        try:
            return r.json()
        except Exception:
            return {"raw": r.text}

def render_template(tpl: str, variables: dict) -> str:
    def replacer(match):
        key = match.group(1)
        return str(variables.get(key, f"{{{{{key}}}}}"))
    return re.sub(r"\{\{\s*([a-zA-Z0-9_.-]+)\s*\}\}", replacer, tpl)

@mcp.tool()
async def list_communities(context: DurableContext):
    return await at_least_once(
        "list_communities",
        context,
        lambda: http_get("/api/public/communities"),
        type=dict,
    )

@mcp.tool()
async def search_prompts(q: str, community: int | None = None, limit: int | None = None, offset: int | None = None, context: DurableContext = None):
    return await http_get(
        "/api/public/prompts/search",
        {"q": q, "community": community, "limit": limit, "offset": offset},
    )

@mcp.tool()
async def get_prompt(id: int, context: DurableContext):
    return await http_get(f"/api/public/prompts/{id}")

@mcp.tool()
async def trending_prompts(community: int | None = None, limit: int | None = None, context: DurableContext = None):
    return await http_get(
        "/api/public/prompts/trending",
        {"community": community, "limit": limit},
    )

@mcp.tool()
async def featured_prompts(limit: int | None = None, context: DurableContext = None):
    return await http_get("/api/public/prompts/featured", {"limit": limit})

@mcp.tool()
async def render_prompt(id: int, variables: dict = {}, context: DurableContext = None):
    data = await http_get(f"/api/public/prompts/{id}")
    body = data.get("data", {}).get("body") or data.get("body", "")
    rendered = render_template(body, variables)
    unresolved = list({m.strip("{} ") for m in re.findall(r"\{\{\s*([a-zA-Z0-9_.-]+)\s*\}\}", rendered)})
    return {
        "id": id,
        "title": data.get("data", {}).get("title") or data.get("title"),
        "rendered": rendered,
        "unresolved_variables": unresolved,
        "raw": data,
    }

async def main():
    await mcp.application().run()

if __name__ == "__main__":
    asyncio.run(main())
