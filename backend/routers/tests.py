import logging

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlmodel import Session, select

from auth import require_api_key, validate_base_url
from config import get_settings
from database import get_session
from models import AttackTemplate, TestRun, TestRunCreate, TestRunUpdateVerdict
from services.runner import substitute_variables, execute_prompt

logger = logging.getLogger(__name__)
settings = get_settings()

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/api/tests", tags=["tests"])


@router.get("")
def list_results(
    category: str | None = None,
    success: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    session: Session = Depends(get_session),
):
    stmt = select(TestRun)
    if category:
        stmt = stmt.where(TestRun.category == category)
    if success == "true":
        stmt = stmt.where(TestRun.success == True)  # noqa: E712
    elif success == "false":
        stmt = stmt.where(TestRun.success == False)  # noqa: E712
    elif success == "null":
        stmt = stmt.where(TestRun.success == None)  # noqa: E711
    stmt = stmt.order_by(TestRun.created_at.desc())
    stmt = stmt.offset((page - 1) * limit).limit(limit)
    return {"success": True, "data": session.exec(stmt).all()}


@router.post("/run")
@limiter.limit(settings.rate_limit_test)
def run_single_test(
    request: Request,
    body: TestRunCreate,
    session: Session = Depends(get_session),
    _: str = Depends(require_api_key),
):
    template = session.get(AttackTemplate, body.template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    # SSRF 防護
    validated_url = validate_base_url(body.base_url)

    prompt = substitute_variables(template.prompt_template, body.variables)

    try:
        response_text, duration_ms = execute_prompt(
            prompt=prompt,
            model=body.model,
            max_tokens=body.max_tokens,
            temperature=body.temperature,
            base_url=validated_url,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        logger.exception("API call failed for model=%s", body.model)
        raise HTTPException(status_code=502, detail="LLM API request failed")

    run = TestRun(
        template_id=template.id,
        template_name=template.name,
        model=body.model,
        prompt_sent=prompt,
        response=response_text,
        duration_ms=duration_ms,
        category=template.category,
        severity=template.severity,
    )
    session.add(run)
    session.commit()
    session.refresh(run)

    logger.info("Test executed: template=%s model=%s duration=%dms", template.name, body.model, duration_ms)
    return {"success": True, "data": run}


@router.put("/{run_id}/verdict")
def update_verdict(
    run_id: str,
    body: TestRunUpdateVerdict,
    session: Session = Depends(get_session),
    _: str = Depends(require_api_key),
):
    run = session.get(TestRun, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Test run not found")
    run.success = body.success
    if body.notes:
        run.notes = body.notes
    session.add(run)
    session.commit()
    session.refresh(run)
    return {"success": True, "data": run}
