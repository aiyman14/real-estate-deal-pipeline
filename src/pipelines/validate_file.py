from pathlib import Path
from typing import Any, Dict, List, Tuple

from src.ingest.read_tsv import read_tsv
from src.validate.schema_loader import load_schema
from src.validate.validators import validate_row


def validate_tsv(schema_path: str, tsv_path: Path) -> Tuple[bool, List[str]]:
    schema: Dict[str, Any] = load_schema(schema_path)
    rows = read_tsv(tsv_path)

    if not rows:
        return False, [f"No data rows found in TSV: {tsv_path}"]

    all_errors: List[str] = []
    ok_all = True

    for i, row in enumerate(rows, start=1):
        ok, errs = validate_row(schema, row)
        if not ok:
            ok_all = False
            for e in errs:
                all_errors.append(f"Row {i}: {e}")

    return ok_all, all_errors
