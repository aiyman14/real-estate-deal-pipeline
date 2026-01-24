import argparse
from pathlib import Path

from src.pipelines.scaffold import scaffold_inbound_tsv, scaffold_transactions_tsv
from src.pipelines.validate_file import validate_tsv   # ← NEW (Phase 2)


def main() -> None:
    print("CLI MAIN RUNNING")

    parser = argparse.ArgumentParser(
        description="Real estate deal pipeline (scaffold + validation phase)"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # ---------- Scaffold commands ----------
    p_in = sub.add_parser(
        "scaffold-inbound",
        help="Write an empty inbound TSV using the inbound schema"
    )
    p_in.add_argument("--out", default="output/inbound_rows.tsv")

    p_tx = sub.add_parser(
        "scaffold-transactions",
        help="Write an empty transactions TSV using the transactions schema"
    )
    p_tx.add_argument("--out", default="output/transaction_rows.tsv")

    # ---------- Validation command (Phase 2) ----------
    p_val = sub.add_parser(
        "validate",
        help="Validate a TSV file against a schema"
    )
    p_val.add_argument("--schema", required=True, help="Path to schema JSON")
    p_val.add_argument("--tsv", required=True, help="Path to TSV file")

    args = parser.parse_args()

    # ---------- Command dispatch ----------
    if args.command == "scaffold-inbound":
        scaffold_inbound_tsv(Path(args.out))

    elif args.command == "scaffold-transactions":
        scaffold_transactions_tsv(Path(args.out))

    elif args.command == "validate":
        ok, errors = validate_tsv(args.schema, Path(args.tsv))
        if ok:
            print("VALID ✅")
        else:
            print("INVALID ❌")
            for e in errors:
                print(f"  - {e}")


if __name__ == "__main__":
    main()
