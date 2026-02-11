# How to Add Mappings & Synonyms

Quick reference for maintaining normalization rules.

---

## Add a Property Type Synonym

**File:** `config/mappings/property_type_map.yml`

```yaml
synonyms:
  Office:
    - office
    - kontor
    - kontorsfastighet
    - YOUR_NEW_SYNONYM_HERE  # ← add here
```

**Rules:**
- Lowercase only
- One word/phrase per line
- Maps to canonical type (Office, Residential, Logistics, etc.)

**Test it:**
```bash
python -m pytest tests/test_row_normalizer.py -v
```

---

## Add a New Canonical Property Type

1. Add to `canonical_types` list in `property_type_map.yml`:
```yaml
canonical_types:
  - Office
  - Residential
  - YOUR_NEW_TYPE  # ← add here
```

2. Add synonyms for it:
```yaml
synonyms:
  YOUR_NEW_TYPE:
    - synonym1
    - synonym2
```

---

## Add a Country Synonym

**File:** `src/normalize/country_normalizer.py`

```python
COUNTRY_SYNONYMS = {
    # Add new variations here
    "your_variation": "Sweden",  # maps to canonical
}
```

**Canonical names:** Sweden, Denmark, Finland (must match schema)

---

## Add a Date Month Name

**File:** `src/normalize/date_normalizer.py`

```python
MONTH_MAP = {
    "januari": 1,
    "your_month_name": 3,  # ← add here (1-12)
}
```

---

## Add a Number Multiplier

**File:** `src/normalize/number_normalizer.py`

```python
MULTIPLIERS = {
    "msek": 1_000_000,
    "your_abbrev": 1_000_000,  # ← add here
}
```

---

## Quick Verification

After any change:
```bash
python -m pytest tests/ -v --tb=short
```

All 120 tests should pass.
