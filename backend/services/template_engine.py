import re
from typing import Tuple, Dict

class TemplateEngine:
    """
    Convert plain text into a reusable template by replacing entities with placeholders.
    """

    @staticmethod
    def convert_to_template(text: str) -> Tuple[str, Dict[str, str]]:
        """
        Args:
            text: Extracted text from parser

        Returns:
            template_text: Text with placeholders like {{NAME}}
            metadata: Mapping of placeholders to example values
        """
        metadata = {}

        # Example: Detect names (simple heuristic: capitalized words)
        name_pattern = r"\b[A-Z][a-z]+\b"
        names = list(set(re.findall(name_pattern, text)))
        for i, name in enumerate(names, start=1):
            placeholder = f"{{{{NAME{i}}}}}"
            text = text.replace(name, placeholder)
            metadata[placeholder] = name

        # Example: Detect dates (simple heuristic: DD/MM/YYYY or YYYY-MM-DD)
        date_pattern = r"\b\d{2}/\d{2}/\d{4}\b|\b\d{4}-\d{2}-\d{2}\b"
        dates = list(set(re.findall(date_pattern, text)))
        for i, date in enumerate(dates, start=1):
            placeholder = f"{{{{DATE{i}}}}}"
            text = text.replace(date, placeholder)
            metadata[placeholder] = date

        return text, metadata
