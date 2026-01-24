import json
from pathlib import Path
from typing import Any, Dict


def load_schema(path: str) -> Dict[str, Any]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Schema not found: {p.resolve()}")
    return json.loads(p.read_text(encoding="utf-8"))