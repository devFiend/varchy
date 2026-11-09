"""Quality assurance and testing documentation schemas."""

from pydantic import BaseModel, Field

from varchy.core.models.common import Priority, TestType


class TestCase(BaseModel):
    id: str = Field(..., description="Stable identifier e.g. TEST-001")
    title: str
    type: TestType = Field(default=TestType.UNIT)
    priority: Priority = Field(default=Priority.HIGH)
    target_id: str = Field(..., description="Target REQ-### or API-### verified by this test")
    preconditions: list[str] = Field(default_factory=list)
    steps: list[str] = Field(default_factory=list)
    expected_result: str
    is_edge_case: bool = False


class TestingSpec(BaseModel):
    overall_strategy: str
    unit_testing_strategy: str
    integration_testing_strategy: str
    e2e_testing_strategy: str
    security_testing_strategy: str
    test_cases: list[TestCase] = Field(default_factory=list)

