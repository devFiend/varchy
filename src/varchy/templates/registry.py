"""Architectural templates and project archetypes."""

from dataclasses import dataclass
from typing import Optional
from varchy.core.models.architecture import TechStackItem
from varchy.core.models.common import ProjectCategory


@dataclass
class ArchitectureTemplate:
    id: str
    name: str
    description: str
    category: ProjectCategory
    recommended_tech_stack: list[TechStackItem]
    default_security_model: str
    default_persistence_model: str


TEMPLATES_REGISTRY: dict[str, ArchitectureTemplate] = {
    "saas": ArchitectureTemplate(
        id="saas",
        name="Multi-Tenant Web SaaS",
        description="Scalable cloud web platform with multi-tenancy, subscription billing, and RBAC.",
        category=ProjectCategory.SAAS,
        recommended_tech_stack=[
            TechStackItem(category="Frontend", name="Next.js / React (TypeScript)", justification="Server-side rendering, SEO, and fast interactive dashboard views."),
            TechStackItem(category="Backend API", name="FastAPI / Node.js", justification="High async concurrency with strict schema validation."),
            TechStackItem(category="Primary Database", name="PostgreSQL", justification="ACID-compliant relational database with multi-tenant row-level security."),
            TechStackItem(category="Cache & Sessions", name="Redis", justification="In-memory session storage and distributed rate limiting."),
        ],
        default_security_model="JWT / OAuth2 bearer authentication with role-based access control and tenant isolation.",
        default_persistence_model="PostgreSQL with schema migrations and foreign-key integrity constraints.",
    ),
    "local_first": ArchitectureTemplate(
        id="local_first",
        name="Local-First Encrypted App",
        description="Zero-knowledge, offline-first client application with local encrypted database.",
        category=ProjectCategory.DEV_TOOL,
        recommended_tech_stack=[
            TechStackItem(category="Runtime", name="Python / Rust / Electron", justification="Native cross-platform execution with direct filesystem access."),
            TechStackItem(category="Database", name="SQLite + SQLCipher", justification="Embedded zero-dependency ACID storage with AES-256 transparent encryption."),
            TechStackItem(category="Sync Engine", name="CRDTs (Automerge / Yjs)", justification="Conflict-free peer-to-peer or server-assisted synchronization."),
        ],
        default_security_model="Master passphrase derivation using Argon2id and client-side AES-GCM encryption.",
        default_persistence_model="Local encrypted SQLite database with full-text search (FTS5).",
    ),
    "api_backend": ArchitectureTemplate(
        id="api_backend",
        name="High-Throughput API Service",
        description="Scalable headless REST and RPC backend microservice designed for high concurrency.",
        category=ProjectCategory.API_BACKEND,
        recommended_tech_stack=[
            TechStackItem(category="API Gateway", name="FastAPI / Go", justification="Low-latency HTTP/2 and gRPC transport layers."),
            TechStackItem(category="Message Broker", name="RabbitMQ / Kafka", justification="Asynchronous event streaming and worker queue decoupling."),
            TechStackItem(category="Database", name="PostgreSQL + ClickHouse", justification="OLTP transaction processing paired with columnar analytical queries."),
        ],
        default_security_model="mTLS service-to-service authentication, API key rate limiting, and strict input schema validation.",
        default_persistence_model="Connection-pooled PostgreSQL with read replicas.",
    ),
    "dev_tool": ArchitectureTemplate(
        id="dev_tool",
        name="Developer CLI & Orchestrator",
        description="Ergonomic terminal developer tool with rich formatting and local state management.",
        category=ProjectCategory.DEV_TOOL,
        recommended_tech_stack=[
            TechStackItem(category="CLI Framework", name="Typer (Python 3.12+)", justification="Type-hint driven declarative commands and automatic autocompletion."),
            TechStackItem(category="Terminal UI", name="Rich", justification="Beautiful terminal tables, live progress bars, and markdown rendering."),
            TechStackItem(category="Vault", name="OS Keyring", justification="Hardware-backed secure secret storage without plaintext disk leaks."),
        ],
        default_security_model="Hardware-backed OS Keychain storage with environment variable fallbacks; zero external telemetry.",
        default_persistence_model="Local JSON state and SQLite transaction journal in hidden workspace directory.",
    ),
    "mobile_app": ArchitectureTemplate(
        id="mobile_app",
        name="Offline-Ready Mobile App",
        description="Cross-platform iOS and Android application with offline caching and background sync.",
        category=ProjectCategory.MOBILE_APP,
        recommended_tech_stack=[
            TechStackItem(category="Mobile Framework", name="React Native / Flutter", justification="Single codebase targeting iOS and Android with native performance."),
            TechStackItem(category="Local Cache", name="SQLite / WatermelonDB", justification="Fast observable local database for 60fps offline scrolling."),
            TechStackItem(category="Backend Sync", name="REST / GraphQL", justification="Delta sync endpoints reducing mobile data consumption."),
        ],
        default_security_model="OAuth2 PKCE mobile authorization flow and biometric keychain authentication.",
        default_persistence_model="Client-side SQLite database synchronizing with cloud backend.",
    ),
}


def get_template(template_id: str) -> Optional[ArchitectureTemplate]:
    """Retrieve template by id."""
    return TEMPLATES_REGISTRY.get(template_id.lower().strip())

