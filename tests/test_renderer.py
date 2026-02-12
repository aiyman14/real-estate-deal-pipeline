"""
Tests for row renderer.
"""

import pytest
from src.render.row_renderer import (
    render_transaction_row,
    render_inbound_row,
    row_to_tsv_line,
    _format_value,
)


# Minimal schema fixtures
TRANSACTION_SCHEMA = {
    "columns": [
        {"name": "Country"},
        {"name": "Date"},
        {"name": "Buyer"},
        {"name": "Seller"},
        {"name": "Location"},
        {"name": "Property type"},
        {"name": "Area, m2"},
        {"name": "Price, SEK"},
        {"name": "Price, DKK"},
        {"name": "Price, EUR"},
        {"name": "Price, CCY/m2"},
        {"name": "Yield"},
        {"name": "Comments"},
        {"name": "Source URL"},
    ]
}

INBOUND_SCHEMA = {
    "columns": [
        {"name": "Project Name"},
        {"name": "Country"},
        {"name": "Location"},
        {"name": "Use"},
        {"name": "Leasable area, sqm"},
        {"name": "NOI, CCY"},
        {"name": "NOI, CCY/sqm"},
        {"name": "Yield"},
        {"name": "Portfolio"},
        {"name": "Comment"},
    ]
}


class TestFormatValue:
    """Test value formatting."""

    def test_none_becomes_empty(self):
        assert _format_value(None) == ""

    def test_empty_string_stays_empty(self):
        assert _format_value("") == ""

    def test_bool_true(self):
        assert _format_value(True) == "Yes"

    def test_bool_false(self):
        assert _format_value(False) == "No"

    def test_whole_float(self):
        assert _format_value(1500000.0) == "1,500,000"

    def test_decimal_float(self):
        assert _format_value(4.5) == "4.50"

    def test_integer(self):
        assert _format_value(1500000) == "1,500,000"

    def test_string_passthrough(self):
        assert _format_value("Stockholm") == "Stockholm"


class TestTransactionRenderer:
    """Test transaction row rendering."""

    def test_price_routed_to_sweden(self):
        """Price should route to Price, SEK for Sweden."""
        row = {
            "Country": "Sweden",
            "Price": 150000000,
        }
        rendered = render_transaction_row(row, TRANSACTION_SCHEMA)
        assert rendered["Price, SEK"] == "150,000,000"
        assert rendered["Price, DKK"] == ""
        assert rendered["Price, EUR"] == ""

    def test_price_routed_to_denmark(self):
        row = {
            "Country": "Denmark",
            "Price": 50000000,
        }
        rendered = render_transaction_row(row, TRANSACTION_SCHEMA)
        assert rendered["Price, DKK"] == "50,000,000"
        assert rendered["Price, SEK"] == ""

    def test_derived_price_per_sqm(self):
        """Price/m2 should be computed from price and area."""
        row = {
            "Country": "Sweden",
            "Price": 150000000,
            "Area, m2": 10000,
        }
        rendered = render_transaction_row(row, TRANSACTION_SCHEMA)
        assert rendered["Price, CCY/m2"] == "15,000"

    def test_missing_columns_empty(self):
        """Missing columns should be empty strings."""
        row = {"Country": "Sweden"}
        rendered = render_transaction_row(row, TRANSACTION_SCHEMA)
        assert rendered["Buyer"] == ""
        assert rendered["Seller"] == ""


class TestInboundRenderer:
    """Test inbound row rendering."""

    def test_derived_noi_per_sqm(self):
        row = {
            "NOI, CCY": 28500000,
            "Leasable area, sqm": 45000,
        }
        rendered = render_inbound_row(row, INBOUND_SCHEMA)
        assert rendered["NOI, CCY/sqm"] == "633"  # Small number, no comma needed

    def test_portfolio_boolean(self):
        row = {"Portfolio": True}
        rendered = render_inbound_row(row, INBOUND_SCHEMA)
        assert rendered["Portfolio"] == "Yes"


class TestTsvOutput:
    """Test TSV line generation."""

    def test_tsv_line_with_header(self):
        row = {"Country": "Sweden", "Location": "Stockholm"}
        tsv = row_to_tsv_line(row, TRANSACTION_SCHEMA, mode="transactions", include_header=True)
        lines = tsv.split("\n")
        assert len(lines) == 2
        assert "Country" in lines[0]
        assert "Sweden" in lines[1]

    def test_tsv_line_without_header(self):
        row = {"Country": "Denmark"}
        tsv = row_to_tsv_line(row, TRANSACTION_SCHEMA, mode="transactions", include_header=False)
        assert "Country" not in tsv
        assert "Denmark" in tsv
