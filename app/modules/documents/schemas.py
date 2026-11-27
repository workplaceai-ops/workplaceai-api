
from typing import Any

from pydantic import BaseModel


class DocumentParseResponse(BaseModel):
    document_id: str
    filename: str
    status: str
    content: str
    structured_data: dict[str, Any]


# This defines the response format returned by your upload endpoint.