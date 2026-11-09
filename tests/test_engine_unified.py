"""Integration tests for the unified VarchyEngine coordinator."""

import pytest
from varchy.core.engine import VarchyEngine
from varchy.core.models.common import GenerationMode, ProjectCategory


@pytest.mark.asyncio
async def test_engine_init_and_generate(tmp_path):
    engine = VarchyEngine(workspace_path=tmp_path)
    assert not engine.workspace.is_initialized()

    # Initialize
    meta = engine.initialize_project(
        name="AgentWorkspace",
        description="A multi-agent development environment",
        category=ProjectCategory.DEV_TOOL,
        mode=GenerationMode.AUTONOMOUS,
    )
    assert engine.workspace.is_initialized()
    assert meta.slug == "agentworkspace"

    # Generate
    bp = await engine.generate_blueprint(
        idea="A multi-agent development environment",
        category=ProjectCategory.DEV_TOOL,
        provider_name="mock",
    )
    assert bp is not None
    assert (tmp_path / ".varchy" / "blueprints" / "current.json").exists()

    # Verify compiled markdown files
    assert (tmp_path / "docs" / "01-product" / "prd.md").exists()
    assert (tmp_path / "docs" / "03-engineering" / "architecture.md").exists()
    assert (tmp_path / "AGENTS.md").exists()
    assert (tmp_path / "CLAUDE.md").exists()
    assert (tmp_path / "GEMINI.md").exists()

    # Validate
    report = engine.validate_blueprint()
    assert report.total_score >= 80.0
    assert report.passed is True

