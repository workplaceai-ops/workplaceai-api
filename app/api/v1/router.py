from fastapi import APIRouter
from app.modules.chat.router import router as chat_router
from app.api.v1.dependencies import health_check

api_router = APIRouter()
api_router.add_api_route("/health", health_check, methods=["GET"], tags=["health"])
api_router.include_router(chat_router, prefix="/chat", tags=["chat"])
