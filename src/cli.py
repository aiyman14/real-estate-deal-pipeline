import argparse
from pathlib import Path

from src.pipelines.scaffold import scaffold_inbound_tsv, scaffold_transactions_tsv


def main() -> None:
    print("CLI MAIN RUNNING")

    parser = argparse.ArgumentParser(
        description="Real estate deal pipeline (scaffold phase)"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_in = sub.add_parser("scaffold-inbound", help="Write an empty inbound TSV using the inbound schema")
    p_in.add_argument("--out", default="output/inbound_rows.tsv")

    p_tx = sub.add_parser("scaffold-transactions", help="Write an empty transactions TSV using the transactions schema")
    p_tx.add_argument("--out", default="output/transaction_rows.tsv")

    args = parser.parse_args()

    if args.command == "scaffold-inbound":
        scaffold_inbound_tsv(Path(args.out))
    elif args.command == "scaffold-transactions":
        scaffold_transactions_tsv(Path(args.out))


if __name__ == "__main__":
    main()
