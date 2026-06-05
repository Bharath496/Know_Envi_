from __future__ import annotations

import argparse
import math
import sqlite3
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


sns.set_theme(style="whitegrid")


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names for notebook-style datasets."""
    cleaned = df.copy()
    cleaned.columns = (
        cleaned.columns.astype(str)
        .str.strip()
        .str.replace(r"\s+", "_", regex=True)
        .str.replace(r"[^0-9a-zA-Z_]+", "", regex=True)
        .str.lower()
    )
    return cleaned


def load_table(path: Path) -> pd.DataFrame:
    """Load a CSV, Excel, or SQLite table into a dataframe."""
    suffix = path.suffix.lower()

    if suffix == ".csv":
        return pd.read_csv(path)

    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)

    if suffix in {".db", ".sqlite", ".sqlite3"}:
        with sqlite3.connect(path) as conn:
            tables = pd.read_sql_query(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name",
                conn,
            )
            if tables.empty:
                raise ValueError(f"No tables found in database: {path}")
            table_name = tables.iloc[0, 0]
            return pd.read_sql_query(f"SELECT * FROM {table_name}", conn)

    raise ValueError(f"Unsupported file type: {path.suffix}")


def coerce_numeric_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Convert obvious numeric-like columns when safe."""
    coerced = df.copy()
    for col in coerced.columns:
        if coerced[col].dtype == object:
            converted = pd.to_numeric(coerced[col], errors="ignore")
            coerced[col] = converted
    return coerced


def save_plot(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, dpi=160, bbox_inches="tight")
    plt.close()


def plot_numeric_distributions(df: pd.DataFrame, output_dir: Path, limit: int = 9) -> None:
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if not numeric_cols:
        return

    selected = numeric_cols[:limit]
    rows = math.ceil(len(selected) / 3)
    fig, axes = plt.subplots(rows, 3, figsize=(15, 4 * rows))
    axes = np.atleast_1d(axes).ravel()

    for ax, col in zip(axes, selected, strict=False):
        sns.histplot(df[col].dropna(), kde=True, ax=ax, color="#2a6fdb")
        ax.set_title(f"Distribution: {col}")
        ax.set_xlabel(col)
        ax.set_ylabel("Count")

    for ax in axes[len(selected):]:
        ax.axis("off")

    save_plot(output_dir / "numeric_distributions.png")


def plot_categorical_counts(df: pd.DataFrame, output_dir: Path, limit: int = 6) -> None:
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    if not categorical_cols:
        return

    selected = categorical_cols[:limit]
    rows = math.ceil(len(selected) / 2)
    fig, axes = plt.subplots(rows, 2, figsize=(16, 5 * rows))
    axes = np.atleast_1d(axes).ravel()

    for ax, col in zip(axes, selected, strict=False):
        value_counts = df[col].astype(str).value_counts().head(12)
        sns.barplot(x=value_counts.values, y=value_counts.index, ax=ax, color="#5f8bff")
        ax.set_title(f"Category counts: {col}")
        ax.set_xlabel("Count")
        ax.set_ylabel(col)

    for ax in axes[len(selected):]:
        ax.axis("off")

    save_plot(output_dir / "categorical_counts.png")


def plot_correlation_heatmap(df: pd.DataFrame, output_dir: Path) -> None:
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.shape[1] < 2:
        return

    plt.figure(figsize=(12, 9))
    corr = numeric_df.corr(numeric_only=True)
    sns.heatmap(corr, cmap="coolwarm", center=0, annot=False, square=False)
    plt.title("Numeric Feature Correlation")
    save_plot(output_dir / "correlation_heatmap.png")


def plot_target_relationships(df: pd.DataFrame, output_dir: Path) -> None:
    lower_map = {c.lower(): c for c in df.columns}
    target_candidates = [
        "depression",
        "stress",
        "performance_index",
        "pi",
        "score",
        "marks",
    ]
    target = next((lower_map[name] for name in target_candidates if name in lower_map), None)
    if target is None:
        return

    numeric_cols = [c for c in df.select_dtypes(include=[np.number]).columns if c != target]
    if not numeric_cols:
        return

    top_features = numeric_cols[:4]
    rows = len(top_features)
    fig, axes = plt.subplots(rows, 1, figsize=(10, 4 * rows))
    axes = np.atleast_1d(axes)

    for ax, feature in zip(axes, top_features, strict=False):
        sns.scatterplot(data=df, x=feature, y=target, ax=ax, alpha=0.5)
        sns.regplot(data=df, x=feature, y=target, ax=ax, scatter=False, color="black")
        ax.set_title(f"{feature} vs {target}")

    save_plot(output_dir / "target_relationships.png")


def summarize_dataset(df: pd.DataFrame) -> None:
    print("\nShape:", df.shape)
    print("\nColumns:")
    for col in df.columns:
        print(" -", col)
    print("\nMissing values:")
    print(df.isna().sum().sort_values(ascending=False).head(20))
    print("\nNumeric summary:")
    numeric = df.select_dtypes(include=[np.number])
    if not numeric.empty:
        print(numeric.describe().T)


def run_analysis(input_path: Path, output_dir: Path) -> None:
    raw = load_table(input_path)
    df = normalize_columns(raw)
    df = coerce_numeric_frame(df)

    summarize_dataset(df)

    output_dir.mkdir(parents=True, exist_ok=True)
    plot_numeric_distributions(df, output_dir)
    plot_categorical_counts(df, output_dir)
    plot_correlation_heatmap(df, output_dir)
    plot_target_relationships(df, output_dir)

    df.to_csv(output_dir / "normalized_data_preview.csv", index=False)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Student dashboard analysis starter")
    parser.add_argument("input", type=Path, help="Path to CSV, Excel, or SQLite input")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs"),
        help="Directory where plots and previews will be saved",
    )
    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()
    run_analysis(args.input, args.output_dir)


if __name__ == "__main__":
    main()
