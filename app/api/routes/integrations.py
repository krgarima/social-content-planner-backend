import httpx
from fastapi import APIRouter, HTTPException, Query, status

from app.core.config import get_settings
from app.schemas.post_idea import HashtagSuggestions

router = APIRouter(prefix="/integrations", tags=["integrations"])
settings = get_settings()


@router.get("/hashtags", response_model=HashtagSuggestions)
def get_hashtag_suggestions(q: str = Query(min_length=2, max_length=40)) -> HashtagSuggestions:
    url = "https://api.datamuse.com/words"
    params = {"ml": q, "max": 10}

    try:
        with httpx.Client(timeout=settings.request_timeout_seconds) as client:
            response = client.get(url, params=params)
            response.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to fetch hashtag suggestions",
        ) from exc

    items = response.json()
    suggestions = [f"#{item['word'].replace(' ', '')}" for item in items if item.get("word")]

    return HashtagSuggestions(query=q, suggestions=suggestions)
