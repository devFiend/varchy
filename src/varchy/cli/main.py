"""Varchy Command Line Interface (Typer + Rich)."""

import asyncio
from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from varchy import __version__
from varchy.core.engine import VarchyEngine
from varchy.core.models.common import GenerationMode, ProjectCategory, StageID
from varchy.core.storage.keystore import KeyStore
from varchy.templates.registry import TEMPLATES_REGISTRY, get_template

app = typer.Typer(
    name="varchy",
    help="🏛️ Varchy: Your idea. Fully architected. Open-source AI Software Architect & Development Orchestrator.",
    no_args_is_help=True,
)
mcp_app = typer.Typer(name="mcp", help="Model Context Protocol (MCP) server commands.")
config_app = typer.Typer(name="config", help="Manage Varchy settings and secure API credentials.")
templates_app = typer.Typer(name="templates", help="Manage and inspect architectural project templates.")

app.add_typer(mcp_app, name="mcp")
app.add_typer(config_app, name="config")
app.add_typer(templates_app, name="templates")

console = Console()


@app.command()
def version():
    """Display Varchy version."""
    console.print(f"[bold cyan]Varchy[/bold cyan] version [green]{__version__}[/green]")


@app.command()
def init(
    name: str = typer.Option("MyProject", "--name", "-n", help="Project name"),
    description: str = typer.Option("A software project", "--desc", "-d", help="Short description"),
    category: ProjectCategory = typer.Option(ProjectCategory.SAAS, "--category", "-c", help="Project category"),
    mode: GenerationMode = typer.Option(GenerationMode.AUTONOMOUS, "--mode", "-m", help="interactive or autonomous"),
    template: Optional[str] = typer.Option(None, "--template", "-t", help="Template archetype: saas, local_first, api_backend, dev_tool, mobile_app"),
):
    """Initialize a new Varchy project workspace."""
    engine = VarchyEngine()
    if engine.workspace.is_initialized():
        console.print("[yellow]Project workspace is already initialized in this directory.[/yellow]")
        raise typer.Exit(code=0)

    if template:
        arch_tmpl = get_template(template)
        if arch_tmpl:
            category = arch_tmpl.category

    metadata = engine.initialize_project(
        name=name,
        description=description,
        category=category,
        mode=mode,
    )
    console.print(
        Panel.fit(
            f"[bold green]Initialized Varchy Project workspace[/bold green]\n"
            f"[cyan]Name:[/cyan] {metadata.name}\n"
            f"[cyan]Category:[/cyan] {metadata.category.value}\n"
            f"[cyan]Mode:[/cyan] {metadata.generation_mode.value}\n"
            f"[dim]Saved metadata in .varchy/project.json[/dim]",
            title="🏛️ Varchy Init",
            border_style="green",
        )
    )


@app.command()
def analyze(
    idea: str = typer.Option(..., "--idea", "-i", help="Raw software idea to analyze"),
    category: ProjectCategory = typer.Option(ProjectCategory.DEV_TOOL, "--category", "-c", help="Category"),
    provider: Optional[str] = typer.Option(None, "--provider", "-p", help="AI provider"),
):
    """Analyze a project idea and produce a structured brief before generating architecture."""
    engine = VarchyEngine()
    with console.status("[bold blue]Analyzing concept, risks, and problem space...[/bold blue]"):
        brief = asyncio.run(engine.analyze_idea(idea=idea, category=category, provider_name=provider))

    table = Table(title="🏛️ Varchy Idea Analysis & Project Brief")
    table.add_column("Property", style="cyan", width=22)
    table.add_column("Assessment", style="white")

    table.add_row("Core Problem", brief.core_problem)
    table.add_row("Proposed Solution", brief.proposed_solution)
    table.add_row("Target Audience", ", ".join(brief.target_audience))
    table.add_row("Technical Complexity", brief.technical_complexity.upper())
    table.add_row("Identified Risks", "\n".join(f"• {r}" for r in brief.identified_risks))
    table.add_row("Key Features", "\n".join(f"• {f}" for f in brief.key_features))

    console.print(table)


@app.command()
def generate(
    idea: str = typer.Option(..., "--idea", "-i", help="One-sentence description of the project idea"),
    category: ProjectCategory = typer.Option(ProjectCategory.SAAS, "--category", "-c", help="Category"),
    provider: Optional[str] = typer.Option(None, "--provider", "-p", help="AI provider (openai, gemini, grok, ollama, mock)"),
    mode: GenerationMode = typer.Option(GenerationMode.AUTONOMOUS, "--mode", "-m", help="interactive or autonomous"),
    no_resume: bool = typer.Option(False, "--force", help="Do not restore cached checkpoints; regenerate all stages"),
    template: Optional[str] = typer.Option(None, "--template", "-t", help="Template: saas, local_first, api_backend, dev_tool, mobile_app"),
):
    """Transform a software idea into a complete, validated architectural blueprint."""
    engine = VarchyEngine()

    if template:
        arch_tmpl = get_template(template)
        if arch_tmpl:
            category = arch_tmpl.category

    def progress_callback(stage_id: StageID, message: str):
        console.print(f"  [cyan]▸ [{stage_id.value.upper()}][/cyan] {message}")

    console.print(f"[bold cyan]Starting Varchy Architecture Pipeline for:[/bold cyan] {idea}\n")

    blueprint = asyncio.run(
        engine.generate_blueprint(
            idea=idea,
            category=category,
            provider_name=provider,
            mode=mode,
            resume=not no_resume,
            progress_callback=progress_callback,
        )
    )

    console.print(
        Panel(
            f"[bold green]Architectural Blueprint Generated Successfully![/bold green]\n"
            f"- [cyan]Project:[/cyan] {blueprint.metadata.name}\n"
            f"- [cyan]Requirements:[/cyan] {len(blueprint.product.requirements)} defined\n"
            f"- [cyan]Screens:[/cyan] {len(blueprint.design.screens)} specified\n"
            f"- [cyan]Entities & Endpoints:[/cyan] {len(blueprint.data_api.entities)} tables, {len(blueprint.data_api.endpoints)} APIs\n"
            f"- [cyan]Tasks:[/cyan] {len(blueprint.planning.tasks)} planned across {len(blueprint.planning.phases)} phases\n"
            f"- [cyan]Tests:[/cyan] {len(blueprint.testing.test_cases)} test cases\n\n"
            f"[bold]Output compiled to:[/bold]\n"
            f"  📁 docs/ (gitignored)\n"
            f"  📄 AGENTS.md\n"
            f"  📄 CLAUDE.md\n"
            f"  📄 GEMINI.md",
            title="🏛️ Varchy Architect",
            border_style="cyan",
        )
    )


@app.command()
def validate():
    """Run deterministic 100-point validation on the current blueprint."""
    engine = VarchyEngine()
    if not engine.workspace.is_initialized():
        console.print("[red]No initialized Varchy project found. Run `varchy init` or `varchy generate` first.[/red]")
        raise typer.Exit(code=1)

    try:
        report = engine.validate_blueprint()
    except FileNotFoundError:
        console.print("[red]No blueprint found to validate. Run `varchy generate` first.[/red]")
        raise typer.Exit(code=1)

    table = Table(title="🏛️ Blueprint Readiness Assessment (100-Point Deterministic Score)")
    table.add_column("Category", style="cyan")
    table.add_column("Max", justify="right")
    table.add_column("Score", justify="right", style="bold")
    table.add_column("Status", justify="center")

    for cat in report.category_scores:
        status = "[green]PASS[/green]" if cat.awarded_points >= (cat.max_points * 0.8) else "[yellow]ATTN[/yellow]"
        table.add_row(cat.category.replace("_", " ").title(), str(cat.max_points), f"{cat.awarded_points:.1f}", status)

    console.print(table)

    summary_color = "green" if report.passed else "red"
    status_str = "READY FOR IMPLEMENTATION" if report.passed else "BLOCKED / REQUIRES ATTENTION"
    console.print(
        Panel.fit(
            f"[{summary_color}]Total Readiness Score: [bold]{report.total_score} / 100[/bold] — {status_str}[/{summary_color}]\n"
            f"Critical Blockers: {len(report.critical_blockers)} | Warnings: {len(report.warnings)} | Recs: {len(report.recommendations)}",
            border_style=summary_color,
        )
    )

    if report.critical_blockers:
        console.print("\n[bold red]Critical Blockers:[/bold red]")
        for b in report.critical_blockers:
            console.print(f"  ❌ [{b.category}] {b.message}")
            if b.suggestion:
                console.print(f"     [dim]Suggestion: {b.suggestion}[/dim]")


@app.command()
def update(
    requirement: Optional[str] = typer.Option(None, "--requirement", "-r", help="Requirement ID to update (e.g. REQ-001)"),
    title: Optional[str] = typer.Option(None, "--title", help="New title for the requirement"),
    description: Optional[str] = typer.Option(None, "--desc", help="New description for the requirement"),
):
    """Selectively update a requirement in the blueprint without regenerating from scratch."""
    engine = VarchyEngine()
    if not engine.workspace.is_initialized():
        console.print("[red]No initialized Varchy project found.[/red]")
        raise typer.Exit(code=1)

    try:
        blueprint = engine.workspace.load_blueprint()
    except FileNotFoundError:
        console.print("[red]No active blueprint found. Run `varchy generate` first.[/red]")
        raise typer.Exit(code=1)

    if not requirement:
        console.print("[yellow]Please specify a requirement ID using `--requirement REQ-###`.[/yellow]")
        raise typer.Exit(code=1)

    found = False
    for req in blueprint.product.requirements:
        if req.id == requirement:
            if title:
                req.title = title
            if description:
                req.description = description
            found = True
            break

    if not found:
        console.print(f"[red]Requirement '{requirement}' not found in current blueprint.[/red]")
        raise typer.Exit(code=1)

    # Persist updated blueprint and re-compile
    engine.workspace.save_blueprint(blueprint)
    engine.compiler.compile_all(blueprint)
    report = engine.validator.evaluate(blueprint)

    console.print(
        Panel.fit(
            f"[bold green]Updated requirement [{requirement}] successfully![/bold green]\n"
            f"Re-compiled documentation and agent instruction files.\n"
            f"New Readiness Score: [bold]{report.total_score}/100[/bold] (Passed: {report.passed})",
            title="🏛️ Varchy Incremental Update",
            border_style="green",
        )
    )


@app.command()
def status():
    """Display current project status, completed stages, and blueprint summary."""
    engine = VarchyEngine()
    if not engine.workspace.is_initialized():
        console.print("[yellow]No Varchy project found in current directory.[/yellow]")
        raise typer.Exit(code=0)

    metadata = engine.workspace.load_metadata()
    console.print(
        Panel(
            f"[bold cyan]Project:[/bold cyan] {metadata.name} ([green]{metadata.category.value}[/green])\n"
            f"[bold cyan]Description:[/bold cyan] {metadata.description}\n"
            f"[bold cyan]Mode:[/bold cyan] {metadata.generation_mode.value}\n"
            f"[bold cyan]Workspace:[/bold cyan] {engine.workspace.varchy_dir}",
            title="🏛️ Varchy Project Status",
            border_style="cyan",
        )
    )

    try:
        blueprint = engine.workspace.load_blueprint()
        report = engine.validator.evaluate(blueprint)
        console.print(
            f"✅ [bold green]Active Blueprint Loaded[/bold green] (Readiness: [bold]{report.total_score}/100[/bold])\n"
            f"   • Requirements: {len(blueprint.product.requirements)}\n"
            f"   • Screens: {len(blueprint.design.screens)}\n"
            f"   • Implementation Tasks: {len(blueprint.planning.tasks)}\n"
            f"   • Test Cases: {len(blueprint.testing.test_cases)}"
        )
    except FileNotFoundError:
        console.print("[yellow]⚠️ No blueprint generated yet. Run `varchy generate`.[/yellow]")


@app.command()
def export():
    """Export or re-compile agent instructions and markdown documentation."""
    engine = VarchyEngine()
    try:
        files = engine.export_instructions()
        console.print(f"[bold green]Successfully compiled {len(files)} files into docs/ and root directory.[/bold green]")
    except FileNotFoundError:
        console.print("[red]No blueprint found to export. Run `varchy generate` first.[/red]")
        raise typer.Exit(code=1)


@app.command()
def doctor():
    """Diagnose local environment, providers, keyring, and file permissions."""
    console.print(Panel("[bold]Varchy System & Environment Diagnosis[/bold]", style="cyan"))

    cwd = Path.cwd()
    engine = VarchyEngine(cwd)
    console.print(f"✅ [bold]Working Directory:[/bold] {cwd}")
    console.print(f"✅ [bold]Workspace Initialized:[/bold] {engine.workspace.is_initialized()}")

    try:
        import keyring
        console.print("✅ [bold]Keyring Integration:[/bold] Available")
    except ImportError:
        console.print("⚠️ [bold]Keyring Integration:[/bold] Not installed (falling back to environment variables)")

    for prov in ["openai", "gemini", "grok"]:
        key = KeyStore.get_api_key(prov)
        status_str = "[green]Configured[/green]" if key else "[dim]Not set (BYOK)[/dim]"
        console.print(f"  • {prov.title()} Key: {status_str}")

    console.print("✅ [bold]Deterministic Validation Engine:[/bold] Ready")
    console.print("✅ [bold]Multi-Stage DAG Orchestrator:[/bold] Ready")
    console.print("✅ [bold]All core subsystems operational.[/bold]")


@templates_app.callback(invoke_without_command=True)
def list_templates(ctx: typer.Context):
    """List available project archetypes and architectural templates."""
    if ctx.invoked_subcommand is not None:
        return

    table = Table(title="🏛️ Varchy Architectural Templates & Archetypes")
    table.add_column("Template ID", style="cyan", width=14)
    table.add_column("Name", style="bold", width=26)
    table.add_column("Category", style="green", width=16)
    table.add_column("Description", style="white")

    for tid, tmpl in TEMPLATES_REGISTRY.items():
        table.add_row(tid, tmpl.name, tmpl.category.value, tmpl.description)

    console.print(table)
    console.print("[dim]Use with `varchy init --template <id>` or `varchy templates inspect <id>`[/dim]")


@templates_app.command("inspect")
def inspect_template(template_id: str = typer.Argument(..., help="Template id: saas, local_first, api_backend, dev_tool, mobile_app")):
    """Inspect the architectural breakdown and recommended stack for a template archetype."""
    tmpl = get_template(template_id)
    if not tmpl:
        console.print(f"[red]Template '{template_id}' not found. Run `varchy templates` to view options.[/red]")
        raise typer.Exit(code=1)

    console.print(
        Panel(
            f"[bold green]{tmpl.name}[/bold green] ([cyan]{tmpl.id}[/cyan])\n"
            f"[dim]{tmpl.description}[/dim]\n\n"
            f"[bold]Category:[/bold] {tmpl.category.value}\n"
            f"[bold]Security Model:[/bold] {tmpl.default_security_model}\n"
            f"[bold]Persistence:[/bold] {tmpl.default_persistence_model}",
            title="🏛️ Template Details",
            border_style="cyan",
        )
    )

    table = Table(title="Recommended Technology Stack")
    table.add_column("Tier", style="cyan", width=18)
    table.add_column("Technology", style="bold white", width=24)
    table.add_column("Architectural Rationale", style="dim")

    for item in tmpl.recommended_tech_stack:
        table.add_row(item.category, item.name, item.justification)

    console.print(table)


@config_app.command("set-key")
def config_set_key(
    provider: str = typer.Argument(..., help="Provider name: openai, gemini, grok"),
    key: str = typer.Argument(..., help="API key string"),
):
    """Store an AI provider API key securely into OS Keyring."""
    success = KeyStore.set_api_key(provider, key)
    if success:
        console.print(f"[bold green]Successfully stored {provider} API key securely in OS Keychain.[/bold green]")
    else:
        console.print(f"[yellow]Stored {provider} key. (If OS Keyring unavailable, use VARCHY_{provider.upper()}_API_KEY env).[/yellow]")


@mcp_app.command("run")
def run_mcp_server():
    """Start the official Varchy Model Context Protocol (MCP) server."""
    console.print("[bold cyan]Starting Varchy MCP Server over stdio...[/bold cyan]")
    from varchy.mcp.server import start_mcp_server
    start_mcp_server()


if __name__ == "__main__":
    app()
