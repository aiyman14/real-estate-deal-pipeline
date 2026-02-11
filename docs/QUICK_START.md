# Quick Start

## Setup

```bash
# Install dependencies
pip install anthropic pyyaml pytest

# Set API key
export ANTHROPIC_API_KEY="your-key-here"
```

---

## Process a News Article → Paste-Ready TSV

```bash
# Save article text to a file
echo "Your article text here..." > article.txt

# Run full pipeline
python -m src.cli process-article --input article.txt --url "https://source-url"
```

Output: Tab-separated row ready to paste into Excel.

---

## Process a PDF/Teaser → Paste-Ready TSV

```bash
# Save PDF text to a file (copy-paste from PDF)
echo "Your PDF text here..." > teaser.txt

# Run full pipeline
python -m src.cli process-pdf --input teaser.txt --date "2024/01/15"
```

---

## All CLI Commands

| Command | Purpose |
|---------|---------|
| `process-article` | Article → paste-ready TSV |
| `process-pdf` | PDF → paste-ready TSV |
| `extract-transaction` | Article → JSON (no TSV) |
| `extract-inbound` | PDF → JSON (no TSV) |
| `normalize-transactions` | Normalize existing TSV |
| `normalize-inbound` | Normalize existing TSV |
| `validate` | Validate TSV against schema |
| `scaffold-transactions` | Create empty TSV template |
| `scaffold-inbound` | Create empty TSV template |

---

## Run Tests

```bash
python -m pytest tests/ -v
```

---

## Project Structure

```
src/
├── extract/       # LLM extraction (Claude API)
├── normalize/     # Field normalization (dates, numbers, types)
├── render/        # TSV output formatting
├── pipelines/     # End-to-end flows
└── cli.py         # Command line interface

config/
├── schemas/       # Column definitions (transactions, inbound)
└── mappings/      # Synonym tables (property types)

tests/
└── fixtures/      # Sample inputs for testing
```
