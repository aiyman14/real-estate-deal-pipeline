# Real Estate Deal Pipeline

Extracts structured deal data from news articles and broker PDFs (IMs/teasers) into Excel-ready rows for a deal tracker.

**Supports:** Sweden, Denmark, Finland

## Quick Install

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key-here"
```

## Usage

**Process a news article URL:**
```bash
python -m src.cli process-url --url "https://example.com/article" --out output/deal.xlsx
```

**Process a single PDF:**
```bash
python -m src.cli process-pdf-file --input deal.pdf --out output/deal.xlsx
```

**Batch process a folder of PDFs:**
```bash
python -m src.cli process-pdf-folder --folder /path/to/pdfs --out output/all_deals.xlsx
```

## Output

- Excel files (.xlsx) with formatted headers
- One row per deal with normalized fields (dates, prices, property types)
- Nordic number formats handled (mkr, tkr, procent)
- City names normalized to English (Göteborg → Gothenburg)

## Documentation

- [Quick Start Guide](docs/QUICK_START.md) - Full command reference
- [How to Add Mappings](docs/HOW_TO_ADD_MAPPINGS.md) - Extend synonyms and normalizers

## Run Tests

```bash
python -m pytest tests/ -v
```
