from pathlib import Path

from src.validate.schema_loader import load_schema
from src.output.write_tsv import write_tsv


def scaffold_inbound_tsv(out_path: Path) -> None:
    schema = load_schema("config/schemas/inbound_purple.schema.json")
    row = {col["name"]: "" for col in schema["columns"]}

    out_path.parent.mkdir(parents=True, exist_ok=True)
    write_tsv(out_path, schema, [row])

    print(f"Wrote: {out_path.resolve()}")


def scaffold_transactions_tsv(out_path: Path, country: str = "Sweden") -> None:
    """
    Scaffold an empty transactions TSV with country-specific columns.

    Args:
        out_path: Output file path
        country: Country for column layout (Sweden, Denmark, Finland)
    """
    schema = load_schema("config/schemas/transactions.schema.json")

    # Get country-specific columns (default to Sweden)
    columns_key = f"columns_{country.lower()}"
    if columns_key in schema:
        columns = schema[columns_key]
    else:
        columns = schema.get("columns_sweden", [])

    row = {col["name"]: "" for col in columns}

    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Write with header
    header = [col["name"] for col in columns]
    out_path.write_text("\t".join(header) + "\n" + "\t".join([""] * len(header)) + "\n", encoding="utf-8")

    print(f"Wrote: {out_path.resolve()}")
