"""
Tests for city name normalization.
"""

import pytest
from src.normalize.city_normalizer import normalize_city


class TestSwedishCities:
    """Test Swedish city name normalization."""

    def test_goteborg_to_gothenburg(self):
        """Test Göteborg -> Gothenburg."""
        result, conf = normalize_city("Göteborg")
        assert result == "Gothenburg"
        assert conf == "high"

    def test_malmo(self):
        """Test Malmö -> Malmo."""
        result, conf = normalize_city("Malmö")
        assert result == "Malmo"
        assert conf == "high"

    def test_linkoping(self):
        """Test Linköping -> Linkoping."""
        result, conf = normalize_city("Linköping")
        assert result == "Linkoping"
        assert conf == "high"

    def test_umea(self):
        """Test Umeå -> Umea."""
        result, conf = normalize_city("Umeå")
        assert result == "Umea"
        assert conf == "high"

    def test_case_insensitive(self):
        """Test case-insensitive matching."""
        result, conf = normalize_city("göteborg")
        assert result == "Gothenburg"
        assert conf == "high"

        result, conf = normalize_city("GÖTEBORG")
        assert result == "Gothenburg"
        assert conf == "high"


class TestNonSwedishCities:
    """Test cities that don't need normalization."""

    def test_stockholm_unchanged(self):
        """Test Stockholm stays unchanged (already English-friendly)."""
        result, conf = normalize_city("Stockholm")
        assert result == "Stockholm"
        assert conf == "medium"

    def test_english_city_unchanged(self):
        """Test English city names pass through."""
        result, conf = normalize_city("London")
        assert result == "London"
        assert conf == "medium"

    def test_already_normalized(self):
        """Test already-normalized names pass through."""
        result, conf = normalize_city("Gothenburg")
        assert result == "Gothenburg"
        assert conf == "medium"


class TestEdgeCases:
    """Test edge cases."""

    def test_empty_string(self):
        """Test empty string returns empty with low confidence."""
        result, conf = normalize_city("")
        assert result == ""
        assert conf == "low"

    def test_none(self):
        """Test None returns empty with low confidence."""
        result, conf = normalize_city(None)
        assert result == ""
        assert conf == "low"

    def test_whitespace_stripped(self):
        """Test whitespace is stripped."""
        result, conf = normalize_city("  Göteborg  ")
        assert result == "Gothenburg"
        assert conf == "high"


class TestNordicCities:
    """Test other Nordic city name normalization."""

    def test_copenhagen_swedish(self):
        """Test Swedish name for Copenhagen."""
        result, conf = normalize_city("Köpenhamn")
        assert result == "Copenhagen"
        assert conf == "high"

    def test_copenhagen_danish(self):
        """Test Danish name for Copenhagen."""
        result, conf = normalize_city("København")
        assert result == "Copenhagen"
        assert conf == "high"

    def test_helsinki_swedish(self):
        """Test Swedish name for Helsinki."""
        result, conf = normalize_city("Helsingfors")
        assert result == "Helsinki"
        assert conf == "high"

    def test_turku_swedish(self):
        """Test Swedish name for Turku (Åbo)."""
        result, conf = normalize_city("Åbo")
        assert result == "Turku"
        assert conf == "high"

    def test_aarhus_danish(self):
        """Test Danish spelling Århus -> Aarhus."""
        result, conf = normalize_city("Århus")
        assert result == "Aarhus"
        assert conf == "high"

    def test_finnish_cities_passthrough(self):
        """Test Finnish cities that don't need normalization pass through."""
        # Helsinki, Tampere, etc. are the same in Finnish and English
        result, conf = normalize_city("Helsinki")
        assert result == "Helsinki"
        assert conf == "medium"  # No mapping needed, passes through
