from typing import List


def extract_fields_from_text(text: str) -> List[dict]:
    """Extract field information from text.

    Example of valid data
    ```
    title|value|true
    title|value|false
    ```
    """
    fields = []
    for item in text.split("\n"):
        try:
            title, value, short = item.split("|")
        except ValueError:
            continue
        short = True if short.lower() == "true" else False
        fields.append({"title": title, "value": value, "short": short})
    return fields
