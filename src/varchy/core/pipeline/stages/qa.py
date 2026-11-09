"""QA & Testing stage: generates TestingSpec and test cases (TEST-###) mapped to requirements."""

from varchy.core.models.common import Priority, StageID, TestType
from varchy.core.models.testing import TestCase, TestingSpec
from varchy.core.pipeline.context import StageContext
from varchy.core.pipeline.stage import BaseStage


class QAStage(BaseStage[TestingSpec]):
    stage_id = StageID.QA
    depends_on = [StageID.PLANNING]

    async def execute(self, ctx: StageContext) -> TestingSpec:
        ctx.log_progress(self.stage_id, "Formulating testing strategies and verification matrix (TEST-###)...")
        product = ctx.get_data("product")
        data_api = ctx.get_data("data_api")
        req_ids = [r.id for r in product.requirements] if product else ["REQ-001"]
        api_ids = [e.id for e in data_api.endpoints] if data_api else ["API-001"]

        try:
            prompt = (
                f"Generate complete TestingSpec for '{ctx.metadata.name}'. "
                f"Define testing strategies (unit, integration, e2e, security) and concrete TestCase "
                f"objects with stable IDs (TEST-001, etc.) mapping to requirement IDs {req_ids} or API IDs {api_ids}."
            )
            spec = await ctx.provider.complete_structured(
                prompt=prompt,
                response_model=TestingSpec,
                system_prompt="You are a Principal Quality Assurance Engineer. Generate rigorous positive, negative, and edge-case test specifications.",
            )
        except Exception:
            spec = TestingSpec(
                overall_strategy="Automated continuous integration pipeline testing every layer from unit to end-to-end integration.",
                unit_testing_strategy="Isolated pytest unit suites for domain entities, cryptographic functions, and validation algorithms.",
                integration_testing_strategy="Ephemeral database containers for testing repository queries, migrations, and API contracts.",
                e2e_testing_strategy="Headless browser and CLI integration tests validating complete user journeys from input to persistence.",
                security_testing_strategy="Automated vulnerability scans, dependency audits, injection fuzzing, and secret leakage prevention.",
                test_cases=[
                    TestCase(
                        id="TEST-001",
                        title="Validate Core Workflow Initialization & State Persistence",
                        type=TestType.INTEGRATION,
                        priority=Priority.CRITICAL,
                        target_id=req_ids[0],
                        preconditions=["Database container is running and migrations are applied"],
                        steps=[
                            "Invoke workflow engine with valid configuration",
                            "Assert state is committed atomically to persistence store",
                            "Query repository to verify state matches Pydantic schema",
                        ],
                        expected_result="Workflow completes within 200ms and returns valid state with zero data corruption.",
                        is_edge_case=False,
                    ),
                    TestCase(
                        id="TEST-002",
                        title="Reject Corrupt or Non-Conforming Schema Payloads",
                        type=TestType.UNIT,
                        priority=Priority.HIGH,
                        target_id=req_ids[0],
                        preconditions=["Workflow engine initialized"],
                        steps=[
                            "Submit malformed payload missing mandatory identifier",
                            "Assert engine raises ValidationError without committing state",
                        ],
                        expected_result="System rejects payload with HTTP 400 / ValidationError; database remains untouched.",
                        is_edge_case=True,
                    ),
                    TestCase(
                        id="TEST-003",
                        title="Verify API Authentication & Rate Limiting Enforcement",
                        type=TestType.SECURITY,
                        priority=Priority.HIGH,
                        target_id=api_ids[0] if api_ids else req_ids[0],
                        preconditions=["API service listening on test port"],
                        steps=[
                            "Send request to protected endpoint without bearer credentials",
                            "Send 100 requests in rapid succession exceeding rate limit threshold",
                        ],
                        expected_result="Unauthorized request returns 401; bursts exceeding quota return 429 Too Many Requests.",
                        is_edge_case=False,
                    ),
                ],
            )

        ctx.set_data("testing", spec)
        return spec
