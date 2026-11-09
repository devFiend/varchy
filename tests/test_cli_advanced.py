"""Tests for advanced CLI commands: analyze, status, config, providers, models."""

from typer.testing import CliRunner
from varchy.cli.main import app

runner = CliRunner()


def test_cli_analyze_command():
    result = runner.invoke(app, ["analyze", "--idea", "A distributed cache server in Rust"])
    assert result.exit_code == 0
    assert "Idea Analysis & Project Brief" in result.stdout
    assert "Core Problem" in result.stdout
    assert "Proposed Solution" in result.stdout


def test_cli_status_uninitialized(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["status"])
    assert result.exit_code == 0
    assert "No Varchy project found" in result.stdout


def test_cli_status_initialized_and_generated(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    # Init
    runner.invoke(app, ["init", "--name", "StatusApp", "--desc", "Status testing"])
    # Generate
    runner.invoke(app, ["generate", "--idea", "Status testing project", "--provider", "mock"])
    # Status
    result = runner.invoke(app, ["status"])
    assert result.exit_code == 0
    assert "StatusApp" in result.stdout
    assert "Active Blueprint Loaded" in result.stdout
    assert "Readiness:" in result.stdout


def test_cli_config_set_key():
    result = runner.invoke(app, ["config", "set-key", "openai", "sk-test-key-12345"])
    assert result.exit_code == 0
    assert "Stored" in result.stdout or "Successfully stored" in result.stdout


def test_cli_providers_command():
    result = runner.invoke(app, ["providers"])
    assert result.exit_code == 0
    assert "Supported AI Providers" in result.stdout
    assert "OpenAI" in result.stdout
    assert "Google Gemini" in result.stdout
    assert "xAI Grok" in result.stdout
    assert "Ollama" in result.stdout


def test_cli_models_command():
    result = runner.invoke(app, ["models"])
    assert result.exit_code == 0
    assert "AI Models per Provider" in result.stdout
    assert "gpt-4o" in result.stdout
    assert "gemini-2.5-pro" in result.stdout
