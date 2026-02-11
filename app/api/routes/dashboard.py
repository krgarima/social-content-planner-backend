from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.post_idea import PostIdea
from app.schemas.post_idea import DashboardSummary

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(db: Session = Depends(get_db)) -> DashboardSummary:
    total_posts = db.scalar(select(func.count(PostIdea.id))) or 0

    status_rows = db.execute(
        select(PostIdea.status, func.count(PostIdea.id)).group_by(PostIdea.status)
    ).all()

    platform_rows = db.execute(
        select(PostIdea.platform, func.count(PostIdea.id)).group_by(PostIdea.platform)
    ).all()

    day_rows = db.execute(
        select(func.date(PostIdea.created_at), func.count(PostIdea.id))
        .group_by(func.date(PostIdea.created_at))
        .order_by(func.date(PostIdea.created_at))
    ).all()

    return DashboardSummary(
        total_posts=total_posts,
        by_status={str(key): count for key, count in status_rows},
        by_platform={str(key): count for key, count in platform_rows},
        by_day={str(key): count for key, count in day_rows},
    )
