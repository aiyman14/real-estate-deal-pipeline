"""
Tests for extraction module.

Note: Full extraction tests require ANTHROPIC_API_KEY.
These tests focus on the parsing and mapping logic.
"""

import pytest
import json
from src.extract.extractor import Extractor


class TestJsonParsing:
    """Test JSON response parsing."""

    def test_parse_clean_json(self):
        """Test parsing clean JSON response."""
        extractor = Extractor.__new__(Extractor)  # Create without __init__

        raw = '{"Country": "Sweden", "Buyer": "Balder"}'
        result = extractor._parse_json_response(raw)
        assert result == {"Country": "Sweden", "Buyer": "Balder"}

    def test_parse_json_with_markdown(self):
        """Test parsing JSON wrapped in markdown code blocks."""
        extractor = Extractor.__new__(Extractor)

        raw = '```json\n{"Country": "Sweden"}\n```'
        result = extractor._parse_json_response(raw)
        assert result == {"Country": "Sweden"}

    def test_parse_json_with_plain_markdown(self):
        """Test parsing JSON wrapped in plain code blocks."""
        extractor = Extractor.__new__(Extractor)

        raw = '```\n{"Country": "Denmark"}\n```'
        result = extractor._parse_json_response(raw)
        assert result == {"Country": "Denmark"}


class TestTransactionFieldMapping:
    """Test transaction field mapping."""

    def test_direct_field_mapping(self):
        """Test that direct fields are mapped correctly."""
        extractor = Extractor.__new__(Extractor)

        extracted = {
            "Country": "Sverige",
            "Date": "15 januari 2024",
            "Buyer": "Balder",
            "Seller": "Castellum",
            "Location": "Göteborg",
            "Property type": "kontor",
            "Comments": "Office sale in central Gothenburg.",
        }

        row = extractor._map_transaction_fields(extracted)

        assert row["Country"] == "Sverige"
        assert row["Date"] == "15 januari 2024"
        assert row["Buyer"] == "Balder"
        assert row["Seller"] == "Castellum"
        assert row["Property type"] == "kontor"

    def test_null_fields_excluded(self):
        """Test that null fields are not included in output."""
        extractor = Extractor.__new__(Extractor)

        extracted = {
            "Country": "Sweden",
            "Buyer": None,
            "Seller": "Test",
        }

        row = extractor._map_transaction_fields(extracted)

        assert "Buyer" not in row
        assert row["Seller"] == "Test"


class TestInboundFieldMapping:
    """Test inbound field mapping."""

    def test_field_name_mapping(self):
        """Test that field names are mapped to schema names."""
        extractor = Extractor.__new__(Extractor)

        extracted = {
            "Project Name": "Logistik Syd",
            "NOI": "28500000",
            "WAULT": "6.2",
            "Occupancy": "97%",
            "Comments": "Modern logistics portfolio.",
        }

        row = extractor._map_inbound_fields(extracted)

        assert row["Project Name"] == "Logistik Syd"
        assert row["NOI, CCY"] == "28500000"
        assert row["WAULT, years"] == "6.2"
        assert row["Economic occupancy rate, %"] == "97%"
        assert row["Comment"] == "Modern logistics portfolio."  # singular

    def test_portfolio_boolean(self):
        """Test portfolio field handles booleans."""
        extractor = Extractor.__new__(Extractor)

        extracted = {"Portfolio": True}
        row = extractor._map_inbound_fields(extracted)
        assert row["Portfolio"] is True

        extracted = {"Portfolio": False}
        row = extractor._map_inbound_fields(extracted)
        assert row["Portfolio"] is False
