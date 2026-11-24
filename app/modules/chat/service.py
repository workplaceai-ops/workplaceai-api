from app.ai.providers.ollama import chat_with_ollama
from app.core.config import settings
from app.modules.chat.schemas import ChatMessage


async def generate_reply(messages: list[ChatMessage]) -> str:
    ollama_messages = [
        {"role": message.role, "content": message.content}
        for message in messages
    ]
    result = await chat_with_ollama(ollama_messages)
    return result
