from pathlib import Path

from src.validate.schema_loader import load_schema
from src.output.write_tsv import write_tsv


def scaffold_inbound_tsv(out_path: Path) -> None:
    schema = load_schema("config/schemas/inbound_purple.schema.json")
    row = {col["name"]: "" for col in schema["columns"]}

    out_path.parent.mkdir(parents=True, exist_ok=True)
    write_tsv(out_path, schema, [row])

    print(f"Wrote: {out_path.resolve()}")


def scaffold_transactions_tsv(out_path: Path) -> None:
    schema = load_schema("config/schemas/transactions.schema.json")
    row = {col["name"]: "" for col in schema["columns"]}

    out_path.parent.mkdir(parents=True, exist_ok=True)
    write_tsv(out_path, schema, [row])

    print(f"Wrote: {out_path.resolve()}")