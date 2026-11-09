"""Common enumerations and base types for Varchy domain models."""

from enum import Enum


class ProjectCategory(str, Enum):
    WEB_APP = "web_app"
    MOBILE_APP = "mobile_app"
    DESKTOP_APP = "desktop_app"
    SAAS = "saas"
    API_BACKEND = "api_backend"
    AI_APP = "ai_app"
    DEV_TOOL = "dev_tool"
    CLI = "cli"
    LIBRARY = "library"
    ECOMMERCE = "ecommerce"
    GAME = "game"
    INFRASTRUCTURE = "infrastructure"
    ENTERPRISE = "enterprise"


class GenerationMode(str, Enum):
    INTERACTIVE = "interactive"
    AUTONOMOUS = "autonomous"


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RequirementType(str, Enum):
    FUNCTIONAL = "functional"
    NON_FUNCTIONAL = "non_functional"
    CONSTRAINT = "constraint"


class TestType(str, Enum):
    UNIT = "unit"
    INTEGRATION = "integration"
    E2E = "e2e"
    SECURITY = "security"
    PERFORMANCE = "performance"


class Severity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class StageID(str, Enum):
    DISCOVERY = "discovery"
    CLARIFICATION = "clarification"
    PRODUCT = "product"
    UX = "ux"
    ARCHITECTURE = "architecture"
    DATA_API = "data_api"
    PLANNING = "planning"
    QA = "qa"
    VALIDATION = "validation"
    COMPILATION = "compilation"

