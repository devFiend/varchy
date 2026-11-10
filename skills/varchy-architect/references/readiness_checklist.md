# Varchy 100-Point Deterministic Readiness Gate

Before any implementation code is generated, the architectural blueprint must be audited against this 100-point deterministic rubric.

---

## Scoring Breakdown (100 Maximum Points)

### 1. Requirement Completeness & Traceability (20 Points)
* **[5 pts]** Every requirement has a globally unique, immutable ID (`REQ-001`..`REQ-n`).
* **[5 pts]** Every requirement has explicit, testable acceptance criteria.
* **[5 pts]** Every requirement has an assigned priority (`critical`, `high`, `medium`, `low`).
* **[5 pts]** Every implementation task in Phase 2+ maps back to at least one `REQ-xxx` ID.

### 2. Dependency Graph Acyclicity & Integrity (20 Points)
* **[10 pts]** Zero circular dependencies exist in the task graph (strictly acyclic DAG).
* **[5 pts]** Every prerequisite referenced in `dependencies: [...]` exists as a valid `TASK-xxx`.
* **[5 pts]** Tasks are grouped into logical, sequenced development phases (Foundations $\rightarrow$ Data $\rightarrow$ UI $\rightarrow$ QA).

### 3. Data Model & Schema Consistency (20 Points)
* **[5 pts]** All database entities have unique IDs (`ENT-001`..`ENT-n`) and designated primary keys.
* **[5 pts]** Every foreign key relationship points to an existing parent entity.
* **[5 pts]** Field data types, nullability, and unique constraints are explicitly defined.
* **[5 pts]** Database indexing strategy is defined for high-cardinality and query-heavy fields.

### 4. API Contract Precision (20 Points)
* **[5 pts]** All endpoints have unique IDs (`API-001`..`API-n`) with HTTP method and path.
* **[5 pts]** Request body schemas specify validation rules and mandatory fields.
* **[5 pts]** Expected response payloads include HTTP status codes (200, 201, 400, 401, 403, 404, 500).
* **[5 pts]** Every frontend state mutation in UI specs is backed by a corresponding API endpoint.

### 5. UI State Coverage (10 Points)
* **[5 pts]** Every screen has a designated route and unique ID (`SCREEN-001`..`SCREEN-n`).
* **[5 pts]** All four fundamental states (Empty, Loading, Success, Error) are specified per screen.

### 6. Testing & Quality Strategy (10 Points)
* **[5 pts]** Unit and integration test specifications exist for all critical business logic.
* **[5 pts]** Happy path and failure mode test cases are documented.

---

## Gate Verdict Thresholds

| Score Range | Status | Action |
|:---:|:---:|---|
| **85 – 100** | **PASSED (Production Ready)** | Blueprint is locked. Hand off task `TASK-001` to coding agent for implementation. |
| **70 – 84** | **PROVISIONAL** | Review warnings. Clarify ambiguous requirements before coding Phase 2. |
| **0 – 69** | **FAILED (Blocked)** | Architectural gaps detected. Re-run refinement and validation before writing code. |

