"""
Full pipeline: raw text -> extracted -> normalized -> rendered TSV.

This is the end-to-end flow for processing articles or PDFs.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from src.extract.extractor import Extractor, ExtractionError
from src.normalize.row_normalizer import normalize_transactions_row, normalize_inbound_row
from src.normalize.load_mappings import load_property_map
from src.render.row_renderer import row_to_tsv_line, render_transaction_row, render_inbound_row
from src.validate.schema_loader import load_schema


def process_article_to_tsv(
    article_text: str,
    source_url: str = "",
    include_header: bool = True,
    api_key: Optional[str] = None,
) -> Tuple[bool, str, str]:
    """
    Full pipeline: article text -> paste-ready TSV line.

    Returns:
        Tuple of (success, message, tsv_output)
        - tsv_output is the paste-ready TSV line(s)
    """
    try:
        # Load resources
        extractor = Extractor(api_key=api_key)
        property_map = load_property_map()
        schema = load_schema("config/schemas/transactions.schema.json")

        # Extract
        raw_row, extract_meta = extractor.extract_transaction(article_text, source_url)

        # Normalize
        normalized_row, norm_meta = normalize_transactions_row(raw_row, property_map)

        # Render
        tsv_line = row_to_tsv_line(
            normalized_row,
            schema,
            mode="transactions",
            include_header=include_header,
        )

        return True, "Success", tsv_line

    except ExtractionError as e:
        return False, f"Extraction failed: {e}", ""
    except Exception as e:
        return False, f"Error: {e}", ""


def process_pdf_to_tsv(
    document_text: str,
    date_received: str = "",
    include_header: bool = True,
    api_key: Optional[str] = None,
) -> Tuple[bool, str, str]:
    """
    Full pipeline: PDF text -> paste-ready TSV line.

    Returns:
        Tuple of (success, message, tsv_output)
    """
    try:
        # Load resources
        extractor = Extractor(api_key=api_key)
        property_map = load_property_map()
        schema = load_schema("config/schemas/inbound_purple.schema.json")

        # Extract
        raw_row, extract_meta = extractor.extract_inbound(document_text, date_received)

        # Normalize
        normalized_row, norm_meta = normalize_inbound_row(raw_row, property_map)

        # Render
        tsv_line = row_to_tsv_line(
            normalized_row,
            schema,
            mode="inbound",
            include_header=include_header,
        )

        return True, "Success", tsv_line

    except ExtractionError as e:
        return False, f"Extraction failed: {e}", ""
    except Exception as e:
        return False, f"Error: {e}", ""


def process_article_file(
    input_path: Path,
    output_path: Optional[Path] = None,
    source_url: str = "",
    api_key: Optional[str] = None,
) -> Tuple[bool, str, str]:
    """
    Process article file -> TSV output.

    If output_path provided, writes TSV to file.
    Always returns the TSV string.
    """
    try:
        article_text = input_path.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"Failed to read input: {e}", ""

    ok, msg, tsv = process_article_to_tsv(
        article_text,
        source_url,
        include_header=True,
        api_key=api_key,
    )

    if ok and output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(tsv + "\n", encoding="utf-8")

    return ok, msg, tsv


def process_pdf_file(
    input_path: Path,
    output_path: Optional[Path] = None,
    date_received: str = "",
    api_key: Optional[str] = None,
) -> Tuple[bool, str, str]:
    """
    Process PDF text file -> TSV output.
    """
    try:
        document_text = input_path.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"Failed to read input: {e}", ""

    ok, msg, tsv = process_pdf_to_tsv(
        document_text,
        date_received,
        include_header=True,
        api_key=api_key,
    )

    if ok and output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(tsv + "\n", encoding="utf-8")

    return ok, msg, tsv
