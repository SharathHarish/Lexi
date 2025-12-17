import re

def convert_to_template(text: str):
    """
    Converts raw document text into a template by
    replacing detected entities with placeholders.
    """
    # Simple heuristic: replace capitalized words
    candidates = re.findall(r"\b[A-Z][a-z]+\b", text)

    for word in set(candidates):
        text = text.replace(word, f"{{{{{word}}}}}")

    return text
