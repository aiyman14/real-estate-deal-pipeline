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


class TestSwedishAbbreviations:
    """Test Swedish-specific abbreviations added in Round 2."""

    def test_tkr_multiplier(self):
        """Test tkr (tusen kronor / thousand kronor) multiplier."""
        assert normalize_price("21 000 tkr")[0] == 21000000
        assert normalize_price("21000 tkr")[0] == 21000000
        assert normalize_price("5 624 tkr")[0] == 5624000

    def test_ar_suffix_stripped(self):
        """Test år (years) suffix is stripped from WAULT values."""
        result, conf = normalize_yield("11,8 år")
        assert result == 11.8
        assert conf == "high"

        result, conf = normalize_yield("11.8 år")
        assert result == 11.8
        assert conf == "high"

        result, conf = normalize_yield("15 år")
        assert result == 15
        assert conf == "high"

    def test_years_suffix_stripped(self):
        """Test years suffix is stripped."""
        result, conf = normalize_yield("5 years")
        assert result == 5
        assert conf == "high"

        result, conf = normalize_yield("3.5 year")
        assert result == 3.5
        assert conf == "high"


class TestSwedishTransactionFormats:
    """Test Swedish formats common in news articles (Round 3)."""

    def test_mkr_multiplier(self):
        """Test mkr (miljoner kronor) multiplier."""
        assert normalize_price("743 mkr")[0] == 743000000
        assert normalize_price("150 mkr")[0] == 150000000
        assert normalize_price("1,5 mkr")[0] == 1500000

    def test_procent_suffix(self):
        """Test procent (percent) suffix stripped."""
        result, conf = normalize_yield("7,2 procent")
        assert result == 7.2
        assert conf == "high"

        result, conf = normalize_yield("5.5 procent")
        assert result == 5.5
        assert conf == "high"

    def test_area_with_trailing_text(self):
        """Test area values with trailing Swedish descriptive text."""
        # The pre-processor should strip trailing text after the unit
        assert normalize_area("47696 kvm")[0] == 47696
        assert normalize_area("15000 m2")[0] == 15000

    def test_price_with_trailing_text(self):
        """Test price values with trailing text get the number extracted."""
        # "743 mkr underliggande fastighetsvärde" should extract "743 mkr"
        result, conf = normalize_price("743 mkr")
        assert result == 743000000
        assert conf == "high"
