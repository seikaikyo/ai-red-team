from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func

from database import get_session
from models import TestRun, AttackTemplate

router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("")
def get_stats(session: Session = Depends(get_session)):
    total = session.exec(select(func.count(TestRun.id))).one()
    total_pass = session.exec(
        select(func.count(TestRun.id)).where(TestRun.success == True)  # noqa: E712
    ).one()
    total_fail = session.exec(
        select(func.count(TestRun.id)).where(TestRun.success == False)  # noqa: E712
    ).one()
    total_pending = session.exec(
        select(func.count(TestRun.id)).where(TestRun.success == None)  # noqa: E711
    ).one()

    # 類別分布
    cat_rows = session.exec(
        select(TestRun.category, func.count(TestRun.id))
        .group_by(TestRun.category)
    ).all()
    category_distribution = {row[0]: row[1] for row in cat_rows if row[0]}

    # 嚴重度分布
    sev_rows = session.exec(
        select(TestRun.severity, func.count(TestRun.id))
        .group_by(TestRun.severity)
    ).all()
    severity_distribution = {row[0]: row[1] for row in sev_rows if row[0]}

    total_templates = session.exec(select(func.count(AttackTemplate.id))).one()

    judged = total_pass + total_fail
    success_rate = (total_pass / judged * 100) if judged > 0 else 0.0

    return {
        "success": True,
        "data": {
            "total_tests": total,
            "total_pass": total_pass,
            "total_fail": total_fail,
            "total_pending": total_pending,
            "success_rate": success_rate,
            "category_distribution": category_distribution,
            "severity_distribution": severity_distribution,
            "total_templates": total_templates,
        },
    }
