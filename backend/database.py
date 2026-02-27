import json
from pathlib import Path

from sqlmodel import SQLModel, create_engine, Session
from config import get_settings

settings = get_settings()


def _is_sqlite(url: str) -> bool:
    return url.startswith("sqlite")


def _build_sync_url(url: str) -> str:
    if _is_sqlite(url):
        return url
    return url.replace("postgresql://", "postgresql+psycopg://")


def _build_engine(url: str):
    sync_url = _build_sync_url(url)
    kwargs = {"echo": settings.debug}
    if _is_sqlite(url):
        kwargs["connect_args"] = {"check_same_thread": False}
    return create_engine(sync_url, **kwargs)


engine = _build_engine(settings.database_url)


def init_db():
    """建立資料表 + 載入 seed data"""
    from models import AttackTemplate  # noqa: F401

    SQLModel.metadata.create_all(engine)
    _load_seed_data()


def _load_seed_data():
    """如果 templates 表為空，從 JSON 載入 seed data"""
    from models import AttackTemplate

    with Session(engine) as session:
        count = session.query(AttackTemplate).count()
        if count > 0:
            return

        seed_path = Path(__file__).parent / "seed" / "templates.json"
        if not seed_path.exists():
            return

        templates = json.loads(seed_path.read_text(encoding="utf-8"))
        for t in templates:
            session.add(AttackTemplate(**t))
        session.commit()
        print(f"[Seed] 載入 {len(templates)} 個攻擊模板")


def get_session():
    with Session(engine) as session:
        yield session
