"""Tests for Varchy core Pydantic domain models."""

import json
from varchy.core.models.common import Priority, ProjectCategory, RequirementType
from varchy.core.models.project import ProjectMetadata
from varchy.core.models.requirement import Requirement
from varchy.core.models.blueprint import Blueprint
from varchy.providers.mock import MockAIProvider


def test_project_metadata_serialization():
    meta = ProjectMetadata(
        name="CryptoNotes",
        slug="cryptonotes",
        description="Local-first secure notes",
        category=ProjectCategory.DEV_TOOL,
    )
    dumped = meta.model_dump_json()
    loaded = ProjectMetadata.model_validate_json(dumped)
    assert loaded.name == "CryptoNotes"
    assert loaded.category == ProjectCategory.DEV_TOOL


def test_requirement_model_validation():
    req = Requirement(
        id="REQ-001",
        title="Zero-Knowledge Encryption",
        description="Notes must be encrypted with user private key.",
        type=RequirementType.NON_FUNCTIONAL,
        priority=Priority.CRITICAL,
        acceptance_criteria=["Key derived via Argon2id", "AES-256-GCM cipher"],
    )
    assert req.id == "REQ-001"
    assert len(req.acceptance_criteria) == 2


def test_mock_blueprint_schema_conformance():
    bp = MockAIProvider.generate_mock_blueprint()
    assert isinstance(bp, Blueprint)
    assert len(bp.product.requirements) > 0
    assert len(bp.planning.tasks) > 0
    assert len(bp.testing.test_cases) > 0

