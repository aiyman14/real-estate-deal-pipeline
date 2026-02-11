# Quick Start

## Setup

```bash
# Install core dependencies
pip install anthropic pyyaml pytest

# For URL fetching (optional)
pip install requests beautifulsoup4

# For direct PDF reading (optional)
pip install pypdf

# Set API key
export ANTHROPIC_API_KEY="your-key-here"
```

---

## Process a News Article → Paste-Ready TSV

```bash
# From a text file
python -m src.cli process-article --input article.txt --url "https://source-url"

# From a URL directly (fetches and processes)
python -m src.cli process-url --url "https://example.com/news-article"
```

Output: Tab-separated row ready to paste into Excel.

---

## Process a PDF/Teaser → Paste-Ready TSV

```bash
# From text file (copy-paste from PDF)
python -m src.cli process-pdf --input teaser.txt --date "2024/01/15"

# From PDF file directly (requires: pip install pypdf)
python -m src.cli process-pdf-file --input teaser.pdf --date "2024/01/15"
```

---

## Extract Text from PDF (no LLM)

```bash
# Just extract text, save to file
python -m src.cli extract-pdf-text --input document.pdf --out document.txt
```

---

## All CLI Commands

| Command | Purpose |
|---------|---------|
| `process-article` | Article text file → paste-ready TSV |
| `process-url` | Fetch URL → paste-ready TSV |
| `process-pdf` | PDF text file → paste-ready TSV |
| `process-pdf-file` | PDF file directly → paste-ready TSV |
| `extract-pdf-text` | Extract text from PDF (no LLM) |
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
├── fetch/         # URL fetching & PDF text extraction
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
