from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class DocumentType(str, Enum):
    CONTRACT = "contract"
    MESSAGE = "message"
    DESCRIPTION = "description"
    UNKNOWN = "unknown"

class ExtractionRequest(BaseModel):
    text: str = Field(
        min_length=10,
        max_length=10000,
        description="The raw text to be processed and structured.",
        examples=["João Silva signed a contract with Tech Ltda on 15/03/2024."]
    )
    document_type: Optional[DocumentType] = Field(
        default=DocumentType.UNKNOWN,
        description="The type of document being processed."
    )

class ExtractedEntities(BaseModel):
    people: list[str] = Field(
        default_factory=list,
        description="List of people mentioned in the document."
    )
    organizations: list[str] = Field(
        default_factory=list,
        description="List of organizations mentioned in the document."
    )
    dates: list[str] = Field(
        default_factory=list,
        description="List of dates found in the document."
    )
    values: list[str] = Field(
        default_factory=list,
        description="List of monetary values found in the document."
    )
    locations: list[str] = Field(
        default_factory=list,
        description="List of locations mentioned in the document."
    )
    key_terms: list[str] = Field(
        default_factory=list,
        description="List of relevant domain-specific terms."
    )

class ExtractionResponse(BaseModel):
    document_type: DocumentType = Field(
        description="The identified or informed document type."
    )
    entities: ExtractedEntities = Field(
        description="All structured entities extracted from the text."
    )
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score of the extraction (0.0 to 1.0)."
    )
    original_text: str = Field(
        description="The original text that was processed."
    )