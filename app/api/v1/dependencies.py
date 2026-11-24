from app.ai.providers.ollama import ollama_health
from app.core.config import settings


async def health_check():
    available = await ollama_health()
    return {
        "status": "ok",
        "ollama": "available" if available else "unavailable",
        "model": settings.ollama_model,
    }
