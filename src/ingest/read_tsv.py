from pathlib import Path
from typing import Dict, List


def read_tsv(path: Path) -> List[Dict[str, str]]:
    """
    Reads a TSV where the first row is headers.
    Returns list of row dicts (all values as strings).
    """
    text = path.read_text(encoding="utf-8")
    lines = [ln for ln in text.splitlines() if ln.strip() != ""]
    if not lines:
        return []

    headers = lines[0].split("\t")
    rows: List[Dict[str, str]] = []

    for ln in lines[1:]:
        parts = ln.split("\t")
        # pad to length
        if len(parts) < len(headers):
            parts += [""] * (len(headers) - len(parts))
        row = {h: parts[i] for i, h in enumerate(headers)}
        rows.append(row)

    return rows
