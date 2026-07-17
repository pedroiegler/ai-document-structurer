import re

def normalize_whitespace(text: str) -> str: 
    """
    Collapse multiple whitespace characters into a single space.
    """
    return re.sub(r"\s+", " ", text)
    
def remove_control_characters(text: str) -> str:
    """
    Remove non-printable control characters that may break processing.
    """
    return re.sub(r"[\x00-\x1F\x7F]", "", text)

def trim_text(text: str) -> str:
    """
    Remove leading and trailing whitespace.
    """
    return text.strip()

def preprocess_text(text: str) -> str:
    """
    Run the full preprocessing pipeline on the input text.

    Steps:
        1. Remove control characters
        2. Normalize whitespace
        3. Trim leading/trailing spaces
    """
    text = remove_control_characters(text)
    text = normalize_whitespace(text)
    text = trim_text(text)
    return text