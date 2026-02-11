from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.post_idea import PostIdea
from app.schemas.post_idea import PostIdeaCreate, PostIdeaRead, PostIdeaUpdate

router = APIRouter(prefix="/post-ideas", tags=["post-ideas"])


@router.post("", response_model=PostIdeaRead, status_code=status.HTTP_201_CREATED)
def create_post_idea(payload: PostIdeaCreate, db: Session = Depends(get_db)) -> PostIdea:
    post_idea = PostIdea(**payload.model_dump())
    db.add(post_idea)
    db.commit()
    db.refresh(post_idea)
    return post_idea


@router.get("", response_model=list[PostIdeaRead])
def list_post_ideas(
    status_filter: str | None = Query(default=None, alias="status"),
    platform: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[PostIdea]:
    stmt = select(PostIdea).order_by(PostIdea.created_at.desc())
    if status_filter:
        stmt = stmt.where(PostIdea.status == status_filter)
    if platform:
        stmt = stmt.where(PostIdea.platform == platform)

    return list(db.scalars(stmt).all())


@router.get("/{post_idea_id}", response_model=PostIdeaRead)
def get_post_idea(post_idea_id: int, db: Session = Depends(get_db)) -> PostIdea:
    post_idea = db.get(PostIdea, post_idea_id)
    if not post_idea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post idea not found")
    return post_idea


@router.put("/{post_idea_id}", response_model=PostIdeaRead)
def replace_post_idea(post_idea_id: int, payload: PostIdeaCreate, db: Session = Depends(get_db)) -> PostIdea:
    post_idea = db.get(PostIdea, post_idea_id)
    if not post_idea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post idea not found")

    for key, value in payload.model_dump().items():
        setattr(post_idea, key, value)

    db.add(post_idea)
    db.commit()
    db.refresh(post_idea)
    return post_idea


@router.patch("/{post_idea_id}", response_model=PostIdeaRead)
def update_post_idea(post_idea_id: int, payload: PostIdeaUpdate, db: Session = Depends(get_db)) -> PostIdea:
    post_idea = db.get(PostIdea, post_idea_id)
    if not post_idea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post idea not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(post_idea, key, value)

    db.add(post_idea)
    db.commit()
    db.refresh(post_idea)
    return post_idea


@router.delete("/{post_idea_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_idea(post_idea_id: int, db: Session = Depends(get_db)) -> None:
    post_idea = db.get(PostIdea, post_idea_id)
    if not post_idea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post idea not found")

    db.delete(post_idea)
    db.commit()
