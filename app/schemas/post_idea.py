from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Platform(str, Enum):
    instagram = "instagram"
    linkedin = "linkedin"
    x = "x"
    tiktok = "tiktok"
    facebook = "facebook"


class PostStatus(str, Enum):
    idea = "idea"
    draft = "draft"
    scheduled = "scheduled"
    published = "published"


class PostIdeaBase(BaseModel):
    platform: Platform
    title: str = Field(min_length=3, max_length=200)
    caption: str = Field(min_length=3)
    status: PostStatus
    scheduled_at: datetime | None = None
    hashtags: str = Field(default="", max_length=1000)

    @field_validator("title", "caption", "hashtags", mode="before")
    @classmethod
    def strip_text(cls, value: str | None) -> str | None:
        if isinstance(value, str):
            return value.strip()
        return value


class PostIdeaCreate(PostIdeaBase):
    pass


class PostIdeaUpdate(BaseModel):
    platform: Platform | None = None
    title: str | None = Field(default=None, min_length=3, max_length=200)
    caption: str | None = Field(default=None, min_length=3)
    status: PostStatus | None = None
    scheduled_at: datetime | None = None
    hashtags: str | None = Field(default=None, max_length=1000)

    @field_validator("title", "caption", "hashtags", mode="before")
    @classmethod
    def strip_optional_text(cls, value: str | None) -> str | None:
        if isinstance(value, str):
            return value.strip()
        return value


class PostIdeaRead(PostIdeaBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DashboardSummary(BaseModel):
    total_posts: int
    by_status: dict[str, int]
    by_platform: dict[str, int]
    by_day: dict[str, int]


class HashtagSuggestions(BaseModel):
    query: str
    suggestions: list[str]
