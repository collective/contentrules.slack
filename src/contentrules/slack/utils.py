"""Helpers for building Slack messages."""


def extract_fields_from_text(text: str) -> list[dict]:
    """Parse attachment field definitions, one per line.

    Each line has the format ``title|value|short``, and ``short`` is ``true``
    or ``false`` (case-insensitive; anything else reads as ``false``). A line
    without exactly three parts is skipped:

    .. code-block:: text

        Title|${title}|true
        Review State|${review_state_title}|false

    :param text: Field definitions, one per line.
    :returns: One ``{"title", "value", "short"}`` dictionary per valid line.
    """
    fields = []
    for item in text.split("\n"):
        try:
            title, value, short = item.split("|")
        except ValueError:
            continue
        fields.append({
            "title": title,
            "value": value,
            "short": short.lower() == "true",
        })
    return fields
