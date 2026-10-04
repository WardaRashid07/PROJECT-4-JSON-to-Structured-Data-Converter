# JSON to Structured Data Converter

A Python tool that reads semi-structured JSON data (array or newline-delimited), flattens nested objects and arrays, and converts the result into tabular formats (CSV and Parquet) suitable for downstream processing, databases, or analytics.

## Overview

Modern systems — APIs, event streams, log pipelines — commonly deliver data as JSON, often with nested objects and arrays that don't map cleanly onto a table. This tool:

- Loads JSON from either a JSON array file or a newline-delimited JSON (NDJSON) file, auto-detecting the format
- Inspects the dataset's schema: top-level keys, nested keys, and data types
- Filters out malformed records (null, empty, or missing a unique identifier) without crashing
- Recursively flattens nested objects into single-level keys using a configurable separator (default `__`)
- Converts first-level arrays into pipe-separated strings
- Fills in missing keys with `None` so every output record has a consistent, uniform column set
- Writes the flattened data to both CSV and Parquet
- Logs per-record parsing stats: total records, successful, and failed/skipped

## Input Format

The tool accepts either:

**A JSON array** — one file containing a list of objects:
```json
[
  {"id": "REC001", "event_timestamp": "2024-01-15T10:30:00", "category": "TypeA", "metrics": {"value_a": 1500, "value_b": 200}, "tags": ["urgent", "reviewed"]},
  {"id": "REC002", ...}
]
```

**Newline-delimited JSON (NDJSON)** — one complete JSON object per line, no wrapping brackets or commas:
```json
{"id": "REC001", "event_timestamp": "2024-01-15T10:30:00", "category": "TypeA", "metrics": {"value_a": 1500, "value_b": 200}, "tags": ["urgent", "reviewed"]}
{"id": "REC002", ...}
```

Format is detected automatically: the loader first attempts to parse the file as a single JSON array; if that fails, it falls back to parsing it line by line as NDJSON.

## Project Structure

```
project_04_json_converter/
├── data/
│   ├── records.json      # sample input, JSON array format
│   └── records.ndjson    # sample input, NDJSON format
├── output/
│   ├── output_flat.csv
│   └── output_flat.parquet
├── converter.py            # main driver: loads, filters, flattens, writes output
├── flattener.py              # recursive flattening logic
├── config.py                  # format loading, detection, separator config
├── requirements.txt
└── README.md
```

## Requirements

```
pandas
pyarrow
```

Install into a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
```

## Usage

```bash
python converter.py
```

This reads the configured input file, processes every record, and writes `output_flat.csv` and `output_flat.parquet` to the `output/` directory. A summary of processing results is printed to the console.

## How It Works

1. **Load.** `config.py` attempts `json.load()` on the whole file first (JSON array case). If that raises `json.JSONDecodeError`, it falls back to reading the file line by line and calling `json.loads()` on each line (NDJSON case). The loading logic lives inside a function and returns the parsed records — nothing runs automatically on import.

2. **Filter malformed records.** A record is treated as malformed and skipped if it is not a dictionary, is an empty dictionary, or is missing its `id` field. Skipped records are counted but do not stop processing.

3. **Flatten nested structures.** `flattener.py` defines a recursive `flatten()` function:
   - For a key whose value is a plain value (string, number, etc.), the key is kept (prefixed with its parent key and `__`, if nested).
   - For a key whose value is another dictionary, `flatten()` calls itself on that nested dictionary, carrying the growing key prefix forward — so nesting of any depth is handled without additional code.
   - For a key whose value is a list, the list is converted to a single pipe-separated string (e.g. `["urgent", "flagged"]` → `"urgent|flagged"`).

4. **Backfill missing keys.** Because fields like `sub_category` are optional and a record may be missing a nested key like `metrics.value_b`, the set of all keys that appear anywhere in the dataset is collected. Every flattened record is then checked against that full set, and any missing key is added with a value of `None`, so every row has the same columns.

5. **Write output.** The uniform, flattened records are written to `output_flat.csv` (via Python's `csv` module) and `output_flat.parquet` (via `pandas`/`pyarrow`).

6. **Log stats.** After processing, the total number of records read, the number successfully processed, and the number skipped as malformed are printed/logged once, as a final summary.

## Example

**Input record:**
```json
{
  "id": "REC001",
  "event_timestamp": "2024-01-15T10:30:00",
  "category": "TypeA",
  "metrics": {"value_a": 1500, "value_b": 200},
  "tags": ["urgent", "reviewed"]
}
```

**Flattened output row:**

| id | event_timestamp | category | metrics__value_a | metrics__value_b | tags |
|---|---|---|---|---|---|
| REC001 | 2024-01-15T10:30:00 | TypeA | 1500 | 200 | urgent\|reviewed |

## Sample Dataset

The included `data/records.json` / `data/records.ndjson` contain 1,200 synthetic records meeting the project's data requirements:

- A unique `id`, an `event_timestamp`, two categorical fields (`category`, `status`), two numeric fields nested under `metrics`, and a variable-length `tags` array
- An optional `sub_category` field present in roughly 15% of records
- ~6% of records missing the nested `metrics.value_b` key
- ~4% malformed records (null, empty object, or missing `id`)

## Design Notes

- **All parsing/flattening logic lives in functions**, not in global/module scope, so importing `config.py` or `flattener.py` has no side effects — nothing runs until explicitly called.
- **Flattening is recursive** rather than hardcoded to one level, so it correctly handles nested objects of any depth without additional branches.
- **Malformed-record detection and missing-key backfilling are separate concerns**: a record missing its `id` is rejected outright, while a valid record missing an optional or nested field is kept and padded with `None` rather than discarded.

## Possible Extensions

- Configurable "one row per array element" mode, as an alternative to pipe-joining
- Schema validation that rejects records missing specific required keys beyond `id`
- Automatic Parquet column type inference
- A standalone schema-introspection report, printed before conversion

## Author

Warda Rashid
