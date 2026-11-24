import httpx

from app.core.config import settings


async def chat_with_ollama(messages: list[dict[str, str]]) -> str:
    payload = {
        "model": settings.ollama_model,
        "messages": messages,
        "stream": False,
    }
    async with httpx.AsyncClient(timeout=httpx.Timeout(180.0)) as client:
        response = await client.post(
            f"{settings.ollama_base_url}/api/chat",
            json=payload,
        )
        response.raise_for_status()
        data = response.json()

    content = data.get("message", {}).get("content")
    if not isinstance(content, str) or not content.strip():
        raise ValueError("Ollama returned an empty response.")
    return content.strip()


async def ollama_health() -> bool:
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            response = await client.get(f"{settings.ollama_base_url}/api/tags")
            response.raise_for_status()
            return True
    except (httpx.HTTPError, ValueError):
        return False
