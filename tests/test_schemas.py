import pytest
from pydantic import ValidationError
from app.schemas.extraction import (
    ExtractionRequest,
    ExtractionResponse,
    ExtractedEntities,
    DocumentType,
)


def test_extraction_request_valid():
    request = ExtractionRequest(text="Texto válido com mais de dez caracteres.")
    assert request.document_type == DocumentType.UNKNOWN


def test_extraction_request_text_too_short():
    with pytest.raises(ValidationError):
        ExtractionRequest(text="Curto")


def test_extraction_request_with_document_type():
    request = ExtractionRequest(
        text="Texto válido com mais de dez caracteres.",
        document_type=DocumentType.CONTRACT,
    )
    assert request.document_type == DocumentType.CONTRACT


def test_extraction_request_invalid_document_type():
    with pytest.raises(ValidationError):
        ExtractionRequest(
            text="Texto válido com mais de dez caracteres.",
            document_type="tipo_invalido",
        )


def test_extracted_entities_default_empty_lists():
    entities = ExtractedEntities()
    assert entities.people == []
    assert entities.organizations == []


def test_extraction_response_invalid_confidence():
    with pytest.raises(ValidationError):
        ExtractionResponse(
            document_type=DocumentType.CONTRACT,
            entities=ExtractedEntities(),
            confidence=1.5,
            original_text="texto",
        )