"""
Full pipeline: raw text -> extracted -> normalized -> rendered TSV.

This is the end-to-end flow for processing articles or PDFs.
Supports: text files, URLs, and direct PDF files.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from src.extract.extractor import Extractor, ExtractionError
from src.normalize.row_normalizer import normalize_transactions_row, normalize_inbound_row
from src.normalize.load_mappings import load_property_map
from src.render.row_renderer import row_to_tsv_line, render_transaction_row, render_inbound_row
from src.render.excel_writer import write_excel
from src.validate.schema_loader import load_schema
from src.fetch.url_fetcher import fetch_article_from_url
from src.fetch.pdf_reader import extract_text_from_pdf


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
    Process article file -> TSV or Excel output.

    If output_path ends with .xlsx, writes Excel file.
    Otherwise writes TSV.
    Always returns the TSV string.
    """
    try:
        article_text = input_path.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"Failed to read input: {e}", ""

    try:
        # Load resources
        extractor = Extractor(api_key=api_key)
        property_map = load_property_map()
        schema = load_schema("config/schemas/transactions.schema.json")
        columns = [c["name"] for c in schema["columns"]]

        # Extract
        raw_row, extract_meta = extractor.extract_transaction(article_text, source_url)

        # Normalize
        normalized_row, norm_meta = normalize_transactions_row(raw_row, property_map)

        # Render
        rendered_row = render_transaction_row(normalized_row, schema)

        # Generate TSV for display
        tsv = row_to_tsv_line(normalized_row, schema, mode="transactions", include_header=True)

        # Write output file
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            if output_path.suffix.lower() == ".xlsx":
                write_excel([rendered_row], columns, output_path, sheet_name="Transactions")
            else:
                output_path.write_text(tsv + "\n", encoding="utf-8")

        return True, "Success", tsv

    except ExtractionError as e:
        return False, f"Extraction failed: {e}", ""
    except Exception as e:
        return False, f"Error: {e}", ""


def process_pdf_file(
    input_path: Path,
    output_path: Optional[Path] = None,
    date_received: str = "",
    api_key: Optional[str] = None,
) -> Tuple[bool, str, str]:
    """
    Process PDF text file -> TSV or Excel output.

    If output_path ends with .xlsx, writes Excel file.
    """
    try:
        document_text = input_path.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"Failed to read input: {e}", ""

    try:
        # Load resources
        extractor = Extractor(api_key=api_key)
        property_map = load_property_map()
        schema = load_schema("config/schemas/inbound_purple.schema.json")
        columns = [c["name"] for c in schema["columns"]]

        # Extract
        raw_row, extract_meta = extractor.extract_inbound(document_text, date_received)

        # Normalize
        normalized_row, norm_meta = normalize_inbound_row(raw_row, property_map)

        # Render
        rendered_row = render_inbound_row(normalized_row, schema)

        # Generate TSV for display
        tsv = row_to_tsv_line(normalized_row, schema, mode="inbound", include_header=True)

        # Write output file
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            if output_path.suffix.lower() == ".xlsx":
                write_excel([rendered_row], columns, output_path, sheet_name="Inbound")
            else:
                output_path.write_text(tsv + "\n", encoding="utf-8")

        return True, "Success", tsv

    except ExtractionError as e:
        return False, f"Extraction failed: {e}", ""
    except Exception as e:
        return False, f"Error: {e}", ""


def process_article_url(
    url: str,
    output_path: Optional[Path] = None,
    api_key: Optional[str] = None,
) -> Tuple[bool, str, str]:
    """
    Full pipeline: URL -> fetch article -> extract -> normalize -> TSV.

    Args:
        url: Article URL to fetch
        output_path: Optional output file (.tsv or .xlsx)
        api_key: Optional Anthropic API key

    Returns:
        Tuple of (success, message, tsv_output)
    """
    # Fetch article from URL
    ok, msg, article_text = fetch_article_from_url(url)
    if not ok:
        return False, f"Failed to fetch URL: {msg}", ""

    try:
        # Load resources
        extractor = Extractor(api_key=api_key)
        property_map = load_property_map()
        schema = load_schema("config/schemas/transactions.schema.json")
        columns = [c["name"] for c in schema["columns"]]

        # Extract (use the URL as source)
        raw_row, extract_meta = extractor.extract_transaction(article_text, url)

        # Normalize
        normalized_row, norm_meta = normalize_transactions_row(raw_row, property_map)

        # Render
        rendered_row = render_transaction_row(normalized_row, schema)

        # Generate TSV for display
        tsv = row_to_tsv_line(normalized_row, schema, mode="transactions", include_header=True)

        # Write output file
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            if output_path.suffix.lower() == ".xlsx":
                write_excel([rendered_row], columns, output_path, sheet_name="Transactions")
            else:
                output_path.write_text(tsv + "\n", encoding="utf-8")

        return True, "Success", tsv

    except ExtractionError as e:
        return False, f"Extraction failed: {e}", ""
    except Exception as e:
        return False, f"Error: {e}", ""


def process_pdf_direct(
    pdf_path: Path,
    output_path: Optional[Path] = None,
    date_received: str = "",
    api_key: Optional[str] = None,
) -> Tuple[bool, str, str]:
    """
    Full pipeline: PDF file -> extract text -> extract deal -> normalize -> TSV.

    Args:
        pdf_path: Path to PDF file
        output_path: Optional output file (.tsv or .xlsx)
        date_received: Date the PDF was received (yyyy/mm/dd)
        api_key: Optional Anthropic API key

    Returns:
        Tuple of (success, message, tsv_output)
    """
    # Extract text from PDF
    ok, msg, document_text = extract_text_from_pdf(pdf_path)
    if not ok:
        return False, f"Failed to read PDF: {msg}", ""

    try:
        # Load resources
        extractor = Extractor(api_key=api_key)
        property_map = load_property_map()
        schema = load_schema("config/schemas/inbound_purple.schema.json")
        columns = [c["name"] for c in schema["columns"]]

        # Extract
        raw_row, extract_meta = extractor.extract_inbound(document_text, date_received)

        # Normalize
        normalized_row, norm_meta = normalize_inbound_row(raw_row, property_map)

        # Render
        rendered_row = render_inbound_row(normalized_row, schema)

        # Generate TSV for display
        tsv = row_to_tsv_line(normalized_row, schema, mode="inbound", include_header=True)

        # Write output file
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            if output_path.suffix.lower() == ".xlsx":
                write_excel([rendered_row], columns, output_path, sheet_name="Inbound")
            else:
                output_path.write_text(tsv + "\n", encoding="utf-8")

        return True, "Success", tsv

    except ExtractionError as e:
        return False, f"Extraction failed: {e}", ""
    except Exception as e:
        return False, f"Error: {e}", ""


def process_pdf_folder(
    folder_path: Path,
    output_path: Optional[Path] = None,
    date_received: str = "",
    api_key: Optional[str] = None,
    max_files: int = 20,
) -> Tuple[bool, str, List[Dict[str, Any]]]:
    """
    Batch process all PDF files in a folder -> single Excel output.

    Args:
        folder_path: Path to folder containing PDF files
        output_path: Output Excel file path (.xlsx)
        date_received: Date the PDFs were received (yyyy/mm/dd)
        api_key: Optional Anthropic API key
        max_files: Maximum number of PDFs to process (default 20)

    Returns:
        Tuple of (success, message, list_of_results)
        - Each result is {"file": filename, "success": bool, "row": dict or None, "error": str or None}
    """
    # Find all PDF files in folder
    pdf_files = sorted(folder_path.glob("*.pdf"))
    if not pdf_files:
        return False, f"No PDF files found in {folder_path}", []

    if len(pdf_files) > max_files:
        pdf_files = pdf_files[:max_files]

    # Load resources once (shared across all PDFs)
    try:
        extractor = Extractor(api_key=api_key)
        property_map = load_property_map()
        schema = load_schema("config/schemas/inbound_purple.schema.json")
        columns = [c["name"] for c in schema["columns"]]
    except Exception as e:
        return False, f"Failed to load resources: {e}", []

    results: List[Dict[str, Any]] = []
    rendered_rows: List[Dict[str, Any]] = []
    success_count = 0
    fail_count = 0

    for i, pdf_path in enumerate(pdf_files, 1):
        print(f"[{i}/{len(pdf_files)}] {pdf_path.name}", end=" ... ", flush=True)

        # Extract text from PDF
        ok, msg, document_text = extract_text_from_pdf(pdf_path)
        if not ok:
            print("FAILED")
            results.append({"file": pdf_path.name, "success": False, "row": None, "error": msg})
            fail_count += 1
            continue

        try:
            # Extract deal data
            raw_row, extract_meta = extractor.extract_inbound(document_text, date_received)

            # Normalize
            normalized_row, norm_meta = normalize_inbound_row(raw_row, property_map)

            # Render
            rendered_row = render_inbound_row(normalized_row, schema)
            rendered_rows.append(rendered_row)

            results.append({"file": pdf_path.name, "success": True, "row": normalized_row, "error": None})
            success_count += 1
            print("OK")

        except ExtractionError as e:
            print("FAILED")
            results.append({"file": pdf_path.name, "success": False, "row": None, "error": str(e)})
            fail_count += 1
        except Exception as e:
            print("FAILED")
            results.append({"file": pdf_path.name, "success": False, "row": None, "error": str(e)})
            fail_count += 1

    # Write output file
    if output_path and rendered_rows:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        write_excel(rendered_rows, columns, output_path, sheet_name="Inbound")

    summary = f"Processed {len(pdf_files)} PDFs: {success_count} success, {fail_count} failed"
    return success_count > 0, summary, results