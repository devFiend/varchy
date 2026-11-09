"""Tests for multi-stage DAG orchestrator, stage execution, and checkpointing."""

import pytest
from varchy.core.models.common import GenerationMode, ProjectCategory, StageID
from varchy.core.models.project import ProjectMetadata
from varchy.core.pipeline.context import StageContext
from varchy.core.pipeline.orchestrator import PipelineOrchestrator
from varchy.core.pipeline.stages.architecture import ArchitectureStage
from varchy.core.pipeline.stages.clarification import ClarificationStage
from varchy.core.pipeline.stages.data_api import DataApiStage
from varchy.core.pipeline.stages.discovery import DiscoveryStage
from varchy.core.pipeline.stages.planning import PlanningStage
from varchy.core.pipeline.stages.product import ProductStage
from varchy.core.pipeline.stages.qa import QAStage
from varchy.core.pipeline.stages.ux import UXStage
from varchy.core.storage.workspace import WorkspaceManager
from varchy.providers.mock import MockAIProvider


@pytest.fixture
def workspace(tmp_path):
    ws = WorkspaceManager(tmp_path)
    meta = ProjectMetadata(
        name="PipelineTestProject",
        slug="pipelinetest",
        description="A distributed task queue with real-time telemetry",
        category=ProjectCategory.DEV_TOOL,
    )
    ws.initialize(meta)
    return ws


@pytest.mark.asyncio
async def test_all_pipeline_stages_execute_in_sequence(workspace):
    provider = MockAIProvider()
    meta = workspace.load_metadata()
    ctx = StageContext(workspace=workspace, provider=provider, metadata=meta)

    # 1. Discovery
    brief = await DiscoveryStage().execute(ctx)
    assert brief is not None
    assert brief.core_problem != ""

    # 2. Clarification
    assumptions = await ClarificationStage().execute(ctx)
    assert len(assumptions) > 0
    assert assumptions[0].id.startswith("ASM-")

    # 3. Product
    product = await ProductStage().execute(ctx)
    assert len(product.requirements) > 0
    assert product.requirements[0].id.startswith("REQ-")

    # 4. UX
    design = await UXStage().execute(ctx)
    assert len(design.screens) > 0
    assert design.screens[0].id.startswith("SCREEN-")

    # 5. Architecture
    arch = await ArchitectureStage().execute(ctx)
    assert len(arch.tech_stack) > 0

    # 6. Data & API
    data_api = await DataApiStage().execute(ctx)
    assert len(data_api.entities) > 0
    assert len(data_api.endpoints) > 0

    # 7. Planning
    planning = await PlanningStage().execute(ctx)
    assert len(planning.phases) > 0
    assert len(planning.tasks) > 0
    assert planning.tasks[0].id.startswith("TASK-")

    # 8. QA
    qa = await QAStage().execute(ctx)
    assert len(qa.test_cases) > 0
    assert qa.test_cases[0].id.startswith("TEST-")


@pytest.mark.asyncio
async def test_pipeline_orchestrator_checkpointing_and_resumption(workspace):
    provider = MockAIProvider()
    meta = workspace.load_metadata()

    logged_stages = []

    def on_progress(stage_id: StageID, msg: str):
        logged_stages.append(stage_id)

    orchestrator = PipelineOrchestrator(
        workspace=workspace,
        provider=provider,
        metadata=meta,
        mode=GenerationMode.AUTONOMOUS,
    )

    # First run: executes all stages and creates checkpoints
    blueprint = await orchestrator.run(resume=True, progress_callback=on_progress)
    assert blueprint is not None
    assert (workspace.checkpoints_dir / "discovery.json").exists()
    assert (workspace.checkpoints_dir / "qa.json").exists()

    # Second run: should restore checkpoints from disk without re-executing
    second_logged = []

    def on_second_progress(stage_id: StageID, msg: str):
        second_logged.append(msg)

    second_orchestrator = PipelineOrchestrator(
        workspace=workspace,
        provider=provider,
        metadata=meta,
    )
    second_bp = await second_orchestrator.run(resume=True, progress_callback=on_second_progress)
    assert second_bp is not None

    # Verify that checkpoints were restored
    restored_msgs = [m for m in second_logged if "Restoring cached checkpoint" in m]
    assert len(restored_msgs) == 8

