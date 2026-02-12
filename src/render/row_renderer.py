"""
Row renderer: converts normalized rows to paste-ready output.

Handles:
- Exact column ordering from schema
- Country-specific column layouts for transactions
- Derived field computation (price per m2)
- Value formatting for Excel compatibility
"""

from datetime import date
from typing import Any, Dict, List, Optional
import json
from pathlib import Path


def get_transaction_columns(schema: Dict[str, Any], country: str) -> List[str]:
    """Get the column names for a specific country's transaction sheet."""
    key = f"columns_{country.lower()}"
    if key in schema:
        return [c["name"] for c in schema[key]]
    # Fallback to Sweden if country not found
    return [c["name"] for c in schema.get("columns_sweden", [])]


def render_transaction_row(
    row: Dict[str, Any],
    schema: Dict[str, Any],
    country: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Render a transaction row for Excel output.

    - Uses country-specific column layout
    - Computes Price/m2 if price and area are present
    - Returns dict with all schema columns (empty string for missing)
    """
    out = {}

    # Determine country for column layout
    country = country or row.get("Country", "Sweden")
    columns = get_transaction_columns(schema, country)

    # Price is already in millions from LLM, keep as-is
    price = row.get("Price")
    area = row.get("Area, m2")

    # Route price to correct column based on country
    if price is not None:
        if country == "Sweden":
            row["Price, MSEK"] = price
        elif country == "Denmark":
            row["Price, MDKK"] = price
        elif country == "Finland":
            row["Price, MEUR"] = price

    # Compute derived: Price/m2
    # Price is in millions, area in sqm, so: (price * 1_000_000) / area
    if price and area and isinstance(price, (int, float)) and isinstance(area, (int, float)) and area > 0:
        price_per_m2 = round((price * 1_000_000) / area)
        if country == "Sweden":
            row["Price, SEK/m2"] = price_per_m2
        elif country == "Denmark":
            row["Price, DKK/m2"] = price_per_m2
        elif country == "Finland":
            row["Price, EUR/m2"] = price_per_m2

    # Build output with all columns in order
    for col in columns:
        val = row.get(col, "")
        out[col] = _format_value(val)

    return out


def render_inbound_row(
    row: Dict[str, Any],
    schema: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Render an inbound row for Excel output.

    - Computes derived fields (NOI/sqm, Deal value/sqm, Price/sqm)
    - Computes Week nr. from Date received
    - Returns dict with all schema columns
    """
    out = {}
    columns = [c["name"] for c in schema["columns"]]

    # Map extraction field names to schema field names
    field_mapping = {
        "NOI": "NOI, CCY",
        "Base rent": "Base rent incl. index, CCY/sqm",
        "WAULT": "WAULT, years",
        "Occupancy": "Economic occupancy rate, %",
        "Deal value": "Deal value, CCY",
    }
    for old_key, new_key in field_mapping.items():
        if old_key in row and new_key not in row:
            row[new_key] = row[old_key]

    # Compute derived: NOI, CCY/sqm
    area = row.get("Leasable area, sqm")
    noi = row.get("NOI, CCY")
    if noi and area and isinstance(noi, (int, float)) and isinstance(area, (int, float)) and area > 0:
        row["NOI, CCY/sqm"] = round(noi / area)

    # Compute derived: Deal value, CCY/sqm
    deal_val = row.get("Deal value, CCY")
    if deal_val and area and isinstance(deal_val, (int, float)) and isinstance(area, (int, float)) and area > 0:
        row["Deal value, CCY/sqm"] = round(deal_val / area)

    # Compute derived: Price, CCY/sqm
    price = row.get("Price, CCY")
    if price and area and isinstance(price, (int, float)) and isinstance(area, (int, float)) and area > 0:
        row["Price, CCY/sqm"] = round(price / area)

    # Compute derived: Week nr. from Date received
    date_received = row.get("Date received")
    if date_received and isinstance(date_received, str) and "/" in date_received:
        try:
            parts = date_received.split("/")
            if len(parts) == 3:
                d = date(int(parts[0]), int(parts[1]), int(parts[2]))
                row["Week nr."] = d.isocalendar()[1]
        except (ValueError, IndexError):
            pass

    # Build output with all columns in order
    for col in columns:
        val = row.get(col, "")
        out[col] = _format_value(val)

    return out


def _format_value(val: Any) -> str:
    """Format a value for Excel paste."""
    if val is None:
        return ""
    if val == "":
        return ""
    if isinstance(val, bool):
        return "Yes" if val else "No"
    if isinstance(val, int):
        # Format integers with comma thousands separator
        return f"{val:,}"
    if isinstance(val, float):
        # Check if it's a whole number
        if val.is_integer():
            return f"{int(val):,}"
        # Keep 2 decimal places for yields/percentages
        return f"{val:.2f}"
    return str(val)


def rows_to_tsv(
    rows: List[Dict[str, Any]],
    schema: Dict[str, Any],
    mode: str = "transactions",
    country: Optional[str] = None,
) -> str:
    """
    Convert rows to TSV string ready for paste.

    Args:
        rows: List of normalized row dicts
        schema: Schema dict with columns
        mode: "transactions" or "inbound"
        country: For transactions, which country's column layout to use

    Returns:
        TSV string with header row
    """
    if mode == "transactions":
        # Use country from first row if not specified
        if not country and rows:
            country = rows[0].get("Country", "Sweden")
        columns = get_transaction_columns(schema, country or "Sweden")
    else:
        columns = [c["name"] for c in schema["columns"]]

    lines = ["\t".join(columns)]

    for row in rows:
        if mode == "transactions":
            rendered = render_transaction_row(row, schema, country)
        else:
            rendered = render_inbound_row(row, schema)
        line = "\t".join(rendered.get(col, "") for col in columns)
        lines.append(line)

    return "\n".join(lines)


def row_to_tsv_line(
    row: Dict[str, Any],
    schema: Dict[str, Any],
    mode: str = "transactions",
    include_header: bool = False,
    country: Optional[str] = None,
) -> str:
    """
    Convert a single row to TSV line(s).

    Useful for clipboard output of a single extracted row.
    """
    if mode == "transactions":
        country = country or row.get("Country", "Sweden")
        columns = get_transaction_columns(schema, country)
        rendered = render_transaction_row(row, schema, country)
    else:
        columns = [c["name"] for c in schema["columns"]]
        rendered = render_inbound_row(row, schema)

    data_line = "\t".join(rendered.get(col, "") for col in columns)

    if include_header:
        header_line = "\t".join(columns)
        return f"{header_line}\n{data_line}"

    return data_line


def write_rendered_tsv(
    rows: List[Dict[str, Any]],
    schema: Dict[str, Any],
    output_path: Path,
    mode: str = "transactions",
    country: Optional[str] = None,
) -> None:
    """Write rendered rows to TSV file."""
    tsv_content = rows_to_tsv(rows, schema, mode, country)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(tsv_content + "\n", encoding="utf-8")
