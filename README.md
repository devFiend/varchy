# VARCHY 🏛️
### *Your idea. Fully architected.*

<p align="center">
  <a href="https://github.com/varchy-org/varchy"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.15-blue" alt="Python 3.12+"></a>
  <a href="https://modelcontextprotocol.io"><img src="https://img.shields.io/badge/MCP-Protocol%20Ready-purple" alt="MCP Ready"></a>
  <a href="#"><img src="https://img.shields.io/badge/Tests-16%2F16%20Passing-brightgreen" alt="Tests"></a>
  <a href="#"><img src="https://img.shields.io/badge/Readiness%20Engine-100%20pt%20Deterministic-emerald" alt="Readiness Engine"></a>
  <a href="#"><img src="https://img.shields.io/badge/BYOK-Zero%20Telemetry-orange" alt="Zero Telemetry"></a>
</p>

<p align="center">
  <strong>Varchy</strong> is the open-source software architect and planning orchestrator for the AI coding era.<br>
  It transforms a <strong>one-sentence idea</strong> into a complete, structured, mathematically validated, and implementation-ready engineering blueprint before a single line of application code is written.
</p>

---

## ⚡ The Problem: The "Vibe Coding" Hangover

AI coding assistants (Claude Code, Cursor, Copilot, Codex) write code in seconds. But without upfront architecture, developers face the same recurring disaster:

```
❌ Vibe Coding Without Architecture:
   Prompt: "Build me an Uber for dog walkers"
     ↳ Agent hallucinates database models on the fly
     ↳ Screen routes conflict with backend API contracts
     ↳ Edge cases and authentication are completely ignored
     ↳ Context window fills up -> Agent forgets earlier decisions
     ↳ Hours wasted debugging spaghetti code
```

```
✅ Vibe Coding With Varchy:
   Command: varchy generate --idea "Uber for dog walkers"
     ↳ Structured PRD with stable requirement IDs (REQ-001)
     ↳ Screen specs & interaction states (SCREEN-001)
     ↳ Relational schemas & API contracts (ENT-001, API-001)
     ↳ Phased task DAG with zero circular dependencies (TASK-001)
     ↳ 100-Point Deterministic Readiness Gate
     ↳ Exported AGENTS.md, CLAUDE.md, and GEMINI.md
     ↳ Your coding agent implements tasks in perfect sequence!
```

---

## 🚀 30-Second Quickstart

### 1. Installation

```bash
pip install varchy
```

### 2. Analyze an Idea (Fast Brief Assessment)

```bash
varchy analyze --idea "A local-first encrypted collaborative markdown workspace"
```

### 3. Generate Complete Architecture Blueprint (Multi-Stage DAG)

```bash
varchy generate --idea "A local-first encrypted collaborative markdown workspace"
```

*Note: Runs with automatic stage checkpointing (`.varchy/checkpoints/`). If interrupted, re-running resumes from the last completed stage. Use `--force` to regenerate all stages.*

### 4. Run the 100-Point Deterministic Readiness Gate

```bash
varchy validate
```

```text
       🏛️ Blueprint Readiness Assessment (100-Point Deterministic Score)
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━┳━━━━━━━┳━━━━━━━━┓
┃ Category                    ┃ Max ┃ Score ┃ Status ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━╇━━━━━━━╇━━━━━━━━┩
│ Product Requirements        │  20 │  20.0 │  PASS  │
│ Technical Architecture      │  20 │  20.0 │  PASS  │
│ UI/UX Specifications        │  15 │  15.0 │  PASS  │
│ Development Planning        │  15 │  15.0 │  PASS  │
│ Database & API Contracts    │  10 │  10.0 │  PASS  │
│ Testing Strategy            │  10 │  10.0 │  PASS  │
│ Security & Deployment       │  10 │  10.0 │  PASS  │
└─────────────────────────────┴─────┴───────┴────────┘
Total Readiness Score: 100.0 / 100 — READY FOR IMPLEMENTATION
Critical Blockers: 0 | Warnings: 0 | Recommendations: 0
```

### 5. Check Project Status & Completed Stages

```bash
varchy status
```

---

## 🛠️ Complete CLI Command Reference

| Command | Description | Example |
|---|---|---|
| `varchy init` | Initialize project workspace & metadata | `varchy init --name "MyApp" --category saas` |
| `varchy analyze` | Analyze idea, risks, and taxonomy before blueprint generation | `varchy analyze --idea "..."` |
| `varchy generate` | Execute 10-stage architecture DAG pipeline | `varchy generate --idea "..." --provider openai` |
| `varchy validate` | Run 100-point deterministic readiness scoring | `varchy validate` |
| `varchy status` | Show current blueprint health, stages, and metrics | `varchy status` |
| `varchy export` | Re-compile documentation & agent instruction files | `varchy export` |
| `varchy doctor` | Diagnose environment, Keychain, and configured providers | `varchy doctor` |
| `varchy config set-key` | Securely store provider key in OS Keychain | `varchy config set-key openai sk-...` |
| `varchy mcp run` | Launch Model Context Protocol server over stdio | `varchy mcp run` |

---

## 🧠 Core Philosophy & Architecture

Varchy is **not** an AI wrapper that blindly outputs huge blobs of unstructured Markdown. It is built on six 100-level engineering invariants:

1. **Structured Data as the Single Source of Truth:**
   The source of truth is strictly typed, serialized Pydantic v2 schemas (`.varchy/blueprints/`). Markdown documentation (`docs/`) is a compiled, read-only projection.
2. **Unified Core Engine:**
   The CLI (`varchy`) and the MCP Server (`varchy mcp run`) share 100% of business logic through a single `VarchyEngine` orchestrator.
3. **Multi-Stage DAG with Checkpoint Resumability:**
   Execution passes through 10 discrete stages (`Discovery` → `Clarification` → `Product` → `UX` → `Architecture` → `Data & APIs` → `Planning` → `QA` → `Validation` → `Compilation`). Checkpoints are persisted atomically after every stage.
4. **Stable Traceability Matrix:**
   Every structural node maintains an immutable, human-readable stable ID:
   `REQ-###` ⟷ `SCREEN-###` ⟷ `API-###` ⟷ `ENT-###` ⟷ `TASK-###` ⟷ `TEST-###`
5. **Deterministic Readiness Scoring:**
   Readiness is calculated via AST and graph traversal algorithms (including cycle detection for tasks), not subjective LLM opinion.
6. **Zero-Leak Bring-Your-Own-Key (BYOK):**
   Keys are securely stored in your hardware-backed OS Keychain (`keyring`) or local environment variables. Secrets never touch disk, logs, or git.

---

## 🔌 Supported AI Providers

| Provider | Integration | Structured Mode | Configuration |
|---|---|---|---|
| **OpenAI** | API (`gpt-4o`, `gpt-4o-mini`, `o3-mini`) | Native JSON Schema (`strict: true`) | `varchy config set-key openai sk-...` |
| **Google Gemini** | API (`gemini-2.5-pro`, `gemini-2.5-flash`) | Native `responseSchema` | `varchy config set-key gemini AIza...` |
| **Ollama** | Local REST (`http://localhost:11434`) | Native JSON Schema Format | Run `ollama serve` (zero key required) |
| **Mock Provider** | Offline Deterministic Blueprint Engine | Built-in | Used in tests or with `--provider mock` |

---

## 🤖 Model Context Protocol (MCP) Integration

Connect Varchy directly to **Cursor**, **Claude Desktop**, or **Claude Code** as a native MCP server:

### Cursor Configuration (`~/.cursor/mcp.json`)
```json
{
  "mcpServers": {
    "varchy": {
      "command": "varchy",
      "args": ["mcp", "run"]
    }
  }
}
```

### Claude Desktop Configuration (`claude_desktop_config.json`)
```json
{
  "mcpServers": {
    "varchy": {
      "command": "varchy",
      "args": ["mcp", "run"]
    }
  }
}
```

Now you can prompt your agent:  
> *"@varchy validate our architecture blueprint and implement TASK-003."*

---

## 📁 Generated Project Layout

```text
my-project/
├── .varchy/                       # Machine System of Record (Git-ignored)
│   ├── project.json               # Metadata & configuration
│   ├── checkpoints/               # Atomic stage transaction snapshots
│   └── blueprints/current.json    # Master Pydantic domain models
│
├── docs/                          # Compiled Engineering Specifications (Git-ignored)
│   ├── 01-product/                # PRD, requirements, personas
│   ├── 02-design/                 # Design system, screen specs, IA
│   ├── 03-engineering/            # Architecture, DB schema, API contracts
│   ├── 04-development/            # Phased roadmap & tasks (with dependencies)
│   └── 05-quality/                # Test strategies, unit/integration test cases
│
├── AGENTS.md                      # Universal Coding Agent Guidelines
├── CLAUDE.md                      # Claude Code optimized instructions
├── GEMINI.md                      # Gemini CLI optimized instructions
└── README.md                      # Project architectural summary
```

---

## 🧪 Testing & Verification

Varchy is engineered with a comprehensive automated test harness:

```bash
pytest -v
```

```text
tests/test_cli.py::test_cli_version PASSED                               [  6%]
tests/test_cli.py::test_cli_doctor PASSED                                [ 12%]
tests/test_cli.py::test_cli_init_and_generate_workflow PASSED            [ 18%]
tests/test_cli_advanced.py::test_cli_analyze_command PASSED              [ 25%]
tests/test_cli_advanced.py::test_cli_status_uninitialized PASSED         [ 31%]
tests/test_cli_advanced.py::test_cli_status_initialized_and_generated PASSED [ 37%]
tests/test_cli_advanced.py::test_cli_config_set_key PASSED               [ 43%]
tests/test_engine_unified.py::test_engine_init_and_generate PASSED       [ 50%]
tests/test_pipeline_stages.py::test_all_pipeline_stages_execute_in_sequence PASSED [ 56%]
tests/test_pipeline_stages.py::test_pipeline_orchestrator_checkpointing_and_resumption PASSED [ 62%]
tests/test_schemas.py::test_project_metadata_serialization PASSED        [ 68%]
tests/test_schemas.py::test_requirement_model_validation PASSED          [ 75%]
tests/test_schemas.py::test_mock_blueprint_schema_conformance PASSED     [ 81%]
tests/test_validation_engine.py::test_complete_blueprint_passes_validation PASSED [ 87%]
tests/test_validation_engine.py::test_circular_dependency_triggers_critical_blocker PASSED [ 93%]
tests/test_validation_engine.py::test_unconfirmed_high_risk_assumption_blocks_blueprint PASSED [100%]

============================== 16 passed in 0.30s ==============================
```

---

## 🗺️ Roadmap & Implementation Progress

- [x] **v0.1.0:** Core Pydantic schemas, Deterministic 100-pt validation engine, Typer CLI, Mock provider, Agent instruction generator (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`).
- [x] **v0.2.0:** Multi-Stage DAG Orchestrator with Checkpoint Resumability, UX (`SCREEN-###`), Architecture, Data & API (`ENT-###`, `API-###`), Planning (`TASK-###`), and QA (`TEST-###`) stages.
- [x] **v0.3.0:** Live BYOK AI Providers: OpenAI (`gpt-4o`, `o3-mini`), Google Gemini (`2.5/3 Pro`), and Ollama local inference adapter.
- [ ] **v0.4.0:** Interactive discovery interview mode (`varchy init --interactive`).
- [ ] **v0.5.0:** Architectural templates (`varchy templates`) & Incremental blueprint updates (`varchy update`).
- [ ] **v1.0.0:** Varchy Build — Coding agent task execution & drift detection.

---

## 🤝 Contributing

Contributions are warmly welcomed! Please read [CONTRIBUTING.md](CONTRIBUTING.md) to get started.

---

## ⚖️ License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
