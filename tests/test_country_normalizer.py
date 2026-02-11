"""
Tests for country normalization.
"""

import pytest
from src.normalize.country_normalizer import normalize_country


class TestCountryNormalizer:
    """Test country normalization function."""

    # Swedish variations
    def test_sweden_canonical(self):
        assert normalize_country("Sweden") == ("Sweden", "high")

    def test_sweden_native(self):
        assert normalize_country("Sverige") == ("Sweden", "high")

    def test_sweden_code(self):
        assert normalize_country("SE") == ("Sweden", "high")

    def test_sweden_lowercase(self):
        assert normalize_country("sweden") == ("Sweden", "high")

    # Danish variations
    def test_denmark_canonical(self):
        assert normalize_country("Denmark") == ("Denmark", "high")

    def test_denmark_native(self):
        assert normalize_country("Danmark") == ("Denmark", "high")

    def test_denmark_code(self):
        assert normalize_country("DK") == ("Denmark", "high")

    # Finnish variations
    def test_finland_canonical(self):
        assert normalize_country("Finland") == ("Finland", "high")

    def test_finland_native(self):
        assert normalize_country("Suomi") == ("Finland", "high")

    def test_finland_code(self):
        assert normalize_country("FI") == ("Finland", "high")

    # Edge cases
    def test_empty_string(self):
        assert normalize_country("") == ("", "low")

    def test_none(self):
        assert normalize_country(None) == ("", "low")

    def test_unknown_country(self):
        """Unknown countries should return empty, not guess."""
        assert normalize_country("Norway") == ("", "low")
        assert normalize_country("Germany") == ("", "low")

    def test_case_insensitive(self):
        assert normalize_country("SWEDEN") == ("Sweden", "high")
        assert normalize_country("danmark") == ("Denmark", "high")
        assert normalize_country("SUOMI") == ("Finland", "high")
