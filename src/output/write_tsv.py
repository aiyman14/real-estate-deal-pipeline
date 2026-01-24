from pathlib import Path
from typing import Any, Dict, List


def write_tsv(out_path: Path, schema: Dict[str, Any], rows: List[Dict[str, Any]]) -> None:
    """
    Writes TSV with columns in the exact schema order.
    """
    cols = [c["name"] for c in schema["columns"]]

    lines = []
    lines.append("\t".join(cols))

    for r in rows:
        vals = []
        for c in cols:
            v = r.get(c, "")
            if v is None:
                v = ""
            vals.append(str(v))
        lines.append("\t".join(vals))

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
