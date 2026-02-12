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

    # ---------- URL and direct PDF commands ----------
    p_url = sub.add_parser(
        "process-url",
        help="Fetch article from URL and process (requires ANTHROPIC_API_KEY)"
    )
    p_url.add_argument("--url", required=True, help="URL of the article")
    p_url.add_argument("--out", default=None, help="Output TSV/Excel path (optional)")

    p_pdf_direct = sub.add_parser(
        "process-pdf-file",
        help="Process PDF file directly (requires ANTHROPIC_API_KEY)"
    )
    p_pdf_direct.add_argument("--input", required=True, help="Path to PDF file")
    p_pdf_direct.add_argument("--out", default=None, help="Output TSV/Excel path (optional)")
    p_pdf_direct.add_argument("--date", default="", help="Date received (yyyy/mm/dd)")

    p_extract_pdf = sub.add_parser(
        "extract-pdf-text",
        help="Extract text from PDF file (no LLM, just text extraction)"
    )
    p_extract_pdf.add_argument("--input", required=True, help="Path to PDF file")
    p_extract_pdf.add_argument("--out", default=None, help="Output text file path")

    # ---------- Batch processing commands ----------
    p_batch_pdf = sub.add_parser(
        "process-pdf-folder",
        help="Process all PDFs in a folder -> single Excel output (requires ANTHROPIC_API_KEY)"
    )
    p_batch_pdf.add_argument("--folder", required=True, help="Path to folder containing PDF files")
    p_batch_pdf.add_argument("--out", default="output/batch_inbound.xlsx", help="Output Excel file path")
    p_batch_pdf.add_argument("--date", default="", help="Date received for all PDFs (yyyy/mm/dd)")
    p_batch_pdf.add_argument("--max", type=int, default=20, help="Maximum PDFs to process (default: 20)")

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

    elif args.command == "process-url":
        from src.pipelines.full_pipeline import process_article_url

        out_path = Path(args.out) if args.out else Path("output/article.xlsx")
        print(f"Processing: {args.url}")
        ok, msg, tsv = process_article_url(
            args.url,
            out_path,
        )
        if ok:
            print(f"Done. Output: {out_path}")
        else:
            print(f"FAILED: {msg}")

    elif args.command == "process-pdf-file":
        from src.pipelines.full_pipeline import process_pdf_direct

        out_path = Path(args.out) if args.out else Path("output/inbound.xlsx")
        print(f"Processing: {args.input}")
        ok, msg, tsv = process_pdf_direct(
            Path(args.input),
            out_path,
            args.date,
        )
        if ok:
            print(f"Done. Output: {out_path}")
        else:
            print(f"FAILED: {msg}")

    elif args.command == "extract-pdf-text":
        from src.fetch.pdf_reader import extract_text_from_pdf

        ok, msg, text = extract_text_from_pdf(Path(args.input))
        if ok:
            print(f"EXTRACTED ✅ ({msg})")
            print("-" * 40)
            if args.out:
                Path(args.out).write_text(text, encoding="utf-8")
                print(f"Saved to: {args.out}")
            else:
                print(text)
        else:
            print("FAILED ❌")
            print(msg)

    elif args.command == "process-pdf-folder":
        from src.pipelines.full_pipeline import process_pdf_folder

        folder = Path(args.folder)
        if not folder.is_dir():
            print(f"FAILED: Not a directory: {folder}")
        else:
            out_path = Path(args.out)
            print(f"Processing PDFs in: {folder}")
            ok, msg, results = process_pdf_folder(
                folder,
                out_path,
                args.date,
                max_files=args.max,
            )
            if ok:
                print(f"Done. {msg}")
                print(f"Output: {out_path}")
            else:
                print(f"FAILED: {msg}")


if __name__ == "__main__":
    main()
