"""
Row normalization: applies all field-level normalizers to a row.

Each normalizer returns (normalized_value, confidence) where confidence is:
- "high": successfully parsed/matched
- "medium": partial match or ambiguous
- "low": could not parse, returned empty or fallback
"""

from typing import Any, Dict, Tuple

from src.normalize.property_type import normalize_property_type
from src.normalize.date_normalizer import normalize_date
from src.normalize.number_normalizer import normalize_number, normalize_price, normalize_area, normalize_yield


# Field definitions for each schema type
# Maps field names to their normalization function

INBOUND_DATE_FIELDS = ["Date received"]
INBOUND_NUMBER_FIELDS = [
    "Leasable area, sqm",
    "Base rent incl. index, CCY/sqm",
    "NOI, CCY",
    "NOI, CCY/sqm",
    "WAULT, years",
    "Deal value, CCY",
    "Deal value, CCY/sqm",
    "Price, CCY",
    "Price, CCY/sqm",
]
INBOUND_YIELD_FIELDS = ["Yield", "Yield2", "Economic occupancy rate, %"]
INBOUND_PROPERTY_TYPE_FIELDS = ["Type", "Use"]

TRANSACTIONS_DATE_FIELDS = ["Date"]
TRANSACTIONS_NUMBER_FIELDS = [
    "Area, m2",
    "Price, SEK",
    "Price, DKK",
    "Price, EUR",
    "Price, CCY/m2",
]
TRANSACTIONS_YIELD_FIELDS = ["Yield"]
TRANSACTIONS_PROPERTY_TYPE_FIELDS = ["Property type"]


def normalize_inbound_row(row: Dict[str, Any], property_map: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Normalize an inbound deal row.

    Returns: (normalized_row, metadata)
    - metadata contains confidence scores for each normalized field
    """
    out = dict(row)
    meta: Dict[str, Any] = {}

    # Date fields
    for field in INBOUND_DATE_FIELDS:
        if field in out and out[field]:
            canon, conf = normalize_date(out[field])
            if canon:  # Only update if we got a valid result
                out[field] = canon
            meta[f"{field}_confidence"] = conf

    # Property type fields
    for field in INBOUND_PROPERTY_TYPE_FIELDS:
        if field in out and out[field]:
            canon, conf = normalize_property_type(out[field], property_map)
            meta[f"{field}_confidence"] = conf
            out[field] = canon

    # Number fields (prices, areas, etc.)
    for field in INBOUND_NUMBER_FIELDS:
        if field in out and out[field]:
            canon, conf = normalize_price(out[field])
            if canon != "":
                out[field] = canon
            meta[f"{field}_confidence"] = conf

    # Yield/percentage fields
    for field in INBOUND_YIELD_FIELDS:
        if field in out and out[field]:
            canon, conf = normalize_yield(out[field])
            if canon != "":
                out[field] = canon
            meta[f"{field}_confidence"] = conf

    return out, meta


def normalize_transactions_row(row: Dict[str, Any], property_map: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Normalize a transactions row.

    Returns: (normalized_row, metadata)
    - metadata contains confidence scores for each normalized field
    """
    out = dict(row)
    meta: Dict[str, Any] = {}

    # Date fields
    for field in TRANSACTIONS_DATE_FIELDS:
        if field in out and out[field]:
            canon, conf = normalize_date(out[field])
            if canon:  # Only update if we got a valid result
                out[field] = canon
            meta[f"{field}_confidence"] = conf

    # Property type fields
    for field in TRANSACTIONS_PROPERTY_TYPE_FIELDS:
        if field in out and out[field]:
            canon, conf = normalize_property_type(out[field], property_map)
            meta[f"{field}_confidence"] = conf
            out[field] = canon

    # Number fields (prices, areas)
    for field in TRANSACTIONS_NUMBER_FIELDS:
        if field in out and out[field]:
            canon, conf = normalize_price(out[field])
            if canon != "":
                out[field] = canon
            meta[f"{field}_confidence"] = conf

    # Yield fields
    for field in TRANSACTIONS_YIELD_FIELDS:
        if field in out and out[field]:
            canon, conf = normalize_yield(out[field])
            if canon != "":
                out[field] = canon
            meta[f"{field}_confidence"] = conf

    return out, meta
