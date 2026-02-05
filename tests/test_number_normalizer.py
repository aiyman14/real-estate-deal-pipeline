"""
Tests for number normalization.
"""

import pytest
from src.normalize.number_normalizer import normalize_number, normalize_price, normalize_yield, normalize_area
from tests.fixtures.sample_numbers import PRICE_TEST_CASES, YIELD_TEST_CASES, AREA_TEST_CASES


class TestPriceNormalizer:
    """Test price normalization (full integers)."""

    @pytest.mark.parametrize("input_val,expected_output,expected_conf", PRICE_TEST_CASES)
    def test_price_normalization(self, input_val, expected_output, expected_conf):
        """Test various price formats are normalized correctly."""
        result, confidence = normalize_price(input_val)
        assert result == expected_output, f"Input '{input_val}' -> got '{result}', expected '{expected_output}'"
        assert confidence == expected_conf, f"Input '{input_val}' -> confidence '{confidence}', expected '{expected_conf}'"


class TestYieldNormalizer:
    """Test yield/percentage normalization (preserves decimals)."""

    @pytest.mark.parametrize("input_val,expected_output,expected_conf", YIELD_TEST_CASES)
    def test_yield_normalization(self, input_val, expected_output, expected_conf):
        """Test yield values preserve decimals."""
        result, confidence = normalize_yield(input_val)
        assert result == expected_output, f"Input '{input_val}' -> got '{result}', expected '{expected_output}'"
        assert confidence == expected_conf


class TestAreaNormalizer:
    """Test area normalization (integers)."""

    @pytest.mark.parametrize("input_val,expected_output,expected_conf", AREA_TEST_CASES)
    def test_area_normalization(self, input_val, expected_output, expected_conf):
        """Test area values return integers."""
        result, confidence = normalize_area(input_val)
        assert result == expected_output, f"Input '{input_val}' -> got '{result}', expected '{expected_output}'"
        assert confidence == expected_conf


class TestMultipliers:
    """Test specific multiplier handling."""

    def test_millions_variations(self):
        """Test various million abbreviations."""
        assert normalize_price("1.5M")[0] == 1500000
        assert normalize_price("1.5m")[0] == 1500000
        assert normalize_price("1.5 million")[0] == 1500000
        assert normalize_price("1.5 miljoner")[0] == 1500000

    def test_billions_variations(self):
        """Test various billion abbreviations."""
        assert normalize_price("1.2 mdr")[0] == 1200000000
        assert normalize_price("1.2 miljarder")[0] == 1200000000
        assert normalize_price("1.2B")[0] == 1200000000

    def test_swedish_currency_multipliers(self):
        """Test MSEK/MDKK/MEUR abbreviations."""
        assert normalize_price("150 MSEK")[0] == 150000000
        assert normalize_price("50 MDKK")[0] == 50000000
        assert normalize_price("25 MEUR")[0] == 25000000


class TestNumberFormats:
    """Test number format handling (European vs US)."""

    def test_european_thousands(self):
        """Test European format with dots as thousands."""
        assert normalize_price("1.500.000")[0] == 1500000

    def test_us_thousands(self):
        """Test US format with commas as thousands."""
        assert normalize_price("1,500,000")[0] == 1500000

    def test_space_thousands(self):
        """Test space as thousands separator."""
        assert normalize_price("1 500 000")[0] == 1500000

    def test_european_decimal(self):
        """Test European decimal (comma)."""
        result, _ = normalize_yield("4,5")
        assert result == 4.5

    def test_mixed_format(self):
        """Test mixed European format (dots thousands, comma decimal)."""
        result, _ = normalize_number("1.500.000,50", as_integer=False)
        assert result == 1500000.5
