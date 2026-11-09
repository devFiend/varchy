"""Database and API contract schemas."""

from pydantic import BaseModel, Field


class DatabaseAttribute(BaseModel):
    name: str
    data_type: str
    is_primary_key: bool = False
    is_nullable: bool = False
    is_unique: bool = False
    foreign_key_target: str | None = None


class DatabaseEntity(BaseModel):
    id: str = Field(..., description="e.g. ENT-001")
    name: str = Field(..., description="Table or collection name")
    description: str
    attributes: list[DatabaseAttribute] = Field(default_factory=list)
    indexes: list[str] = Field(default_factory=list)


class ApiEndpoint(BaseModel):
    id: str = Field(..., description="e.g. API-001")
    path: str
    method: str = Field(..., description="GET, POST, PUT, DELETE, etc.")
    summary: str
    auth_required: bool = True
    request_body_schema: dict | None = None
    response_body_schema: dict = Field(default_factory=dict)
    status_codes: list[int] = Field(default_factory=lambda: [200, 400, 401, 500])
    requirement_ids: list[str] = Field(default_factory=list)


class DataApiSpec(BaseModel):
    entities: list[DatabaseEntity] = Field(default_factory=list)
    endpoints: list[ApiEndpoint] = Field(default_factory=list)
    mermaid_er_diagram: str = ""

