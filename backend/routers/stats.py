from fastapi import APIRouter, Depends
from sqlmodel import Session, text

from database import get_session
from models import TestRun, AttackTemplate

router = APIRouter(prefix="/api/stats", tags=["stats"])

# 表名從 model metadata 取得
_test_table = TestRun.__tablename__
_tmpl_table = AttackTemplate.__tablename__

_STATS_SQL = text(f"""
SELECT
  COUNT(*) AS total,
  COUNT(*) FILTER (WHERE success = true) AS total_pass,
  COUNT(*) FILTER (WHERE success = false) AS total_fail,
  COUNT(*) FILTER (WHERE success IS NULL) AS total_pending,
  (SELECT COUNT(*) FROM {_tmpl_table}) AS total_templates
FROM {_test_table}
""")

_CAT_SQL = text(f"""
SELECT category, COUNT(*) AS cnt
FROM {_test_table}
WHERE category IS NOT NULL
GROUP BY category
""")

_SEV_SQL = text(f"""
SELECT severity, COUNT(*) AS cnt
FROM {_test_table}
WHERE severity IS NOT NULL
GROUP BY severity
""")


@router.get("")
def get_stats(session: Session = Depends(get_session)):
    row = session.exec(_STATS_SQL).one()
    total, total_pass, total_fail, total_pending, total_templates = row

    cat_rows = session.exec(_CAT_SQL).all()
    category_distribution = {r[0]: r[1] for r in cat_rows}

    sev_rows = session.exec(_SEV_SQL).all()
    severity_distribution = {r[0]: r[1] for r in sev_rows}

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
