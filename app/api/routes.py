from fastapi import APIRouter
from app.api.auth import auth_router
from app.api.moderate import moderation_router
from app.api.usage import usage_router

api_router = APIRouter()

@api_router.get("/health")
def health_check():
    return {"status": "ok"}

api_router.include_router(auth_router)
api_router.include_router(moderation_router)
api_router.include_router(usage_router)
