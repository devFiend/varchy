"""Tests for MCP Resources and Prompts endpoints."""

import json
from io import StringIO
import sys
from varchy.core.engine import VarchyEngine
from varchy.core.models.common import ProjectCategory


def test_mcp_resources_and_prompts(tmp_path, monkeypatch):
    engine = VarchyEngine(tmp_path)
    engine.initialize_project(name="MCPTestApp", description="Testing MCP server", category=ProjectCategory.DEV_TOOL)
    # Generate blueprint
    import asyncio
    asyncio.run(engine.generate_blueprint(idea="Testing MCP server", provider_name="mock"))

    # Test JSON-RPC calls against start_mcp_server logic
    from varchy.mcp.server import start_mcp_server

    requests = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize"},
        {"jsonrpc": "2.0", "id": 2, "method": "resources/list"},
        {"jsonrpc": "2.0", "id": 3, "method": "resources/read", "params": {"uri": "varchy://project/overview"}},
        {"jsonrpc": "2.0", "id": 4, "method": "prompts/list"},
        {"jsonrpc": "2.0", "id": 5, "method": "prompts/get", "params": {"name": "review_architecture"}},
    ]
    input_text = "\n".join(json.dumps(r) for r in requests) + "\n"

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "stdin", StringIO(input_text))
    output_capture = StringIO()
    monkeypatch.setattr(sys, "stdout", output_capture)

    start_mcp_server()

    responses = [json.loads(line) for line in output_capture.getvalue().strip().split("\n") if line]
    assert len(responses) == 5

    # Check resources/list
    res_list = responses[1]["result"]["resources"]
    assert any(r["uri"] == "varchy://project/overview" for r in res_list)
    assert any(r["uri"] == "varchy://project/prd" for r in res_list)

    # Check resources/read
    res_read = responses[2]["result"]["contents"][0]
    assert res_read["uri"] == "varchy://project/overview"
    assert "MCPTestApp" in res_read["text"]

    # Check prompts/list
    prompt_list = responses[3]["result"]["prompts"]
    assert any(p["name"] == "review_architecture" for p in prompt_list)
    assert any(p["name"] == "prepare_task_implementation" for p in prompt_list)

    # Check prompts/get
    prompt_get = responses[4]["result"]
    assert "Architectural Review Prompt" in prompt_get["description"]

