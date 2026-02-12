# Quick Start

## Setup

```bash
# Install all dependencies
pip install -r requirements.txt

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

## Batch Process PDFs

```bash
# Process all PDFs in a folder → single Excel file
python -m src.cli process-pdf-folder --folder /path/to/pdfs --out output/all_deals.xlsx

# With options
python -m src.cli process-pdf-folder --folder /path/to/pdfs --out output/deals.xlsx --date "2024/01/15" --max 10
```

Options:
- `--folder` - Path to folder containing PDF files (required)
- `--out` - Output Excel file (default: output/batch_inbound.xlsx)
- `--date` - Date received for all PDFs (optional)
- `--max` - Maximum PDFs to process (default: 20)

---

## All CLI Commands

| Command | Purpose |
|---------|---------|
| `process-url` | Fetch URL → Excel output |
| `process-pdf-file` | PDF file → Excel output |
| `process-pdf-folder` | Folder of PDFs → single Excel output |
| `process-article` | Article text file → TSV |
| `process-pdf` | PDF text file → TSV |
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
