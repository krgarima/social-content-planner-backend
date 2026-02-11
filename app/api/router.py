from fastapi import APIRouter

from app.api.routes import dashboard, integrations, post_ideas

api_router = APIRouter()
api_router.include_router(post_ideas.router)
api_router.include_router(dashboard.router)
api_router.include_router(integrations.router)
