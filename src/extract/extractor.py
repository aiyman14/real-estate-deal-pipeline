"""
LLM-based extraction using Claude API.

Extracts structured data from raw text (articles or PDFs) and returns
a dict ready for normalization.
"""

import json
import os
from typing import Any, Dict, Optional, Tuple

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None

from src.extract.prompts import (
    TRANSACTIONS_SYSTEM_PROMPT,
    TRANSACTIONS_USER_PROMPT,
    INBOUND_SYSTEM_PROMPT,
    INBOUND_USER_PROMPT,
)


class ExtractionError(Exception):
    """Raised when extraction fails."""
    pass


class Extractor:
    """LLM-based extractor for real estate deal information."""

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-sonnet-4-20250514"):
        """
        Initialize the extractor.

        Args:
            api_key: Anthropic API key. If not provided, uses ANTHROPIC_API_KEY env var.
            model: Claude model to use.
        """
        if Anthropic is None:
            raise ImportError("anthropic package not installed. Run: pip install anthropic")

        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("No API key provided. Set ANTHROPIC_API_KEY or pass api_key.")

        self.client = Anthropic(api_key=self.api_key)
        self.model = model

    def extract_transaction(self, article_text: str, source_url: str = "") -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Extract transaction data from a news article.

        Args:
            article_text: Raw text from the news article.
            source_url: URL of the article (added to output).

        Returns:
            Tuple of (extracted_row, metadata)
            - extracted_row: Dict with schema-aligned field names
            - metadata: Dict with extraction info (model, tokens, etc.)
        """
        prompt = TRANSACTIONS_USER_PROMPT.format(article_text=article_text)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=TRANSACTIONS_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )

        # Parse response
        raw_output = response.content[0].text
        extracted = self._parse_json_response(raw_output)

        # Map to schema field names and add source
        row = self._map_transaction_fields(extracted)
        row["Source URL"] = source_url or "pasted-text"

        metadata = {
            "model": self.model,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
            "raw_response": raw_output,
        }

        return row, metadata

    def extract_inbound(self, document_text: str, date_received: str = "") -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Extract inbound deal data from PDF/IM text.

        Args:
            document_text: Raw text from the PDF/teaser.
            date_received: Date the document was received (added to output).

        Returns:
            Tuple of (extracted_row, metadata)
        """
        prompt = INBOUND_USER_PROMPT.format(document_text=document_text)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=INBOUND_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )

        # Parse response
        raw_output = response.content[0].text
        extracted = self._parse_json_response(raw_output)

        # Map to schema field names
        row = self._map_inbound_fields(extracted)
        if date_received:
            row["Date received"] = date_received

        metadata = {
            "model": self.model,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
            "raw_response": raw_output,
        }

        return row, metadata

    def _parse_json_response(self, raw_output: str) -> Dict[str, Any]:
        """Parse JSON from LLM response, handling markdown code blocks."""
        text = raw_output.strip()

        # Remove markdown code blocks if present
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]

        text = text.strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise ExtractionError(f"Failed to parse JSON response: {e}\nRaw: {raw_output}")

    def _map_transaction_fields(self, extracted: Dict[str, Any]) -> Dict[str, Any]:
        """Map extracted fields to transaction schema field names."""
        row = {}

        # Direct mappings
        direct_fields = [
            "Country", "Date", "Buyer", "Seller", "Location",
            "Property type", "Yield", "Broker", "Project name", "Comments"
        ]
        for field in direct_fields:
            if extracted.get(field) is not None:
                row[field] = extracted[field]

        # Area mapping
        if extracted.get("Area, m2") is not None:
            row["Area, m2"] = extracted["Area, m2"]

        # Price needs to be mapped to country-specific column
        # For now, store as generic "Price" - the pipeline will route it
        if extracted.get("Price") is not None:
            row["Price"] = extracted["Price"]

        return row

    def _map_inbound_fields(self, extracted: Dict[str, Any]) -> Dict[str, Any]:
        """Map extracted fields to inbound schema field names."""
        row = {}

        # Direct mappings
        direct_fields = [
            "Type", "Project Name", "Seller", "Broker", "Country", "Location",
            "Portfolio", "Address", "Postal code", "Property designation",
            "Comments"
        ]
        for field in direct_fields:
            if extracted.get(field) is not None:
                row[field] = extracted[field]

        # Field name mappings (extracted name -> schema name)
        mappings = {
            "Use": "Use",
            "Leasable area, sqm": "Leasable area, sqm",
            "Base rent": "Base rent incl. index, CCY/sqm",
            "NOI": "NOI, CCY",
            "WAULT": "WAULT, years",
            "Occupancy": "Economic occupancy rate, %",
            "Yield": "Yield",
            "Deal value": "Deal value, CCY",
        }

        for src, dst in mappings.items():
            if extracted.get(src) is not None:
                row[dst] = extracted[src]

        # Map Comments to Comment (schema uses singular)
        if "Comments" in row:
            row["Comment"] = row.pop("Comments")

        return row


def extract_transaction(article_text: str, source_url: str = "", api_key: Optional[str] = None) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Convenience function for extracting a single transaction."""
    extractor = Extractor(api_key=api_key)
    return extractor.extract_transaction(article_text, source_url)


def extract_inbound(document_text: str, date_received: str = "", api_key: Optional[str] = None) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Convenience function for extracting a single inbound deal."""
    extractor = Extractor(api_key=api_key)
    return extractor.extract_inbound(document_text, date_received)
