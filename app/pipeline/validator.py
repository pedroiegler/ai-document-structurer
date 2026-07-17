from app.schemas.extraction import ExtractedEntities

def _clean_list(values: list[str]) -> list[str]:
    """
    Remove empty strings, duplicates, and normalize whitespace.
    """
    seen = set()
    result = []

    for item in values: 
        cleaned = item.strip()
        if cleaned and cleaned.lower() not in seen:
            seen.add(cleaned.lower())
            result.append(cleaned)
            
    return result

def _calculate_confidence(entities: ExtractedEntities) -> float:
    """
    Calculate a confidence score based on extraction completeness.
    """
    total_fields = 6
    filled_fields = sum([
        bool(entities.people),
        bool(entities.organizations),
        bool(entities.dates),
        bool(entities.values),
        bool(entities.locations),
        bool(entities.key_terms),
    ])

    return round(filled_fields / total_fields, 2)

def validate_entities(entities: ExtractedEntities) -> tuple[ExtractedEntities, float]:
    """
    Validate and clean extracted entities.
    Returns a cleaned ExtractedEntities and a confidence score.
    """
    cleaned = ExtractedEntities(
        people=_clean_list(entities.people),
        organizations=_clean_list(entities.organizations),
        dates=_clean_list(entities.dates),
        values=_clean_list(entities.values),
        locations=_clean_list(entities.locations),
        key_terms=_clean_list(entities.key_terms)
    )

    confidence = _calculate_confidence(cleaned)

    return cleaned, confidence
    