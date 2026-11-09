# Contributing to Varchy 🏛️

Thank you for your interest in contributing to **Varchy**!

Varchy is an open-source standard for AI-assisted software architecture and development planning. We welcome contributions from developers, architects, and open-source enthusiasts.

---

## 🛠️ Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/varchy.git
   cd varchy
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies with development tools:**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Run the test suite:**
   ```bash
   pytest -v
   ```

---

## 📐 Architectural Principles

When submitting code or features, ensure you follow Varchy's core invariants:

1. **Zero Logic Duplication:** The CLI and MCP server must never implement distinct business logic. Both invoke `VarchyEngine`.
2. **Structured Intelligence First:** Markdown is a compiled view. The source of truth is always validated Pydantic v2 domain schemas (`src/varchy/core/models/`).
3. **Deterministic Readiness Scoring:** Readiness scores are calculated mathematically by `ValidationEngine`, not by asking an LLM for its subjective opinion.
4. **Zero-Leak BYOK:** Never commit API keys or store credentials in plain text. Always use `KeyStore` (OS Keychain with env fallback).

---

## 🧪 Testing Guidelines

- Every new domain schema must include serialization and roundtrip tests in `tests/test_schemas.py`.
- Validation rule additions must include passing and failing test cases in `tests/test_validation_engine.py`.
- All tests must pass cleanly before submitting a PR.
