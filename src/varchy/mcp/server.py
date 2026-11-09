"""Model Context Protocol (MCP) Server for Varchy with Tools, Resources, and Prompts."""

import json
import sys
from pathlib import Path
from typing import Any

from varchy.core.engine import VarchyEngine
from varchy.core.models.common import GenerationMode, ProjectCategory


def start_mcp_server():
    """
    Standards-compliant stdio JSON-RPC handler conforming to Model Context Protocol (MCP).
    Enables Claude Desktop, Cursor, and other MCP clients to query tools, read live resources,
    and trigger reusable architectural prompts.
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
                        "version": "0.1.1",
                    },
                }

            # -------------------------------------------------------------
            # TOOLS API
            # -------------------------------------------------------------
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

            # -------------------------------------------------------------
            # RESOURCES API (PRD Section 7.4)
            # -------------------------------------------------------------
            elif method == "resources/list":
                result = {
                    "resources": [
                        {
                            "uri": "varchy://project/overview",
                            "name": "Project Overview & Metadata",
                            "mimeType": "application/json",
                        },
                        {
                            "uri": "varchy://project/prd",
                            "name": "Product Requirements Document (PRD)",
                            "mimeType": "text/markdown",
                        },
                        {
                            "uri": "varchy://project/architecture",
                            "name": "Technical Architecture Specification",
                            "mimeType": "text/markdown",
                        },
                        {
                            "uri": "varchy://project/database",
                            "name": "Database Schema & Entity Models",
                            "mimeType": "text/markdown",
                        },
                        {
                            "uri": "varchy://project/tasks",
                            "name": "Implementation Tasks & Dependencies",
                            "mimeType": "application/json",
                        },
                        {
                            "uri": "varchy://project/validation",
                            "name": "Deterministic 100-Point Readiness Report",
                            "mimeType": "application/json",
                        },
                    ]
                }

            elif method == "resources/read":
                uri = params.get("uri", "")
                if uri == "varchy://project/overview":
                    meta = engine.workspace.load_metadata()
                    result = {"contents": [{"uri": uri, "mimeType": "application/json", "text": meta.model_dump_json(indent=2)}]}
                elif uri == "varchy://project/prd":
                    prd_file = engine.workspace.docs_dir / "01-product" / "prd.md"
                    text = prd_file.read_text(encoding="utf-8") if prd_file.exists() else "# PRD not yet generated"
                    result = {"contents": [{"uri": uri, "mimeType": "text/markdown", "text": text}]}
                elif uri == "varchy://project/architecture":
                    arch_file = engine.workspace.docs_dir / "03-engineering" / "architecture.md"
                    text = arch_file.read_text(encoding="utf-8") if arch_file.exists() else "# Architecture not yet generated"
                    result = {"contents": [{"uri": uri, "mimeType": "text/markdown", "text": text}]}
                elif uri == "varchy://project/database":
                    db_file = engine.workspace.docs_dir / "03-engineering" / "database.md"
                    text = db_file.read_text(encoding="utf-8") if db_file.exists() else "# Database specs not yet generated"
                    result = {"contents": [{"uri": uri, "mimeType": "text/markdown", "text": text}]}
                elif uri == "varchy://project/tasks":
                    bp = engine.workspace.load_blueprint()
                    tasks_json = json.dumps([t.model_dump() for t in bp.planning.tasks], indent=2)
                    result = {"contents": [{"uri": uri, "mimeType": "application/json", "text": tasks_json}]}
                elif uri == "varchy://project/validation":
                    report = engine.validate_blueprint()
                    result = {"contents": [{"uri": uri, "mimeType": "application/json", "text": report.model_dump_json(indent=2)}]}
                else:
                    result = {"contents": [{"uri": uri, "mimeType": "text/plain", "text": f"Unknown resource URI: {uri}"}]}

            # -------------------------------------------------------------
            # PROMPTS API (PRD Section 7.5)
            # -------------------------------------------------------------
            elif method == "prompts/list":
                result = {
                    "prompts": [
                        {
                            "name": "review_architecture",
                            "description": "Reviews the current project architecture against the 100-point readiness gate and reports critical blockers.",
                        },
                        {
                            "name": "prepare_task_implementation",
                            "description": "Retrieves the exact specifications, acceptance criteria, and constraints for implementing a specific TASK-###.",
                            "arguments": [
                                {
                                    "name": "task_id",
                                    "description": "e.g. TASK-001",
                                    "required": True,
                                },
                            ],
                        },
                    ]
                }

            elif method == "prompts/get":
                prompt_name = params.get("name")
                prompt_args = params.get("arguments", {})

                if prompt_name == "review_architecture":
                    report = engine.validate_blueprint()
                    result = {
                        "description": "Architectural Review Prompt",
                        "messages": [
                            {
                                "role": "user",
                                "content": {
                                    "type": "text",
                                    "text": f"Review current project readiness score: {report.total_score}/100. Critical blockers: {len(report.critical_blockers)}. Provide guidance on next steps.",
                                },
                            }
                        ],
                    }
                elif prompt_name == "prepare_task_implementation":
                    task_id = prompt_args.get("task_id", "TASK-001")
                    bp = engine.workspace.load_blueprint()
                    target_task = next((t for t in bp.planning.tasks if t.id == task_id), None)
                    task_desc = target_task.model_dump_json(indent=2) if target_task else f"Task {task_id} not found"
                    result = {
                        "description": f"Implementation guidelines for {task_id}",
                        "messages": [
                            {
                                "role": "user",
                                "content": {
                                    "type": "text",
                                    "text": f"You are implementing {task_id}. Details:\n{task_desc}\nFollow architecture constraints in docs/03-engineering/architecture.md and test acceptance criteria.",
                                },
                            }
                        ],
                    }
                else:
                    result = {"description": f"Unknown prompt: {prompt_name}", "messages": []}

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
