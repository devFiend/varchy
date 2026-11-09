"""Model Context Protocol (MCP) Server for Varchy."""

import json
import sys
from pathlib import Path
from typing import Any

from varchy.core.engine import VarchyEngine
from varchy.core.models.common import GenerationMode, ProjectCategory


def start_mcp_server():
    """
    Minimal robust stdio JSON-RPC handler conforming to Model Context Protocol primitives.
    Enables Claude Desktop, Cursor, and other MCP clients to query Varchy.
    """
    engine = VarchyEngine()

    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            request = json.loads(line)
            method = request.get("method")
            req_id = request.get("id")
            params = request.get("params", {})

            result: Any = None

            if method == "initialize":
                result = {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {},
                        "resources": {},
                        "prompts": {},
                    },
                    "serverInfo": {
                        "name": "varchy-mcp-server",
                        "version": "0.1.0",
                    },
                }
            elif method == "tools/list":
                result = {
                    "tools": [
                        {
                            "name": "varchy_initialize_project",
                            "description": "Initialize a new Varchy architecture workspace.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "description": {"type": "string"},
                                    "category": {"type": "string", "default": "saas"},
                                },
                                "required": ["name", "description"],
                            },
                        },
                        {
                            "name": "varchy_generate_blueprint",
                            "description": "Generate a full software architecture blueprint from an idea.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "idea": {"type": "string"},
                                    "category": {"type": "string", "default": "saas"},
                                },
                                "required": ["idea"],
                            },
                        },
                        {
                            "name": "varchy_validate_blueprint",
                            "description": "Run 100-point deterministic validation scoring on current project.",
                            "inputSchema": {"type": "object", "properties": {}},
                        },
                        {
                            "name": "varchy_get_context",
                            "description": "Retrieve project blueprint summary and readiness score.",
                            "inputSchema": {"type": "object", "properties": {}},
                        },
                    ]
                }
            elif method == "tools/call":
                name = params.get("name")
                args = params.get("arguments", {})

                if name == "varchy_initialize_project":
                    meta = engine.initialize_project(
                        name=args.get("name", "NewProject"),
                        description=args.get("description", ""),
                        category=ProjectCategory(args.get("category", "saas")),
                    )
                    result = {"content": [{"type": "text", "text": meta.model_dump_json(indent=2)}]}
                elif name == "varchy_validate_blueprint":
                    report = engine.validate_blueprint()
                    result = {"content": [{"type": "text", "text": report.model_dump_json(indent=2)}]}
                elif name == "varchy_get_context":
                    bp = engine.workspace.load_blueprint()
                    result = {
                        "content": [
                            {
                                "type": "text",
                                "text": f"Project: {bp.metadata.name}\nRequirements: {len(bp.product.requirements)}\nTasks: {len(bp.planning.tasks)}",
                            }
                        ]
                    }
                else:
                    result = {"content": [{"type": "text", "text": f"Unknown tool: {name}"}]}

            response = {"jsonrpc": "2.0", "id": req_id, "result": result}
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()

        except Exception as e:
            err_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32603, "message": str(e)},
            }
            sys.stdout.write(json.dumps(err_response) + "\n")
            sys.stdout.flush()

