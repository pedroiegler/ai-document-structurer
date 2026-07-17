from app.pipeline.validator import _clean_list, _calculate_confidence, validate_entities
from app.schemas.extraction import ExtractedEntities

def test_clean_list_removes_empty_strings():
    assert _clean_list(["João", "", "Maria"]) == ["João", "Maria"]

def test_clean_list_removes_duplicates():
    result = _clean_list(["Tech Ltda", "tech ltda", "TECH LTDA"])
    assert len(result) == 1

def test_clean_list_preserves_original_casing():
    result = _clean_list(["Tech Ltda", "tech ltda"])
    assert result[0] == "Tech Ltda"

def test_clean_list_strips_whitespace():
    assert _clean_list(["  João  ", "Maria"]) == ["João", "Maria"]

def test_calculate_confidence_all_fields():
    entities = ExtractedEntities(
        people=["João"],
        organizations=["Tech"],
        dates=["15/03/2024"],
        values=["R$ 50.000"],
        locations=["São Paulo"],
        key_terms=["contrato"],
    )
    assert _calculate_confidence(entities) == 1.0

def test_calculate_confidence_no_fields():
    entities = ExtractedEntities()
    assert _calculate_confidence(entities) == 0.0


def test_calculate_confidence_partial_fields():
    entities = ExtractedEntities(
        people=["João"],
        organizations=["Tech"],
    )
    assert _calculate_confidence(entities) == round(2 / 6, 2)


def test_validate_entities_removes_duplicates_and_empties():
    raw = ExtractedEntities(
        people=["João Silva", "", "joão silva"],
        organizations=["Tech Ltda"],
    )
    cleaned, confidence = validate_entities(raw)
    assert len(cleaned.people) == 1
    assert cleaned.people[0] == "João Silva"


def test_validate_entities_returns_confidence():
    entities = ExtractedEntities(people=["João"])
    _, confidence = validate_entities(entities)
    assert 0.0 <= confidence <= 1.0