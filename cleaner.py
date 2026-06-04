"""csv-cleaner — one command to tidy a messy CSV.

Does the boring 80%: strips whitespace, normalises column names to snake_case,
drops fully-empty rows/columns, removes exact duplicate rows, infers numeric &
datetime types, and prints a missing-value report.

Usage:
    python cleaner.py messy.csv -o clean.csv
    python cleaner.py messy.csv --report-only
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import pandas as pd


def snake(name: str) -> str:
    name = str(name).strip()
    name = re.sub(r"[^\w]+", "_", name)
    name = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name)
    return re.sub(r"_+", "_", name).strip("_").lower()


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [snake(c) for c in df.columns]

    # trim whitespace in string cells
    for col in df.select_dtypes(include="object"):
        df[col] = df[col].map(lambda v: v.strip() if isinstance(v, str) else v)
        df[col] = df[col].replace({"": None})

    df = df.dropna(axis=0, how="all").dropna(axis=1, how="all")
    df = df.drop_duplicates(ignore_index=True)

    # try to upgrade object columns to numeric, then datetime
    for col in df.select_dtypes(include="object"):
        as_num = pd.to_numeric(df[col], errors="coerce")
        if as_num.notna().mean() >= 0.9:
            df[col] = as_num
            continue
        as_dt = pd.to_datetime(df[col], errors="coerce", format="mixed")
        if as_dt.notna().mean() >= 0.9:
            df[col] = as_dt
    return df


def missing_report(df: pd.DataFrame) -> pd.DataFrame:
    miss = df.isna().sum()
    pct = (miss / len(df) * 100).round(1) if len(df) else miss
    return pd.DataFrame({"missing": miss, "missing_pct": pct})


def main() -> None:
    ap = argparse.ArgumentParser(description="Clean a messy CSV file.")
    ap.add_argument("input", type=Path)
    ap.add_argument("-o", "--out", type=Path, help="output CSV path")
    ap.add_argument("--report-only", action="store_true", help="print report, don't write")
    args = ap.parse_args()

    raw = pd.read_csv(args.input)
    out = clean(raw)

    print(f"rows: {len(raw)} -> {len(out)} | cols: {raw.shape[1]} -> {out.shape[1]}")
    print("\nmissing values after cleaning:")
    print(missing_report(out).to_string())

    if args.report_only:
        return
    dest = args.out or args.input.with_name(args.input.stem + "_clean.csv")
    out.to_csv(dest, index=False)
    print(f"\nwrote {dest}")


if __name__ == "__main__":
    sys.exit(main())
