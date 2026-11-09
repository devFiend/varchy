"""UI/UX and Design system schemas."""

from pydantic import BaseModel, Field


class InteractionState(BaseModel):
    state_name: str = Field(..., description="e.g. Loading, Empty, Error, Success")
    behavior: str


class ScreenSpec(BaseModel):
    id: str = Field(..., description="Stable identifier e.g. SCREEN-001")
    title: str
    purpose: str
    route_or_view: str
    required_components: list[str] = Field(default_factory=list)
    actions: list[str] = Field(default_factory=list)
    interaction_states: list[InteractionState] = Field(default_factory=list)
    requirement_ids: list[str] = Field(default_factory=list)


class DesignSystem(BaseModel):
    color_palette: dict[str, str] = Field(default_factory=dict)
    typography: dict[str, str] = Field(default_factory=dict)
    spacing_scale: list[str] = Field(default_factory=list)
    component_conventions: list[str] = Field(default_factory=list)


class DesignSpec(BaseModel):
    information_architecture: str
    design_system: DesignSystem = Field(default_factory=DesignSystem)
    screens: list[ScreenSpec] = Field(default_factory=list)

