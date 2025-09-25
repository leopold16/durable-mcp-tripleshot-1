Understood — you want something that reads like a real engineer wrote it for other engineers, zero fluff, just what’s needed to get running and hacking. Here’s a **lean, technical README**:

---

# durable-mcp-tripleshot

Minimal [Durable MCP](https://docs.reboot.dev/get_started/python_mcp/) server exposing Tripleshot public API as MCP tools.

## Setup

```bash
uv init --python 3.12.11
uv add reboot durable-mcp httpx "mcp[cli]"
```

Create `.rbtrc`:

```
dev run --no-generate-watch
dev run --python --application=server.py --working-directory=.
dev run --watch=**/*.py
```

Run server:

```bash
rbt dev run
# MCP available at http://127.0.0.1:9991/mcp
```

## Tools

| Tool             | Endpoint                                |
| ---------------- | --------------------------------------- |
| list_communities | `GET /api/public/communities`           |
| search_prompts   | `GET /api/public/prompts/search`        |
| get_prompt       | `GET /api/public/prompts/:id`           |
| trending_prompts | `GET /api/public/prompts/trending`      |
| featured_prompts | `GET /api/public/prompts/featured`      |
| render_prompt    | fetch + template-substitute prompt body |

## Client

Run interactive client:

```bash
uv run python client.py
```

Supports `list_communities`, `search_prompts`, `get_prompt`, `trending_prompts`, `featured_prompts`, `render_prompt`.

## Config

| Variable        | Default                                                |
| --------------- | ------------------------------------------------------ |
| TRIPLESHOT_BASE | [https://api.tripleshot.ai](https://api.tripleshot.ai) |
| HTTP_TIMEOUT_MS | 15000                                                  |
| MCP_TOKEN       | unset                                                  |

## Notes

* Server is durable: tools run inside `DurableContext`, safe to retry.
* HTTP handled via `httpx.AsyncClient`.
* State can be inspected at `http://127.0.0.1:9991/__/inspect`.
