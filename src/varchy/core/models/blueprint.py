"""Master Blueprint schema combining all structured domains."""

from pydantic import BaseModel, Field

from varchy.core.models.project import Assumption, ProjectBrief, ProjectMetadata
from varchy.core.models.requirement import ProductSpec
from varchy.core.models.design import DesignSpec
from varchy.core.models.architecture import ArchitectureSpec
from varchy.core.models.data_api import DataApiSpec
from varchy.core.models.planning import PlanningSpec
from varchy.core.models.testing import TestingSpec


class Blueprint(BaseModel):
    metadata: ProjectMetadata
    brief: ProjectBrief
    assumptions: list[Assumption] = Field(default_factory=list)
    product: ProductSpec
    design: DesignSpec
    architecture: ArchitectureSpec
    data_api: DataApiSpec
    planning: PlanningSpec
    testing: TestingSpec

