"""
Extraction pipeline: raw text -> extracted row -> normalized row -> output.

Combines extraction (LLM) with normalization for end-to-end processing.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from src.extract.extractor import Extractor, ExtractionError
from src.normalize.row_normalizer import normalize_transactions_row, normalize_inbound_row
from src.normalize.load_mappings import load_property_map


def extract_and_normalize_transaction(
    article_text: str,
    source_url: str = "",
    api_key: Optional[str] = None,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Extract and normalize a transaction from article text.

    Returns:
        Tuple of (normalized_row, metadata)
        - metadata includes extraction info and normalization confidence
    """
    extractor = Extractor(api_key=api_key)
    property_map = load_property_map()

    # Extract
    raw_row, extract_meta = extractor.extract_transaction(article_text, source_url)

    # Normalize
    normalized_row, norm_meta = normalize_transactions_row(raw_row, property_map)

    # Combine metadata
    metadata = {
        "extraction": extract_meta,
        "normalization": norm_meta,
    }

    return normalized_row, metadata


def extract_and_normalize_inbound(
    document_text: str,
    date_received: str = "",
    api_key: Optional[str] = None,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Extract and normalize an inbound deal from PDF text.

    Returns:
        Tuple of (normalized_row, metadata)
    """
    extractor = Extractor(api_key=api_key)
    property_map = load_property_map()

    # Extract
    raw_row, extract_meta = extractor.extract_inbound(document_text, date_received)

    # Normalize
    normalized_row, norm_meta = normalize_inbound_row(raw_row, property_map)

    # Combine metadata
    metadata = {
        "extraction": extract_meta,
        "normalization": norm_meta,
    }

    return normalized_row, metadata


def process_transaction_file(
    input_path: Path,
    output_path: Optional[Path] = None,
    source_url: str = "",
    api_key: Optional[str] = None,
) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Process a text file containing an article.

    Args:
        input_path: Path to text file with article content.
        output_path: Optional path to write JSON output.
        source_url: URL of the article.
        api_key: Anthropic API key.

    Returns:
        Tuple of (success, message, result_dict)
    """
    try:
        article_text = input_path.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"Failed to read input file: {e}", {}

    try:
        row, metadata = extract_and_normalize_transaction(
            article_text, source_url, api_key
        )
    except ExtractionError as e:
        return False, f"Extraction failed: {e}", {}
    except Exception as e:
        return False, f"Error: {e}", {}

    result = {
        "row": row,
        "metadata": metadata,
    }

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))

    return True, "Extraction successful", result


def process_inbound_file(
    input_path: Path,
    output_path: Optional[Path] = None,
    date_received: str = "",
    api_key: Optional[str] = None,
) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Process a text file containing PDF/IM content.

    Args:
        input_path: Path to text file with document content.
        output_path: Optional path to write JSON output.
        date_received: Date the document was received.
        api_key: Anthropic API key.

    Returns:
        Tuple of (success, message, result_dict)
    """
    try:
        document_text = input_path.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"Failed to read input file: {e}", {}

    try:
        row, metadata = extract_and_normalize_inbound(
            document_text, date_received, api_key
        )
    except ExtractionError as e:
        return False, f"Extraction failed: {e}", {}
    except Exception as e:
        return False, f"Error: {e}", {}

    result = {
        "row": row,
        "metadata": metadata,
    }

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))

    return True, "Extraction successful", result
