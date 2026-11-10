---
name: varchy-architect
description: Autonomous AI Software Architect & Development Orchestrator. Transforms one-sentence software ideas into complete, mathematically validated engineering blueprints, PRDs, database schemas, and DAG task roadmaps before a single line of code is written.
---

# 🏛️ Varchy: AI Software Architect & Planning Orchestrator

The **Varchy Architect Skill** equips coding agents (Claude Code, Cursor, GitHub Copilot, Gemini CLI) with a principal-level software architecture and project decomposition protocol.

It prevents the *"vibe coding hangover"*—where agents hallucinate schemas on the fly, introduce conflicting API routes, omit authentication, fill up context windows, and produce spaghetti code.

---

## ⚡ When to Activate This Skill

Activate this skill whenever the user asks to:
* **Architect or plan a new application** from an idea or brief.
* **Generate a Product Requirements Document (PRD)** or feature specifications.
* **Design database schemas, entity relationships, or API contracts**.
* **Decompose a project into a phased dependency task DAG**.
* **Create universal agent instruction files** (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`).
* **Audit an existing project architecture** for missing edge cases or circular dependencies.

---

## 🏗️ The 7-Stage Architectural Protocol

When triggered, execute the architecture lifecycle through 7 discrete, verifiable stages:

```
[1. Discovery] ──> [2. Product (PRD)] ──> [3. UI/UX Specs] ──> [4. Architecture]
                                                                      │
[7. QA Strategy] <── [6. Task Graph (DAG)] <── [5. Data & APIs] <─────┘
```

### Stage 1: Discovery & Clarification
* Extract core problem statement, target audience, and primary success metrics.
* Identify hard architectural constraints: latency targets, offline requirements, security/compliance (e.g. HIPAA, GDPR, SOC2), and deployment environment.
* Select archetype template from `templates/` (`saas.md`, `api_backend.md`, or `local_first.md`).

### Stage 2: Product Requirements Document (PRD)
* Assign immutable, globally unique IDs (`REQ-001`, `REQ-002`, ...).
* Define user personas and prioritized user journeys.
* Specify non-functional requirements (throughput, p99 latency, SLA).
* Output file: `docs/01-product/prd.md`.

### Stage 3: UI/UX & Interaction Design
* Assign screen IDs (`SCREEN-001`, `SCREEN-002`, ...).
* Map all user interaction flows and component hierarchy.
* Detail all 4 fundamental UI states for every screen:
  1. **Empty state** (initial onboarding / no data)
  2. **Loading state** (skeleton loader / progress indicator)
  3. **Success state** (data rendered with interaction affordances)
  4. **Error state** (retry mechanics, network drop handling)
* Output file: `docs/02-design/screens.md`.

### Stage 4: Engineering & Component Architecture
* High-level architectural pattern (Modular Monolith, Event-Driven, Microservices, or Local-First).
* Component breakdown, data flow, and Mermaid sequence diagrams.
* Technology stack selection with architectural justification for each layer.
* Output file: `docs/03-engineering/architecture.md`.

### Stage 5: Data Models & API Contracts
* Relational / document schemas with explicit types, primary keys, foreign keys, and indexes.
* Assign entity IDs (`ENT-001`, `ENT-002`, ...).
* RESTful or GraphQL endpoints with method, route, request payload, response schema, and error codes.
* Assign API IDs (`API-001`, `API-002`, ...).
* Output file: `docs/03-engineering/database.md`.

### Stage 6: Implementation Task Graph (DAG)
* Decompose implementation into strictly ordered phases:
  * **Phase 1: Foundation & Infrastructure** (scaffolding, auth, database setup)
  * **Phase 2: Core Data & APIs** (models, migrations, backend endpoints)
  * **Phase 3: User Interface & State** (components, pages, client store)
  * **Phase 4: Integration & Edge Cases** (end-to-end flows, error boundaries)
* Assign task IDs (`TASK-001`, `TASK-002`, ...).
* **Strict Rule:** Every task MUST reference prerequisite task IDs (`dependencies: ["TASK-001"]`).
* **Strict Rule:** Zero circular dependencies permitted. Tasks must form a Directed Acyclic Graph (DAG).
* Output file: `docs/04-development/tasks.md`.

### Stage 7: Quality Assurance & Testing Strategy
* Unit test targets, integration test suites, and end-to-end user acceptance tests.
* Detailed test cases mapped back to `REQ-xxx` IDs.
* Output file: `docs/05-quality/testing.md`.

---

## 📄 Universal Agent Rules Generation

At the conclusion of the architectural phase, generate universal agent instruction files in the project root:

1. **`AGENTS.md`**: Universal cross-agent operational rules (formatting, conventions, execution sequence).
2. **`CLAUDE.md`**: Optimized rules for Claude Code and Anthropic models.
3. **`.cursorrules`**: Context-efficient rules for Cursor IDE.
4. **`.github/copilot-instructions.md`**: Directives for GitHub Copilot.

---

## 🎯 100-Point Deterministic Readiness Gate

Before considering any architecture complete, verify compliance against the 100-point gate:

| Dimension | Points | Criteria |
|---|:---:|---|
| **Requirement Traceability** | 20 | Every task in Phase 2+ maps to at least one `REQ-xxx` ID. |
| **DAG Integrity** | 20 | Zero circular dependencies. Every task has verifiable completion criteria. |
| **Schema Completeness** | 20 | All foreign keys have corresponding parent entities. All fields are typed. |
| **API Contract Consistency** | 20 | Every frontend mutation has a corresponding backend API endpoint (`API-xxx`). |
| **UI State Coverage** | 10 | Every screen specifies Empty, Loading, Success, and Error states. |
| **Testing Coverage** | 10 | Critical business logic has corresponding test specifications. |

*(Readiness score MUST reach $\ge 85/100$ before implementation code is written).*

---

## 🛠️ CLI Power-User Integration (Optional)

Developers with Python installed can also use the open-source **Varchy CLI** for automated offline generation and deterministic scoring:

```bash
# Install from PyPI
pip install varchy

# Generate blueprint via CLI
varchy generate --idea "Uber for dog walkers" --template saas

# Run 100-point deterministic validation engine
varchy validate

# Determine next actionable task in DAG
varchy task next
```

*Open Source Repository:* [github.com/devFiend/varchy](https://github.com/devFiend/varchy)
