"""Tests for architectural templates, incremental updates, and Mermaid diagram generation."""

import pytest
from typer.testing import CliRunner
from varchy.cli.main import app
from varchy.core.compiler.compiler import DocCompiler
from varchy.core.engine import VarchyEngine
from varchy.core.models.common import GenerationMode, ProjectCategory
from varchy.core.pipeline.context import StageContext
from varchy.core.pipeline.stages.clarification import ClarificationStage
from varchy.core.storage.workspace import WorkspaceManager
from varchy.providers.mock import MockAIProvider
from varchy.templates.registry import TEMPLATES_REGISTRY, get_template

runner = CliRunner()


def test_templates_registry_contains_archetypes():
    assert "saas" in TEMPLATES_REGISTRY
    assert "local_first" in TEMPLATES_REGISTRY
    assert "api_backend" in TEMPLATES_REGISTRY
    assert "dev_tool" in TEMPLATES_REGISTRY
    assert "mobile_app" in TEMPLATES_REGISTRY

    tmpl = get_template("local_first")
    assert tmpl is not None
    assert tmpl.category == ProjectCategory.DEV_TOOL
    assert len(tmpl.recommended_tech_stack) > 0


def test_cli_templates_list_and_inspect():
    res = runner.invoke(app, ["templates"])
    assert res.exit_code == 0
    assert "Multi-Tenant Web SaaS" in res.stdout
    assert "Local-First Encrypted App" in res.stdout

    inspect_res = runner.invoke(app, ["templates", "inspect", "saas"])
    assert inspect_res.exit_code == 0
    assert "Recommended Technology Stack" in inspect_res.stdout
    assert "PostgreSQL" in inspect_res.stdout


@pytest.mark.asyncio
async def test_interactive_discovery_interview_callback(tmp_path):
    ws = WorkspaceManager(tmp_path)
    engine = VarchyEngine(tmp_path)
    meta = engine.initialize_project(
        name="InterviewApp",
        description="Testing interactive interview",
        mode=GenerationMode.INTERACTIVE,
    )
    provider = MockAIProvider()

    prompts_received = []

    def mock_prompt_callback(prompt: str, defaults: list[str]) -> str:
        prompts_received.append(prompt)
        return "Custom User Choice"

    ctx = StageContext(
        workspace=ws,
        provider=provider,
        metadata=meta,
        mode=GenerationMode.INTERACTIVE,
        prompt_callback=mock_prompt_callback,
    )

    stage = ClarificationStage()
    assumptions = await stage.execute(ctx)

    assert len(prompts_received) == 4
    assert len(assumptions) == 4
    assert all(a.confirmed is True for a in assumptions)
    assert any("Custom User Choice" in a.statement for a in assumptions)


def test_cli_update_requirement_incremental(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    # Init and generate blueprint
    runner.invoke(app, ["init", "--name", "UpdateApp", "--desc", "Testing updates"])
    runner.invoke(app, ["generate", "--idea", "Testing updates", "--provider", "mock"])

    # Update REQ-001
    res = runner.invoke(app, ["update", "--requirement", "REQ-001", "--title", "Updated Enterprise Engine", "--desc", "Brand new description"])
    assert res.exit_code == 0
    assert "Updated requirement [REQ-001] successfully" in res.stdout

    # Verify updated content in compiled prd.md
    prd_text = (tmp_path / "docs" / "01-product" / "prd.md").read_text()
    assert "Updated Enterprise Engine" in prd_text


def test_doc_compiler_generates_mermaid_diagrams(tmp_path):
    ws = WorkspaceManager(tmp_path)
    compiler = DocCompiler(ws)
    bp = MockAIProvider.generate_mock_blueprint()

    files = compiler.compile_all(bp)

    # Check architecture.md has Mermaid diagram
    arch_content = files["architecture"].read_text()
    assert "```mermaid" in arch_content
    assert "flowchart TD" in arch_content

    # Check database.md was generated with ER diagram
    db_content = files["database"].read_text()
    assert "## Schema Definitions" in db_content
    assert "| Column | Data Type | Key | Nullable |" in db_content
