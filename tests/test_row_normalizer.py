"""
Tests for full row normalization.
"""

import pytest
import yaml
from pathlib import Path

from src.normalize.row_normalizer import normalize_inbound_row, normalize_transactions_row
from tests.fixtures.sample_rows import (
    SAMPLE_INBOUND_RAW,
    SAMPLE_INBOUND_EXPECTED,
    SAMPLE_TRANSACTIONS_RAW,
    SAMPLE_TRANSACTIONS_EXPECTED,
)


@pytest.fixture
def property_map():
    """Load the property type mapping."""
    map_path = Path(__file__).parent.parent / "config" / "mappings" / "property_type_map.yml"
    with open(map_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


class TestInboundRowNormalizer:
    """Test inbound row normalization."""

    def test_full_row_normalization(self, property_map):
        """Test that a complete inbound row normalizes correctly."""
        result, meta = normalize_inbound_row(SAMPLE_INBOUND_RAW, property_map)

        # Check each expected field
        for field, expected_value in SAMPLE_INBOUND_EXPECTED.items():
            assert result[field] == expected_value, (
                f"Field '{field}': got '{result[field]}', expected '{expected_value}'"
            )

    def test_date_normalized(self, property_map):
        """Test date field is normalized."""
        row = {"Date received": "15 januari 2024"}
        result, meta = normalize_inbound_row(row, property_map)
        assert result["Date received"] == "2024/01/15"
        assert meta["Date received_confidence"] == "high"

    def test_property_type_normalized(self, property_map):
        """Test property type (Use field) is normalized via synonyms.
        Note: 'Type' is document type (IM/Teaser), not property type.
        """
        row = {"Type": "IM", "Use": "warehouse"}
        result, meta = normalize_inbound_row(row, property_map)
        assert result["Type"] == "IM"  # Document type passes through unchanged
        assert result["Use"] == "Logistics"  # Property type gets normalized

    def test_numbers_normalized(self, property_map):
        """Test numeric fields are normalized."""
        row = {
            "Leasable area, sqm": "15 000",
            "NOI, CCY": "2.5M",
            "Yield": "4.5%",
        }
        result, meta = normalize_inbound_row(row, property_map)
        assert result["Leasable area, sqm"] == 15000
        assert result["NOI, CCY"] == 2500000
        assert result["Yield"] == 4.5

    def test_empty_fields_stay_empty(self, property_map):
        """Test that empty fields don't get filled with guesses."""
        row = {"Date received": "", "Type": "", "Yield": ""}
        result, meta = normalize_inbound_row(row, property_map)
        assert result["Date received"] == ""
        assert result["Type"] == ""
        assert result["Yield"] == ""

    def test_missing_fields_not_added(self, property_map):
        """Test that missing fields are not added to the output."""
        row = {"Project Name": "Test"}
        result, meta = normalize_inbound_row(row, property_map)
        assert "Date received" not in result
        assert "Type" not in result


class TestTransactionsRowNormalizer:
    """Test transactions row normalization."""

    def test_full_row_normalization(self, property_map):
        """Test that a complete transactions row normalizes correctly."""
        result, meta = normalize_transactions_row(SAMPLE_TRANSACTIONS_RAW, property_map)

        # Check each expected field
        for field, expected_value in SAMPLE_TRANSACTIONS_EXPECTED.items():
            assert result[field] == expected_value, (
                f"Field '{field}': got '{result[field]}', expected '{expected_value}'"
            )

    def test_date_normalized(self, property_map):
        """Test date field is normalized."""
        row = {"Date": "2024-01-15"}
        result, meta = normalize_transactions_row(row, property_map)
        assert result["Date"] == "2024/01/15"
        assert meta["Date_confidence"] == "high"

    def test_property_type_normalized(self, property_map):
        """Test property type is normalized via synonyms."""
        row = {"Property type": "lager"}
        result, meta = normalize_transactions_row(row, property_map)
        assert result["Property type"] == "Logistics"

    def test_price_field_passthrough(self, property_map):
        """Test Price field (already a number) passes through."""
        row = {"Price": 150}  # Price in millions, already a number
        result, meta = normalize_transactions_row(row, property_map)
        assert result["Price"] == 150  # Stays as-is

    def test_price_msek_string_normalized(self, property_map):
        """Test Price, MSEK field with string is normalized."""
        row = {"Price, MSEK": "150"}  # String number
        result, meta = normalize_transactions_row(row, property_map)
        assert result["Price, MSEK"] == 150  # Parsed to number


class TestConfidenceMetadata:
    """Test that confidence metadata is returned correctly."""

    def test_high_confidence_on_match(self, property_map):
        """Test high confidence when normalization succeeds."""
        row = {"Date": "2024-01-15", "Property type": "office"}
        _, meta = normalize_transactions_row(row, property_map)
        assert meta["Date_confidence"] == "high"
        assert meta["Property type_confidence"] == "high"

    def test_low_confidence_on_no_match(self, property_map):
        """Test low confidence when normalization fails."""
        row = {"Date": "not a date", "Property type": "xyz unknown type"}
        _, meta = normalize_transactions_row(row, property_map)
        assert meta["Date_confidence"] == "low"
        assert meta["Property type_confidence"] == "low"
