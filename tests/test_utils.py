from contentrules.slack import utils

import pytest


class TestExtractFields:
    @pytest.mark.parametrize(
        "text,fields",
        [
            ["title|value|true\ntitle|other|true", 2],
            ["title|value|true\n\n", 1],
            ["title|value|true", 1],
            ["title|value", 0],  # Wrong number of elements
            ["title|value|true|bar", 0],  # Wrong number of elements
        ],
    )
    def test_extract_fields_from_text(self, text: str, fields: int):
        result = utils.extract_fields_from_text(text)
        assert len(result) == fields
