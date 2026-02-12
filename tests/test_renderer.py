"""
Tests for row renderer.
"""

import pytest
from src.render.row_renderer import (
    render_transaction_row,
    render_inbound_row,
    row_to_tsv_line,
    _format_value,
    get_transaction_columns,
)


# Minimal schema fixtures - now with country-specific column layouts
TRANSACTION_SCHEMA = {
    "columns_sweden": [
        {"name": "Country"},
        {"name": "Date"},
        {"name": "Buyer"},
        {"name": "Seller"},
        {"name": "Location"},
        {"name": "Property type"},
        {"name": "Property type 2"},
        {"name": "Main use (if Mixed use)"},
        {"name": "Use (if Development/Building rights)"},
        {"name": "Comment (if Redevelopment)"},
        {"name": "Comment (if Other)"},
        {"name": "Price, MSEK"},
        {"name": "Area, m2"},
        {"name": "Price, SEK/m2"},
        {"name": "Comments"},
        {"name": "Comments from Friday meeting"},
        {"name": "Yield"},
        {"name": "Project name"},
        {"name": "Broker"},
        {"name": "BRE received"},
        {"name": "Received by"},
        {"name": "BRE reviewed"},
        {"name": "BRE bid"},
        {"name": "Source"},
    ],
    "columns_denmark": [
        {"name": "Country"},
        {"name": "Date"},
        {"name": "Buyer"},
        {"name": "Seller"},
        {"name": "Location"},
        {"name": "Property type"},
        {"name": "Property type 2"},
        {"name": "Main use (if Mixed use)"},
        {"name": "Use (if Development/Building rights)"},
        {"name": "Comment (if Redevelopment)"},
        {"name": "Comment (if Other)"},
        {"name": "Price, MDKK"},
        {"name": "Area, m2"},
        {"name": "Price, DKK/m2"},
        {"name": "Comments"},
        {"name": "Comments from meeting"},
        {"name": "BRE received"},
        {"name": "BRE reviewed"},
        {"name": "BRE bid"},
        {"name": "Broker"},
        {"name": "Source"},
    ],
    "columns_finland": [
        {"name": "Source"},
        {"name": "Country"},
        {"name": "Date"},
        {"name": "Buyer"},
        {"name": "Seller"},
        {"name": "Location"},
        {"name": "Property type"},
        {"name": "Price, MEUR"},
        {"name": "Area, m2"},
        {"name": "Price, EUR/m2"},
        {"name": "Comments"},
        {"name": "Yield"},
        {"name": "Project name"},
        {"name": "Broker"},
        {"name": "BRE received"},
        {"name": "BRE reviewed"},
        {"name": "BRE bid"},
    ],
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
        """Price should route to Price, MSEK for Sweden (already in millions)."""
        row = {
            "Country": "Sweden",
            "Price": 150,  # Price is already in millions
        }
        rendered = render_transaction_row(row, TRANSACTION_SCHEMA)
        assert rendered["Price, MSEK"] == "150"

    def test_price_routed_to_denmark(self):
        row = {
            "Country": "Denmark",
            "Price": 50,  # Price in millions
        }
        rendered = render_transaction_row(row, TRANSACTION_SCHEMA)
        assert rendered["Price, MDKK"] == "50"

    def test_derived_price_per_sqm(self):
        """Price/m2 should be computed from price (in millions) and area."""
        row = {
            "Country": "Sweden",
            "Price": 150,  # 150 million
            "Area, m2": 10000,
        }
        rendered = render_transaction_row(row, TRANSACTION_SCHEMA)
        # 150,000,000 / 10,000 = 15,000 SEK/m2
        assert rendered["Price, SEK/m2"] == "15,000"

    def test_missing_columns_empty(self):
        """Missing columns should be empty strings."""
        row = {"Country": "Sweden"}
        rendered = render_transaction_row(row, TRANSACTION_SCHEMA)
        assert rendered["Buyer"] == ""
        assert rendered["Seller"] == ""


class TestGetTransactionColumns:
    """Test country-specific column selection."""

    def test_sweden_columns(self):
        cols = get_transaction_columns(TRANSACTION_SCHEMA, "Sweden")
        assert "Price, MSEK" in cols
        assert "Price, SEK/m2" in cols

    def test_denmark_columns(self):
        cols = get_transaction_columns(TRANSACTION_SCHEMA, "Denmark")
        assert "Price, MDKK" in cols
        assert "Price, DKK/m2" in cols

    def test_finland_columns(self):
        cols = get_transaction_columns(TRANSACTION_SCHEMA, "Finland")
        assert "Price, MEUR" in cols
        assert "Price, EUR/m2" in cols

    def test_fallback_to_sweden(self):
        """Unknown country should fall back to Sweden columns."""
        cols = get_transaction_columns(TRANSACTION_SCHEMA, "Norway")
        assert "Price, MSEK" in cols


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
        tsv = row_to_tsv_line(row, TRANSACTION_SCHEMA, mode="transactions", include_header=False, country="Denmark")
        assert "Country" not in tsv
        assert "Denmark" in tsv
