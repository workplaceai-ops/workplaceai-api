
import tempfile
import uuid

from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from starlette.concurrency import run_in_threadpool

from app.modules.documents.schemas import DocumentParseResponse
from app.modules.documents.service import parse_document


router = APIRouter()

# Initial supported formats
ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".xlsx",
    ".pptx",
    ".html",
    ".htm",
    ".md",
    ".txt",
    ".png",
    ".jpg",
    ".jpeg",
    ".tiff",
    ".tif",
}

MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB


@router.post("/upload", response_model=DocumentParseResponse)
async def upload_document(file: UploadFile = File(...)):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )

    filename = Path(file.filename).name
    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file format: {extension}",
        )

    document_id = str(uuid.uuid4())

    temp_path = None

    try:
        # Save upload temporarily
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension,
        ) as temp_file:

            temp_path = Path(temp_file.name)
            total_size = 0

            while True:
                chunk = await file.read(1024 * 1024)

                if not chunk:
                    break

                total_size += len(chunk)

                if total_size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=413,
                        detail="File exceeds the 25 MB limit.",
                    )

                temp_file.write(chunk)

        if total_size == 0:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty.",
            )

        # Docling conversion is synchronous, so run it
        # outside the async event loop.
        parsed_data = await run_in_threadpool(
            parse_document,
            temp_path,
        )

        return DocumentParseResponse(
            document_id=document_id,
            filename=filename,
            status="processed",
            content=parsed_data["content"],
            structured_data=parsed_data["structured_data"],
        )

    except HTTPException:
        raise

    except Exception:
        # Avoid exposing internal parser errors to clients.
        raise HTTPException(
            status_code=422,
            detail="Unable to process this document. Check its format and contents.",
        )

    finally:
        if temp_path and temp_path.exists():
            temp_path.unlink(missing_ok=True)

        await file.close()


