import re
from typing import Any, Dict, List, Tuple


DATE_RE = re.compile(r"^\d{4}/\d{2}/\d{2}$")


def _is_blank(v: Any) -> bool:
    if v is None:
        return True
    if isinstance(v, str) and v.strip() == "":
        return True
    return False


def _parse_number(v: Any) -> float:
    """
    Accepts numbers as strings with spaces/commas, e.g. '12 345', '12,345'.
    """
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().replace(" ", "").replace(",", "")
    return float(s)


def validate_row(schema: Dict[str, Any], row: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate a single row against a schema.
    Returns: (is_valid, errors)
    """
    errors: List[str] = []

    for col in schema.get("columns", []):
        name = col["name"]
        required = col.get("required", False)
        ctype = col.get("type", "string")
        value = row.get(name, "")

        # Required
        if required and _is_blank(value):
            errors.append(f"Missing required field: {name}")
            continue

        # If blank and not required, skip further checks
        if _is_blank(value):
            continue

        # Type checks
        if ctype == "date":
            fmt = col.get("format", "yyyy/mm/dd")
            if fmt == "yyyy/mm/dd" and not DATE_RE.match(str(value).strip()):
                errors.append(f"Invalid date format for {name}: '{value}' (expected yyyy/mm/dd)")

        elif ctype == "number":
            try:
                _parse_number(value)
            except Exception:
                errors.append(f"Invalid number for {name}: '{value}'")

        elif ctype == "integer":
            try:
                int(str(value).strip())
            except Exception:
                errors.append(f"Invalid integer for {name}: '{value}'")

        elif ctype == "boolean":
            v = str(value).strip().lower()
            if v not in {"true", "false", "yes", "no", "1", "0"}:
                errors.append(f"Invalid boolean for {name}: '{value}' (use true/false, yes/no, 1/0)")

        elif ctype == "enum":
            allowed = col.get("allowed_values")
            if isinstance(allowed, list) and str(value).strip() not in allowed:
                errors.append(f"Invalid enum for {name}: '{value}' (allowed: {allowed})")

    return (len(errors) == 0, errors)
