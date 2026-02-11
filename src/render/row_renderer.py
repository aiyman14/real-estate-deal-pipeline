"""
Row renderer: converts normalized rows to paste-ready output.

Handles:
- Exact column ordering from schema
- Country-specific price column routing
- Derived field computation (price per m2)
- Value formatting for Excel compatibility
"""

from typing import Any, Dict, List, Optional
import json
from pathlib import Path


# Country -> Price column mapping for transactions
COUNTRY_PRICE_COLUMNS = {
    "Sweden": "Price, SEK",
    "Denmark": "Price, DKK",
    "Finland": "Price, EUR",
}


def render_transaction_row(
    row: Dict[str, Any],
    schema: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Render a transaction row for Excel output.

    - Routes generic "Price" to country-specific column
    - Computes Price, CCY/m2 if price and area are present
    - Returns dict with all schema columns (empty string for missing)
    """
    out = {}
    columns = [c["name"] for c in schema["columns"]]

    # Route price to correct country column
    country = row.get("Country", "")
    price = row.get("Price")
    if price and country in COUNTRY_PRICE_COLUMNS:
        price_col = COUNTRY_PRICE_COLUMNS[country]
        row[price_col] = price

    # Compute derived: Price, CCY/m2
    area = row.get("Area, m2")
    if price and area and isinstance(price, (int, float)) and isinstance(area, (int, float)) and area > 0:
        row["Price, CCY/m2"] = round(price / area)

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
    - Returns dict with all schema columns
    """
    out = {}
    columns = [c["name"] for c in schema["columns"]]

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
    if isinstance(val, float):
        # Check if it's a whole number
        if val.is_integer():
            return str(int(val))
        # Keep 2 decimal places for yields/percentages
        return f"{val:.2f}"
    return str(val)


def rows_to_tsv(
    rows: List[Dict[str, Any]],
    schema: Dict[str, Any],
    mode: str = "transactions",
) -> str:
    """
    Convert rows to TSV string ready for paste.

    Args:
        rows: List of normalized row dicts
        schema: Schema dict with columns
        mode: "transactions" or "inbound"

    Returns:
        TSV string with header row
    """
    columns = [c["name"] for c in schema["columns"]]
    lines = ["\t".join(columns)]

    render_fn = render_transaction_row if mode == "transactions" else render_inbound_row

    for row in rows:
        rendered = render_fn(row, schema)
        line = "\t".join(rendered[col] for col in columns)
        lines.append(line)

    return "\n".join(lines)


def row_to_tsv_line(
    row: Dict[str, Any],
    schema: Dict[str, Any],
    mode: str = "transactions",
    include_header: bool = False,
) -> str:
    """
    Convert a single row to TSV line(s).

    Useful for clipboard output of a single extracted row.
    """
    columns = [c["name"] for c in schema["columns"]]
    render_fn = render_transaction_row if mode == "transactions" else render_inbound_row

    rendered = render_fn(row, schema)
    data_line = "\t".join(rendered[col] for col in columns)

    if include_header:
        header_line = "\t".join(columns)
        return f"{header_line}\n{data_line}"

    return data_line


def write_rendered_tsv(
    rows: List[Dict[str, Any]],
    schema: Dict[str, Any],
    output_path: Path,
    mode: str = "transactions",
) -> None:
    """Write rendered rows to TSV file."""
    tsv_content = rows_to_tsv(rows, schema, mode)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(tsv_content + "\n", encoding="utf-8")
