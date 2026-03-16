from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func

from auth import require_api_key
from database import get_session
from models import AttackTemplate, TemplateCreate, TemplateUpdate

router = APIRouter(prefix="/api/templates", tags=["templates"])


@router.get("")
def list_templates(
    category: str | None = None,
    severity: str | None = None,
    language: str | None = None,
    q: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    session: Session = Depends(get_session),
):
    stmt = select(AttackTemplate)
    count_stmt = select(func.count(AttackTemplate.id))

    if category:
        stmt = stmt.where(AttackTemplate.category == category)
        count_stmt = count_stmt.where(AttackTemplate.category == category)
    if severity:
        stmt = stmt.where(AttackTemplate.severity == severity)
        count_stmt = count_stmt.where(AttackTemplate.severity == severity)
    if language:
        stmt = stmt.where(AttackTemplate.language == language)
        count_stmt = count_stmt.where(AttackTemplate.language == language)
    if q:
        stmt = stmt.where(AttackTemplate.name.contains(q))
        count_stmt = count_stmt.where(AttackTemplate.name.contains(q))

    total = session.exec(count_stmt).one()
    stmt = stmt.order_by(AttackTemplate.created_at.desc())
    stmt = stmt.offset((page - 1) * limit).limit(limit)
    templates = session.exec(stmt).all()
    return {"success": True, "data": templates, "total": total}


@router.get("/{template_id}")
def get_template(template_id: str, session: Session = Depends(get_session)):
    template = session.get(AttackTemplate, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return {"success": True, "data": template}


@router.post("", status_code=201)
def create_template(
    body: TemplateCreate,
    session: Session = Depends(get_session),
    _: str = Depends(require_api_key),
):
    template = AttackTemplate(**body.model_dump())
    session.add(template)
    session.commit()
    session.refresh(template)
    return {"success": True, "data": template}


@router.put("/{template_id}")
def update_template(
    template_id: str,
    body: TemplateUpdate,
    session: Session = Depends(get_session),
    _: str = Depends(require_api_key),
):
    template = session.get(AttackTemplate, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    update_data = body.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(template, key, value)
    template.updated_at = datetime.now(timezone.utc)

    session.add(template)
    session.commit()
    session.refresh(template)
    return {"success": True, "data": template}


@router.delete("/{template_id}")
def delete_template(
    template_id: str,
    session: Session = Depends(get_session),
    _: str = Depends(require_api_key),
):
    template = session.get(AttackTemplate, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    session.delete(template)
    session.commit()
    return {"success": True}
