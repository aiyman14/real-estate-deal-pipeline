from pathlib import Path
from typing import Any, Dict, List, Tuple

from src.ingest.read_tsv import read_tsv
from src.output.write_tsv import write_tsv
from src.validate.schema_loader import load_schema

from src.normalize.load_mappings import load_yaml
from src.normalize.row_normalizer import normalize_inbound_row, normalize_transactions_row


def normalize_tsv(schema_path: str, tsv_path: Path, out_path: Path, mode: str) -> Tuple[bool, str]:
    """
    mode: inbound | transactions
    """
    schema: Dict[str, Any] = load_schema(schema_path)
    rows = read_tsv(tsv_path)

    if not rows:
        return False, f"No data rows found in TSV: {tsv_path}"

    prop_map = load_yaml("config/mappings/property_type_map.yml")

    normalized_rows: List[Dict[str, Any]] = []
    for r in rows:
        if mode == "inbound":
            nr, _meta = normalize_inbound_row(r, prop_map)
        elif mode == "transactions":
            nr, _meta = normalize_transactions_row(r, prop_map)
        else:
            return False, f"Unknown mode: {mode}"
        normalized_rows.append(nr)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    write_tsv(out_path, schema, normalized_rows)
    return True, f"Wrote normalized TSV: {out_path.resolve()}"
