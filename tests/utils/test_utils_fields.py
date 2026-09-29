"""Parsing the ``title|value|short`` field definitions of an action."""

from contentrules.slack.utils import extract_fields_from_text

import pytest


class TestExtractFieldsFromText:
    @pytest.mark.parametrize(
        "text,expected",
        [
            ["title|value|true\ntitle|other|true", 2],
            ["title|value|true\n\n", 1],
            ["title|value|true", 1],
            ["", 0],
            ["title|value", 0],
            ["title|value|true|bar", 0],
            ["title|value\ntitle|value|true", 1],
        ],
    )
    def test_count(self, text: str, expected: int):
        assert len(extract_fields_from_text(text)) == expected

    def test_field(self):
        assert extract_fields_from_text("Review State|${review_state}|true") == [
            {"title": "Review State", "value": "${review_state}", "short": True}
        ]

    def test_keeps_order(self):
        result = extract_fields_from_text("first|1|true\nsecond|2|true")
        assert [field["title"] for field in result] == ["first", "second"]

    @pytest.mark.parametrize(
        "short,expected",
        [
            ["true", True],
            ["True", True],
            ["TRUE", True],
            ["false", False],
            ["False", False],
            ["yes", False],
            ["", False],
        ],
    )
    def test_short(self, short: str, expected: bool):
        result = extract_fields_from_text(f"title|value|{short}")
        assert result[0]["short"] is expected
