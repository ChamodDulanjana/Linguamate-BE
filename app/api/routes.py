from fastapi import APIRouter
from app.api.endpoints import grammar, activity

api_router = APIRouter()
api_router.include_router(grammar.router, tags=["grammar"])
api_router.include_router(activity.router, tags=["activity"])
