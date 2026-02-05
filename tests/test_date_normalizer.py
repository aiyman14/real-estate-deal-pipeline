"""
Tests for date normalization.
"""

import pytest
from src.normalize.date_normalizer import normalize_date
from tests.fixtures.sample_dates import DATE_TEST_CASES


class TestDateNormalizer:
    """Test date normalization function."""

    @pytest.mark.parametrize("input_val,expected_output,expected_conf", DATE_TEST_CASES)
    def test_date_normalization(self, input_val, expected_output, expected_conf):
        """Test various date formats are normalized correctly."""
        result, confidence = normalize_date(input_val)
        assert result == expected_output, f"Input '{input_val}' -> got '{result}', expected '{expected_output}'"
        assert confidence == expected_conf, f"Input '{input_val}' -> confidence '{confidence}', expected '{expected_conf}'"

    def test_already_normalized_unchanged(self):
        """Dates already in target format should pass through."""
        result, conf = normalize_date("2024/01/15")
        assert result == "2024/01/15"
        assert conf == "high"

    def test_padding_single_digits(self):
        """Single-digit months/days should be zero-padded."""
        result, _ = normalize_date("2024/1/5")
        assert result == "2024/01/05"

    def test_finnish_months(self):
        """Finnish month names should be recognized."""
        result, conf = normalize_date("15 tammikuu 2024")
        assert result == "2024/01/15"
        assert conf == "high"

    def test_danish_months(self):
        """Danish month names should be recognized."""
        result, conf = normalize_date("15 marts 2024")
        assert result == "2024/03/15"
        assert conf == "high"
