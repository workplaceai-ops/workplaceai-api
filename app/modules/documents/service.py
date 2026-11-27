
from functools import lru_cache
from pathlib import Path
from typing import Any

from docling.document_converter import DocumentConverter


@lru_cache(maxsize=1)
def get_converter() -> DocumentConverter:
    """
    Reuse one converter instance instead of initializing
    document processing models for every upload.
    """
    return DocumentConverter()


def parse_document(file_path: Path) -> dict[str, Any]:
    """
    Parse a document using Docling.

    Returns:
        Markdown content and structured document JSON.
    """
    converter = get_converter()

    result = converter.convert(str(file_path))

    try:
        document = result.document

        markdown_content = document.export_to_markdown()
        structured_data = document.export_to_dict()

        return {
            "content": markdown_content,
            "structured_data": structured_data,
        }

    finally:
        # Release input resources after exporting.
        result.input.release()

        
# DocumentConverter() initializes Docling.
# convert() reads the uploaded document.
# export_to_markdown() produces readable document content.
# export_to_dict() produces structured JSON containing document information, including its structural elements.