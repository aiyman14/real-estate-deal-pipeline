"""
Excel (.xlsx) output writer.
"""

from pathlib import Path
from typing import Any, Dict, List

try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill
except ImportError:
    Workbook = None


def write_excel(
    rows: List[Dict[str, Any]],
    columns: List[str],
    output_path: Path,
    sheet_name: str = "Deals",
) -> None:
    """
    Write rows to an Excel file.

    Args:
        rows: List of row dicts (already rendered/formatted)
        columns: Column names in order
        output_path: Path to .xlsx file
        sheet_name: Name of the worksheet
    """
    if Workbook is None:
        raise ImportError("openpyxl not installed. Run: pip install openpyxl")

    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name

    # Header row with styling
    header_font = Font(bold=True)
    header_fill = PatternFill(start_color="DDDDDD", end_color="DDDDDD", fill_type="solid")

    for col_idx, col_name in enumerate(columns, start=1):
        cell = ws.cell(row=1, column=col_idx, value=col_name)
        cell.font = header_font
        cell.fill = header_fill

    # Data rows
    for row_idx, row in enumerate(rows, start=2):
        for col_idx, col_name in enumerate(columns, start=1):
            value = row.get(col_name, "")
            ws.cell(row=row_idx, column=col_idx, value=value)

    # Auto-adjust column widths (approximate)
    for col_idx, col_name in enumerate(columns, start=1):
        max_length = len(col_name)
        for row in rows:
            val = str(row.get(col_name, ""))
            if len(val) > max_length:
                max_length = min(len(val), 50)  # Cap at 50
        ws.column_dimensions[ws.cell(row=1, column=col_idx).column_letter].width = max_length + 2

    # Save
    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(output_path)
