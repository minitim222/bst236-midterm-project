#!/usr/bin/env python3
"""
Generic Data Profiler for JAMA Paper Workflow

Scans a directory for data files (CSV, XLSX, TSV) and markdown/text files,
then produces a structured summary report suitable for research question
formulation and analysis planning.

Usage:
    python data_profiler.py /path/to/data/folder
    python data_profiler.py /path/to/data/folder > data_summary.md
"""

import sys
import os
from pathlib import Path
from collections import Counter
from typing import Dict, List, Optional

import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np


def read_text_files(data_dir: Path) -> Dict[str, str]:
    """Read all markdown and text files in the directory."""
    text_files = {}
    for ext in ('*.md', '*.txt', '*.MD', '*.TXT'):
        for f in sorted(data_dir.glob(ext)):
            try:
                text_files[f.name] = f.read_text(encoding='utf-8')
            except Exception as e:
                text_files[f.name] = f"[Error reading file: {e}]"
    return text_files


def load_dataframe(filepath: Path) -> Optional[pd.DataFrame]:
    """Load a data file into a DataFrame, handling common issues."""
    suffix = filepath.suffix.lower()
    try:
        if suffix == '.csv':
            for enc in ('utf-8', 'latin-1', 'cp1252'):
                try:
                    return pd.read_csv(filepath, encoding=enc, low_memory=False)
                except UnicodeDecodeError:
                    continue
            return pd.read_csv(filepath, encoding='latin-1', low_memory=False,
                               on_bad_lines='skip')
        elif suffix in ('.xlsx', '.xls'):
            return pd.read_excel(filepath, engine='openpyxl')
        elif suffix == '.tsv':
            return pd.read_csv(filepath, sep='\t', encoding='utf-8',
                               low_memory=False)
    except Exception as e:
        print(f"[Error loading {filepath.name}: {e}]")
    return None


def detect_date_columns(df: pd.DataFrame) -> List[str]:
    """Detect columns that likely contain dates."""
    date_cols = []
    for col in df.columns:
        if df[col].dtype == 'datetime64[ns]':
            date_cols.append(col)
            continue
        if df[col].dtype != 'object':
            continue
        col_lower = col.lower()
        if any(kw in col_lower for kw in ('date', 'time', 'year', 'month', 'week')):
            sample = df[col].dropna().head(20)
            try:
                pd.to_datetime(sample)
                date_cols.append(col)
            except (ValueError, TypeError):
                pass
    return date_cols


def profile_dataframe(filepath: Path, df: pd.DataFrame) -> str:
    """Generate a markdown profile for a single DataFrame."""
    lines = []
    lines.append(f"### {filepath.name}")
    lines.append(f"")
    lines.append(f"**Shape:** {df.shape[0]:,} rows x {df.shape[1]} columns")
    lines.append(f"")

    lines.append("**Columns:**")
    lines.append("")
    lines.append("| Column | Type | Non-Null | Missing | Missing % |")
    lines.append("|--------|------|----------|---------|-----------|")
    for col in df.columns:
        dtype = str(df[col].dtype)
        non_null = df[col].notna().sum()
        missing = df[col].isna().sum()
        miss_pct = missing / len(df) * 100 if len(df) > 0 else 0
        lines.append(f"| {col} | {dtype} | {non_null:,} | {missing:,} | {miss_pct:.1f}% |")
    lines.append("")

    lines.append("**First 5 rows:**")
    lines.append("")
    try:
        head_str = df.head(5).to_markdown(index=False)
        lines.append(head_str if head_str else "(empty)")
    except Exception:
        lines.append(df.head(5).to_string(index=False))
    lines.append("")

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if numeric_cols:
        lines.append("**Numeric Summary:**")
        lines.append("")
        try:
            desc = df[numeric_cols].describe().round(2)
            lines.append(desc.to_markdown())
        except Exception:
            lines.append(desc.to_string())
        lines.append("")

    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    if cat_cols:
        lines.append("**Categorical Columns (unique value counts):**")
        lines.append("")
        for col in cat_cols:
            n_unique = df[col].nunique()
            if n_unique <= 30:
                lines.append(f"- **{col}** ({n_unique} unique): "
                             + ", ".join(f"{v} ({c})"
                                        for v, c in df[col].value_counts().head(15).items()))
            else:
                lines.append(f"- **{col}**: {n_unique} unique values "
                             f"(top 5: {', '.join(str(v) for v in df[col].value_counts().head(5).index)})")
        lines.append("")

    date_cols = detect_date_columns(df)
    if date_cols:
        lines.append("**Date Columns:**")
        lines.append("")
        for col in date_cols:
            try:
                dates = pd.to_datetime(df[col], errors='coerce')
                valid = dates.dropna()
                if len(valid) > 0:
                    lines.append(f"- **{col}**: {valid.min()} to {valid.max()} "
                                 f"({len(valid):,} valid dates)")
            except Exception:
                lines.append(f"- **{col}**: (could not parse dates)")
        lines.append("")

    weight_cols = [c for c in df.columns
                   if any(kw in c.lower() for kw in ('weight', 'wgt', 'pweight', 'hweight'))]
    if weight_cols:
        lines.append(f"**Survey Weight Columns:** {', '.join(weight_cols)}")
        lines.append("")

    return "\n".join(lines)


def find_common_columns(dataframes: Dict[str, pd.DataFrame]) -> List[str]:
    """Find column names that appear in multiple dataframes."""
    col_counter = Counter()
    for df in dataframes.values():
        for col in df.columns:
            col_counter[col.lower()] += 1
    return [col for col, count in col_counter.most_common() if count > 1]


def main():
    if len(sys.argv) < 2:
        print("Usage: python data_profiler.py <data_directory>")
        sys.exit(1)

    data_dir = Path(sys.argv[1])
    if not data_dir.is_dir():
        print(f"Error: {data_dir} is not a directory")
        sys.exit(1)

    print("# Data Profile Report")
    print(f"\n**Directory:** `{data_dir}`\n")
    print(f"**Generated by:** data_profiler.py\n")
    print("---\n")

    text_files = read_text_files(data_dir)
    if text_files:
        print("## Documentation Files\n")
        for name, content in text_files.items():
            print(f"### {name}\n")
            print(content)
            print("\n---\n")

    data_extensions = ('*.csv', '*.xlsx', '*.xls', '*.tsv',
                       '*.CSV', '*.XLSX', '*.XLS', '*.TSV')
    data_files = []
    for ext in data_extensions:
        data_files.extend(sorted(data_dir.glob(ext)))
    for subdir in sorted(data_dir.iterdir()):
        if subdir.is_dir() and not subdir.name.startswith('.'):
            for ext in data_extensions:
                data_files.extend(sorted(subdir.glob(ext)))

    if not data_files:
        print("## No data files found\n")
        print("No CSV, XLSX, or TSV files were found in the directory.")
        return

    print(f"## Data Files ({len(data_files)} found)\n")

    dataframes = {}  # type: Dict[str, pd.DataFrame]
    for filepath in data_files:
        df = load_dataframe(filepath)
        if df is not None:
            rel = filepath.relative_to(data_dir)
            dataframes[str(rel)] = df
            print(profile_dataframe(filepath, df))
            print("---\n")
        else:
            print(f"### {filepath.name}\n")
            print("[Could not load this file]\n")
            print("---\n")

    if len(dataframes) > 1:
        common = find_common_columns(dataframes)
        if common:
            print("## Potential Merge Keys\n")
            print("Columns appearing in multiple datasets (case-insensitive):\n")
            for col in common[:20]:
                sources = [name for name, df in dataframes.items()
                           if col in [c.lower() for c in df.columns]]
                print(f"- **{col}** — found in: {', '.join(sources)}")
            print("")

    print("## Summary Statistics\n")
    print(f"- **Total datasets:** {len(dataframes)}")
    total_rows = sum(len(df) for df in dataframes.values())
    total_cols = sum(len(df.columns) for df in dataframes.values())
    print(f"- **Total rows across all datasets:** {total_rows:,}")
    print(f"- **Total columns across all datasets:** {total_cols}")

    all_cols = set()
    for df in dataframes.values():
        all_cols.update(c.lower() for c in df.columns)
    state_cols = [c for c in all_cols
                  if any(kw in c for kw in ('state', 'fips', 'jurisdiction', 'geography'))]
    if state_cols:
        print(f"- **Geographic columns detected:** {', '.join(state_cols)}")

    date_cols_all = set()
    for df in dataframes.values():
        date_cols_all.update(c.lower() for c in detect_date_columns(df))
    if date_cols_all:
        print(f"- **Date/time columns detected:** {', '.join(date_cols_all)}")

    weight_cols_all = set()
    for df in dataframes.values():
        for c in df.columns:
            if any(kw in c.lower() for kw in ('weight', 'wgt', 'pweight')):
                weight_cols_all.add(c.lower())
    if weight_cols_all:
        print(f"- **Survey weight columns detected:** {', '.join(weight_cols_all)}")

    print("")


if __name__ == '__main__':
    main()
