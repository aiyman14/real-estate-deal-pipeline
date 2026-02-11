from pathlib import Path
from typing import Any, Dict

import yaml


def load_yaml(path: str) -> Dict[str, Any]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Mapping file not found: {p.resolve()}")
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


def load_property_map() -> Dict[str, Any]:
    """Load the property type mapping file."""
    return load_yaml("config/mappings/property_type_map.yml")
