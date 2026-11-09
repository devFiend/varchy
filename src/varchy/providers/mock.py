"""Mock AI provider for testing and deterministic blueprint generation."""

from typing import TypeVar
from pydantic import BaseModel

from varchy.core.models.architecture import ArchitectureSpec, SecuritySpec, TechStackItem
from varchy.core.models.blueprint import Blueprint
from varchy.core.models.common import Priority, ProjectCategory, RequirementType, TestType
from varchy.core.models.data_api import ApiEndpoint, DataApiSpec, DatabaseAttribute, DatabaseEntity
from varchy.core.models.design import DesignSpec, InteractionState, ScreenSpec
from varchy.core.models.planning import Phase, PlanningSpec, Task
from varchy.core.models.project import Assumption, ProjectBrief, ProjectMetadata
from varchy.core.models.requirement import ProductSpec, Requirement
from varchy.core.models.testing import TestCase, TestingSpec
from varchy.providers.base import BaseAIProvider

TModel = TypeVar("TModel", bound=BaseModel)


class MockAIProvider(BaseAIProvider):
    """Provides complete, mathematically sound blueprints for testing."""

    async def complete_structured(
        self,
        prompt: str,
        response_model: type[TModel],
        system_prompt: str | None = None,
        temperature: float = 0.2,
    ) -> TModel:
        if response_model is Blueprint:
            return self.generate_mock_blueprint()  # type: ignore
        raise NotImplementedError(f"Mock does not support {response_model.__name__} directly.")

    @classmethod
    def generate_mock_blueprint(
        cls,
        name: str = "TestApp",
        idea: str = "A secure note-taking developer tool",
    ) -> Blueprint:
        metadata = ProjectMetadata(
            name=name,
            slug="testapp",
            description=idea,
            category=ProjectCategory.DEV_TOOL,
        )
        brief = ProjectBrief(
            raw_idea=idea,
            target_audience=["Developers", "Engineers"],
            core_problem="Notes are disorganized and not connected to code.",
            proposed_solution="A local-first encrypted markdown notebook with bidirectional links.",
            key_features=["End-to-end encryption", "Markdown editing", "Local SQLite sync"],
        )
        assumptions = [
            Assumption(
                id="ASM-001",
                statement="Users have local storage access for SQLite files.",
                category="Storage",
                confirmed=True,
            )
        ]
        requirements = [
            Requirement(
                id="REQ-001",
                title="Local-First Note Storage",
                description="Application persists all notes locally in an encrypted SQLite database.",
                type=RequirementType.FUNCTIONAL,
                priority=Priority.CRITICAL,
                acceptance_criteria=[
                    "Notes can be created offline.",
                    "Notes are stored using AES-256-GCM encryption.",
                ],
                user_story="As a developer, I want my notes stored locally so they remain private.",
            ),
            Requirement(
                id="REQ-002",
                title="Full-Text Search",
                description="Users can search notes with sub-50ms latency.",
                type=RequirementType.FUNCTIONAL,
                priority=Priority.HIGH,
                acceptance_criteria=[
                    "Search index updates on save.",
                    "FTS5 query returns matched excerpts.",
                ],
            ),
        ]
        product = ProductSpec(
            overview="Local-first secure note taking developer tool.",
            problem_statement="Engineers need private, fast documentation.",
            vision="The standard offline knowledge base for programmers.",
            requirements=requirements,
        )
        design = DesignSpec(
            information_architecture="Main window with two-pane layout: Sidebar note tree and Editor.",
            screens=[
                ScreenSpec(
                    id="SCREEN-001",
                    title="Editor Workspace",
                    purpose="Main writing and editing interface",
                    route_or_view="/workspace",
                    required_components=["NoteTree", "MarkdownEditor", "PreviewPane"],
                    actions=["Create Note", "Save Note", "Search"],
                    interaction_states=[
                        InteractionState(
                            state_name="Loading",
                            behavior="Render skeleton view of tree and editor",
                        ),
                        InteractionState(
                            state_name="Empty",
                            behavior="Show prompt to create first note",
                        ),
                    ],
                    requirement_ids=["REQ-001"],
                )
            ],
        )
        architecture = ArchitectureSpec(
            tech_stack=[
                TechStackItem(
                    category="Language",
                    name="Python 3.12",
                    justification="Native async performance and typing",
                ),
                TechStackItem(
                    category="Database",
                    name="SQLite (FTS5 + SQLCipher)",
                    justification="Local-first ACID storage with zero server dependencies",
                ),
            ],
            service_boundaries=[],
            frontend_architecture="Desktop UI shell",
            backend_architecture="Local embedded SQLite engine",
            security=SecuritySpec(
                authentication="Local master passphrase with Argon2id hashing",
                authorization="Single user local role",
                secret_management="Keys kept in process memory and OS Keychain",
                input_validation="Pydantic models on all payload inputs",
                data_protection="AES-256-GCM at rest",
                rate_limiting="Not applicable (local app)",
            ),
            deployment_topology="Standalone binary",
            scalability_notes="Single user local database supporting up to 100k notes.",
        )
        data_api = DataApiSpec(
            entities=[
                DatabaseEntity(
                    id="ENT-001",
                    name="notes",
                    description="Encrypted note records",
                    attributes=[
                        DatabaseAttribute(name="id", data_type="TEXT", is_primary_key=True),
                        DatabaseAttribute(name="title", data_type="TEXT"),
                        DatabaseAttribute(name="encrypted_body", data_type="BLOB"),
                    ],
                )
            ],
            endpoints=[
                ApiEndpoint(
                    id="API-001",
                    path="/api/notes",
                    method="GET",
                    summary="Retrieve notes metadata list",
                    requirement_ids=["REQ-001"],
                )
            ],
        )
        planning = PlanningSpec(
            phases=[
                Phase(
                    id="PHASE-1",
                    name="Foundation",
                    objective="Scaffold database and crypto layer",
                    order=1,
                )
            ],
            tasks=[
                Task(
                    id="TASK-001",
                    phase_id="PHASE-1",
                    title="Initialize SQLite and SQLCipher",
                    description="Configure SQLite connection and schema migrations.",
                    dependencies=[],
                    requirement_ids=["REQ-001"],
                    completion_criteria=["Database initializes without errors.", "Migrations run."],
                ),
                Task(
                    id="TASK-002",
                    phase_id="PHASE-1",
                    title="Implement Note CRUD Operations",
                    description="Implement create, read, update, delete service methods.",
                    dependencies=["TASK-001"],
                    requirement_ids=["REQ-001"],
                    completion_criteria=["All CRUD unit tests pass."],
                ),
            ],
        )
        testing = TestingSpec(
            overall_strategy="Comprehensive pytest suite with 90%+ code coverage.",
            unit_testing_strategy="Unit test encryption, schema, and queries.",
            integration_testing_strategy="Integration test file migrations and indexing.",
            e2e_testing_strategy="UI and CLI end-to-end tests.",
            security_testing_strategy="Cryptographic verification tests.",
            test_cases=[
                TestCase(
                    id="TEST-001",
                    title="Verify Note Encryption at Rest",
                    type=TestType.UNIT,
                    target_id="REQ-001",
                    expected_result="Plain text string is not present in raw database bytes.",
                )
            ],
        )
        return Blueprint(
            metadata=metadata,
            brief=brief,
            assumptions=assumptions,
            product=product,
            design=design,
            architecture=architecture,
            data_api=data_api,
            planning=planning,
            testing=testing,
        )

