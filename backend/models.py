from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import uuid4

from pydantic import field_validator
from sqlalchemy import Column, JSON
from sqlmodel import SQLModel, Field


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _uuid() -> str:
    return str(uuid4())


class CategoryEnum(str, Enum):
    prompt_injection = "prompt_injection"
    jailbreak = "jailbreak"
    bias = "bias"
    safety_bypass = "safety_bypass"
    multilingual = "multilingual"
    tool_use = "tool_use"
    multi_turn = "multi_turn"
    rag_poisoning = "rag_poisoning"
    output_manipulation = "output_manipulation"
    system_prompt_reconstruction = "system_prompt_reconstruction"
    hallucination = "hallucination"
    training_data_extraction = "training_data_extraction"


class SeverityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class LanguageEnum(str, Enum):
    en = "en"
    zh = "zh"
    ja = "ja"
    mixed = "mixed"


class AttackTemplate(SQLModel, table=True):
    __tablename__ = "attack_templates"

    id: str = Field(default_factory=_uuid, primary_key=True)
    name: str = Field(index=True)
    category: str = Field(index=True)
    severity: str = Field(default="medium")
    description: str = Field(default="")
    prompt_template: str
    variables: list[str] = Field(default_factory=list, sa_column=Column(JSON, default=[]))
    expected_behavior: str = Field(default="")
    tags: list[str] = Field(default_factory=list, sa_column=Column(JSON, default=[]))
    language: str = Field(default="en")
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)


class TestRun(SQLModel, table=True):
    __tablename__ = "test_runs"

    id: str = Field(default_factory=_uuid, primary_key=True)
    template_id: str = Field(index=True)
    template_name: str = Field(default="")
    model: str = Field(default="claude-sonnet-4-20250514")
    prompt_sent: str
    response: str = Field(default="")
    success: Optional[bool] = Field(default=None)
    notes: str = Field(default="")
    duration_ms: int = Field(default=0)
    category: str = Field(default="")
    severity: str = Field(default="")
    created_at: datetime = Field(default_factory=_utcnow)


# -- Pydantic schemas (request/response) --

class TemplateCreate(SQLModel):
    name: str
    category: CategoryEnum
    severity: SeverityEnum = SeverityEnum.medium
    description: str = ""
    prompt_template: str
    variables: list[str] = []
    expected_behavior: str = ""
    tags: list[str] = []
    language: LanguageEnum = LanguageEnum.en


class TemplateUpdate(SQLModel):
    name: Optional[str] = None
    category: Optional[CategoryEnum] = None
    severity: Optional[SeverityEnum] = None
    description: Optional[str] = None
    prompt_template: Optional[str] = None
    variables: Optional[list[str]] = None
    expected_behavior: Optional[str] = None
    tags: Optional[list[str]] = None
    language: Optional[LanguageEnum] = None


class TestRunCreate(SQLModel):
    template_id: str
    model: str = "claude-sonnet-4-20250514"
    variables: dict[str, str] = {}
    max_tokens: int = 1024
    temperature: float = 1.0
    base_url: str | None = None

    @field_validator("max_tokens")
    @classmethod
    def validate_max_tokens(cls, v: int) -> int:
        if not 1 <= v <= 8192:
            raise ValueError("max_tokens must be between 1 and 8192")
        return v

    @field_validator("temperature")
    @classmethod
    def validate_temperature(cls, v: float) -> float:
        if not 0 <= v <= 2:
            raise ValueError("temperature must be between 0 and 2")
        return v


class TestRunUpdateVerdict(SQLModel):
    success: Optional[bool] = None
    notes: str = ""
