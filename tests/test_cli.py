"""Tests for Typer CLI commands."""

from typer.testing import CliRunner
from varchy.cli.main import app

runner = CliRunner()


def test_cli_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "Varchy" in result.stdout


def test_cli_doctor():
    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 0
    assert "System & Environment Diagnosis" in result.stdout


def test_cli_init_and_generate_workflow(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    # Init
    init_res = runner.invoke(app, ["init", "--name", "CLITestApp", "--desc", "Testing CLI"])
    assert init_res.exit_code == 0
    assert "Initialized Varchy Project" in init_res.stdout

    # Generate
    gen_res = runner.invoke(app, ["generate", "--idea", "Testing CLI workflow"])
    assert gen_res.exit_code == 0
    assert "Architectural Blueprint Generated" in gen_res.stdout

    # Validate
    val_res = runner.invoke(app, ["validate"])
    assert val_res.exit_code == 0
    assert "Blueprint Readiness Assessment" in val_res.stdout

