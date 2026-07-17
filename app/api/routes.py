from fastapi import APIRouter, HTTPException
from app.schemas.extraction import (
    ExtractionRequest,
    ExtractionResponse,
)
from app.pipeline.preprocessor import preprocess_text
from app.pipeline.extractor import AIExtractor
from app.pipeline.validator import validate_entities

router = APIRouter()
extractor = AIExtractor()

@router.get("/health")
async def health_check() -> dict:
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "ok"}

@router.post("/extract", response_model=ExtractionResponse)
async def extract_entities(request: ExtractionRequest) -> ExtractionResponse:
    """
    Receive raw text and return structured extracted entities.
    """
    try:
        clean_text = preprocess_text(request.text)

        raw_entities = extractor.extract(text=clean_text, document_type=request.document_type)

        validated_entities, confidence = validate_entities(raw_entities)

        return ExtractionResponse(
            document_type=request.document_type,
            entities=validated_entities,
            confidence=confidence,
            original_text=clean_text,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Extraction failed: {str(e)}"
        )