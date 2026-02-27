from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from sqlalchemy import Column, JSON
from sqlmodel import SQLModel, Field


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _uuid() -> str:
    return str(uuid4())


class AttackTemplate(SQLModel, table=True):
    __tablename__ = "attack_templates"

    id: str = Field(default_factory=_uuid, primary_key=True)
    name: str = Field(index=True)
    category: str = Field(index=True)  # prompt_injection / jailbreak / bias / safety_bypass / multilingual
    severity: str = Field(default="medium")  # low / medium / high / critical
    description: str = Field(default="")
    prompt_template: str  # 支援 {{variable}} 語法
    variables: list[str] = Field(default_factory=list, sa_column=Column(JSON, default=[]))
    expected_behavior: str = Field(default="")
    tags: list[str] = Field(default_factory=list, sa_column=Column(JSON, default=[]))
    language: str = Field(default="en")  # en / zh / mixed
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)


class TestRun(SQLModel, table=True):
    __tablename__ = "test_runs"

    id: str = Field(default_factory=_uuid, primary_key=True)
    template_id: str = Field(index=True)
    template_name: str = Field(default="")
    model: str = Field(default="claude-sonnet-4-20250514")
    prompt_sent: str  # 變數已替換的完整 prompt
    response: str = Field(default="")
    success: Optional[bool] = Field(default=None)  # None=pending, True=pass, False=fail
    notes: str = Field(default="")
    duration_ms: int = Field(default=0)
    category: str = Field(default="")
    severity: str = Field(default="")
    created_at: datetime = Field(default_factory=_utcnow)


# -- Pydantic schemas (request/response) --

class TemplateCreate(SQLModel):
    name: str
    category: str
    severity: str = "medium"
    description: str = ""
    prompt_template: str
    variables: list[str] = []
    expected_behavior: str = ""
    tags: list[str] = []
    language: str = "en"


class TemplateUpdate(SQLModel):
    name: Optional[str] = None
    category: Optional[str] = None
    severity: Optional[str] = None
    description: Optional[str] = None
    prompt_template: Optional[str] = None
    variables: Optional[list[str]] = None
    expected_behavior: Optional[str] = None
    tags: Optional[list[str]] = None
    language: Optional[str] = None


class TestRunCreate(SQLModel):
    template_id: str
    model: str = "claude-sonnet-4-20250514"
    variables: dict[str, str] = {}
    max_tokens: int = 1024
    temperature: float = 1.0
    base_url: str | None = None


class TestRunUpdateVerdict(SQLModel):
    success: Optional[bool] = None
    notes: str = ""
