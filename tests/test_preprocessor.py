import pytest
from app.pipeline.preprocessor import (
    remove_control_characters,
    normalize_whitespace,
    trim_text,
    preprocess_text
)

def test_normalize_whitespace_collapses_spaces():
    assert normalize_whitespace("This   is  a   test.") == "This is a test."

def test_normalize_whitespace_handles_newlines():
    assert normalize_whitespace("linha1\n\nlinha2") == "linha1 linha2"

def test_normalize_whitespace_handles_tabs():
    assert normalize_whitespace("texto\t\tcom\ttabs") == "texto com tabs"

def test_trim_text_removes_leading_spaces():
    assert trim_text("   texto") == "texto"

def test_trim_text_removes_trailing_spaces():
    assert trim_text("texto   ") == "texto"

def test_remove_control_characters_removes_null():
    assert remove_control_characters("texto\x00limpo") == "textolimpo"

def test_preprocess_text_full_pipeline():
    dirty = "   João Silva   assinou\n\n contrato   com a   Tech Ltda.   "
    result = preprocess_text(dirty)
    assert result == "João Silva assinou contrato com a Tech Ltda."

def test_preprocess_text_preserves_valid_content():
    text = "Texto válido sem problemas."
    assert preprocess_text(text) == text