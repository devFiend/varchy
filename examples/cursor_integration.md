# Using Varchy with Cursor IDE 🚀

Varchy works seamlessly with **Cursor** in two complementary ways:

---

## 1. Automatic IDE Rules (`.cursorrules`)

When you run `varchy generate` in your project folder, Varchy automatically creates a `.cursorrules` file in your project root.

Cursor Composer and Cursor Chat immediately read this file to enforce:
- System architecture constraints from `docs/03-engineering/architecture.md`.
- Database schemas from `docs/03-engineering/database.md`.
- Task sequencing from `docs/04-development/tasks.md`.

You can simply prompt Cursor Composer:
> *"Implement our next task. Verify acceptance criteria in docs/ before finishing."*

---

## 2. Model Context Protocol (MCP) Server

You can connect Varchy directly as an in-IDE MCP tool inside Cursor:

1. Open Cursor Settings (`Cmd + ,` or `Ctrl + ,`).
2. Navigate to **Features** ➔ **MCP Servers**.
3. Click **Add New MCP Server** and fill out:
   - **Name:** `varchy`
   - **Type:** `command`
   - **Command:** `varchy mcp run`

Or add directly to your `~/.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "varchy": {
      "command": "varchy",
      "args": ["mcp", "run"]
    }
  }
}
```

### Available In-Cursor Actions:
- Call `@varchy_validate_blueprint` to run the 100-point gate.
- Read live specifications via `varchy://project/prd` and `varchy://project/architecture`.
- Prepare task prompts via `@prepare_task_implementation`.

