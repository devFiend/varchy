"""Tests for task commands (task list, task next) and Cursor/Copilot instruction generation."""

from typer.testing import CliRunner
from varchy.cli.main import app
from varchy.core.compiler.compiler import DocCompiler
from varchy.core.storage.workspace import WorkspaceManager
from varchy.providers.mock import MockAIProvider

runner = CliRunner()


def test_cursor_and_copilot_files_generated(tmp_path):
    ws = WorkspaceManager(tmp_path)
    compiler = DocCompiler(ws)
    bp = MockAIProvider.generate_mock_blueprint()

    files = compiler.compile_all(bp)

    # Verify .cursorrules was generated
    assert (tmp_path / ".cursorrules").exists()
    cursor_text = files["cursorrules"].read_text()
    assert "Cursor Rules for" in cursor_text
    assert "docs/03-engineering/architecture.md" in cursor_text

    # Verify .github/copilot-instructions.md was generated
    assert (tmp_path / ".github" / "copilot-instructions.md").exists()
    copilot_text = files["copilot_instructions"].read_text()
    assert "GitHub Copilot Instructions for" in copilot_text


def test_cli_task_list_and_task_next(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    # Init and generate blueprint
    runner.invoke(app, ["init", "--name", "TaskApp", "--desc", "Testing tasks"])
    runner.invoke(app, ["generate", "--idea", "Testing tasks", "--provider", "mock"])

    # Task list
    list_res = runner.invoke(app, ["task", "list"])
    assert list_res.exit_code == 0
    assert "Development Tasks & Dependencies" in list_res.stdout
    assert "TASK-001" in list_res.stdout

    # Task next
    next_res = runner.invoke(app, ["task", "next"])
    assert next_res.exit_code == 0
    assert "Next Actionable Implementation Task" in next_res.stdout
    assert "TASK-001" in next_res.stdout
    assert "Completion Criteria:" in next_res.stdout

