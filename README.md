# csv-cleaner

One command to tidy a messy CSV. Handles the boring 80% of data cleaning:

- normalises column names to `snake_case`
- strips whitespace, blanks → nulls
- drops fully-empty rows/columns
- removes exact duplicate rows
- infers numeric & datetime types
- prints a missing-value report

> Portfolio sample by **Vladimir Podlevskikh** — Python developer & automation engineer.
> Data wrangling / pandas pipelines are a service I offer.

## Run
```bash
pip install -r requirements.txt
python cleaner.py sample_messy.csv -o clean.csv
python cleaner.py sample_messy.csv --report-only
pytest -q
```

## Example
`sample_messy.csv` (whitespace, a duplicate, an empty row) →
clean output with `first_name, last_name, signup_date, spend`, typed and deduped.

## License
MIT
