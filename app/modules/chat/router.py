from fastapi import APIRouter, HTTPException
import httpx

from app.modules.chat.schemas import ChatRequest, ChatResponse
from app.modules.chat.service import generate_reply
from app.core.config import settings

router = APIRouter()


@router.post("", response_model=ChatResponse)
async def chat(payload: ChatRequest):
    try:
        answer = await generate_reply(payload.messages)
        return ChatResponse(response=answer, model=settings.ollama_model)
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="Cannot connect to Ollama. Make sure Ollama is running (ollama serve).",
        )
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=502, detail=f"Ollama returned an error: {exc.response.text}")
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Ollama took too long to respond.")
