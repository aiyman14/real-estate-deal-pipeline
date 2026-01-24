from typing import Any, Dict, Tuple

from src.normalize.property_type import normalize_property_type


def normalize_inbound_row(row: Dict[str, Any], property_map: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    out = dict(row)
    meta: Dict[str, Any] = {}

    # Inbound files often use "Type" (your TSV shows this)
    if "Type" in out:
        canon, conf = normalize_property_type(out.get("Type", ""), property_map)
        meta["Type_confidence"] = conf
        out["Type"] = canon

    # Keep this too, in case later inbound schema uses "Use"
    if "Use" in out:
        canon, conf = normalize_property_type(out.get("Use", ""), property_map)
        meta["Use_confidence"] = conf
        out["Use"] = canon

    return out, meta


def normalize_transactions_row(row: Dict[str, Any], property_map: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    out = dict(row)
    meta: Dict[str, Any] = {}

    # Transactions: normalize "Property type" if present
    if "Property type" in out:
        canon, conf = normalize_property_type(out.get("Property type", ""), property_map)
        meta["Property type_confidence"] = conf
        out["Property type"] = canon

    return out, meta
