import argparse
import json
from pathlib import Path

from src.pipelines.scaffold import scaffold_inbound_tsv, scaffold_transactions_tsv
from src.pipelines.validate_file import validate_tsv
from src.pipelines.normalize_file import normalize_tsv


def main() -> None:
    print("CLI MAIN RUNNING")

    parser = argparse.ArgumentParser(
        description="Real estate deal pipeline (scaffold + validation + normalization + extraction)"
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

    # ---------- Normalization commands (Phase 3) ----------
    p_nin = sub.add_parser(
        "normalize-inbound",
        help="Normalize inbound TSV (Use -> canonical)"
    )
    p_nin.add_argument("--tsv", required=True, help="Path to inbound TSV")
    p_nin.add_argument("--out", default="output/inbound_rows.normalized.tsv")

    p_ntx = sub.add_parser(
        "normalize-transactions",
        help="Normalize transactions TSV (Property type -> canonical)"
    )
    p_ntx.add_argument("--tsv", required=True, help="Path to transactions TSV")
    p_ntx.add_argument("--out", default="output/transaction_rows.normalized.tsv")

    # ---------- Extraction commands (Phase 4) ----------
    p_ext = sub.add_parser(
        "extract-transaction",
        help="Extract transaction from article text file (requires ANTHROPIC_API_KEY)"
    )
    p_ext.add_argument("--input", required=True, help="Path to text file with article")
    p_ext.add_argument("--out", default=None, help="Output JSON path (optional)")
    p_ext.add_argument("--url", default="", help="Source URL of the article")

    p_exi = sub.add_parser(
        "extract-inbound",
        help="Extract inbound deal from PDF text file (requires ANTHROPIC_API_KEY)"
    )
    p_exi.add_argument("--input", required=True, help="Path to text file with PDF content")
    p_exi.add_argument("--out", default=None, help="Output JSON path (optional)")
    p_exi.add_argument("--date", default="", help="Date received (yyyy/mm/dd)")

    # ---------- Full pipeline commands (Phase 5) ----------
    p_proc_tx = sub.add_parser(
        "process-article",
        help="Full pipeline: article -> paste-ready TSV (requires ANTHROPIC_API_KEY)"
    )
    p_proc_tx.add_argument("--input", required=True, help="Path to article text file")
    p_proc_tx.add_argument("--out", default=None, help="Output TSV path (optional)")
    p_proc_tx.add_argument("--url", default="", help="Source URL")

    p_proc_in = sub.add_parser(
        "process-pdf",
        help="Full pipeline: PDF text -> paste-ready TSV (requires ANTHROPIC_API_KEY)"
    )
    p_proc_in.add_argument("--input", required=True, help="Path to PDF text file")
    p_proc_in.add_argument("--out", default=None, help="Output TSV path (optional)")
    p_proc_in.add_argument("--date", default="", help="Date received (yyyy/mm/dd)")

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

    elif args.command == "normalize-inbound":
        ok, msg = normalize_tsv(
            "config/schemas/inbound_purple.schema.json",
            Path(args.tsv),
            Path(args.out),
            mode="inbound",
        )
        print("OK ✅" if ok else "FAILED ❌")
        print(msg)

    elif args.command == "normalize-transactions":
        ok, msg = normalize_tsv(
            "config/schemas/transactions.schema.json",
            Path(args.tsv),
            Path(args.out),
            mode="transactions",
        )
        print("OK ✅" if ok else "FAILED ❌")
        print(msg)

    elif args.command == "extract-transaction":
        from src.pipelines.extract_pipeline import process_transaction_file

        out_path = Path(args.out) if args.out else None
        ok, msg, result = process_transaction_file(
            Path(args.input),
            out_path,
            args.url,
        )
        if ok:
            print("EXTRACTED ✅")
            print(json.dumps(result["row"], indent=2, ensure_ascii=False))
        else:
            print("FAILED ❌")
            print(msg)

    elif args.command == "extract-inbound":
        from src.pipelines.extract_pipeline import process_inbound_file

        out_path = Path(args.out) if args.out else None
        ok, msg, result = process_inbound_file(
            Path(args.input),
            out_path,
            args.date,
        )
        if ok:
            print("EXTRACTED ✅")
            print(json.dumps(result["row"], indent=2, ensure_ascii=False))
        else:
            print("FAILED ❌")
            print(msg)

    elif args.command == "process-article":
        from src.pipelines.full_pipeline import process_article_file

        out_path = Path(args.out) if args.out else None
        ok, msg, tsv = process_article_file(
            Path(args.input),
            out_path,
            args.url,
        )
        if ok:
            print("READY TO PASTE ✅")
            print("-" * 40)
            print(tsv)
        else:
            print("FAILED ❌")
            print(msg)

    elif args.command == "process-pdf":
        from src.pipelines.full_pipeline import process_pdf_file

        out_path = Path(args.out) if args.out else None
        ok, msg, tsv = process_pdf_file(
            Path(args.input),
            out_path,
            args.date,
        )
        if ok:
            print("READY TO PASTE ✅")
            print("-" * 40)
            print(tsv)
        else:
            print("FAILED ❌")
            print(msg)


if __name__ == "__main__":
    main()
