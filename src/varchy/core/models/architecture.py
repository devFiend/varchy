"""Technical architecture schemas."""

from pydantic import BaseModel, Field


class TechStackItem(BaseModel):
    category: str = Field(..., description="e.g. Frontend, Backend, Database, Cache")
    name: str = Field(..., description="Technology name e.g. FastAPI, PostgreSQL")
    justification: str = Field(..., description="Reasoning and trade-offs considered")


class ServiceBoundary(BaseModel):
    name: str
    description: str
    responsibilities: list[str] = Field(default_factory=list)


class SecuritySpec(BaseModel):
    authentication: str
    authorization: str
    secret_management: str
    input_validation: str
    data_protection: str
    rate_limiting: str


class ArchitectureSpec(BaseModel):
    tech_stack: list[TechStackItem] = Field(default_factory=list)
    service_boundaries: list[ServiceBoundary] = Field(default_factory=list)
    frontend_architecture: str
    backend_architecture: str
    security: SecuritySpec
    deployment_topology: str
    scalability_notes: str

