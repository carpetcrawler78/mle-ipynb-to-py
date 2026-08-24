"""Starter functions for the King County notebook-to-script refactoring lesson.

This file is the exercise version used alongside:
- `03-notebook-to-python-scripts/03-from-jupyter-notebook-to-python-scripts-example.ipynb`
- `03-notebook-to-python-scripts/king-county-data-preparation.ipynb`

Each function should:
- accept a pandas DataFrame,
- work on a copy,
- apply one focused transformation,
- and return the transformed DataFrame.
"""

from pathlib import Path

import numpy as np
import pandas as pd


def bath_bed_ratio_outlier(df):
    # Exercise goal: Remove outlier rows based on `bathrooms / bedrooms` ratio.
    # @TODO:
    # 1. Work on a DataFrame copy.
    # 2. Build a helper column named `bath_bed_ratio`.
    # 3. Mark rows where the ratio is >= 2 or <= 0.10.
    # 4. Keep only the rows that are inside the valid range.
    # 5. Drop the helper column before returning so the output schema matches the input schema.
    # Reference solution: `03-notebook-to-python-scripts/src/king_county_refactoring/data_preparation_solution.py`.

    # Work on a copy so callers keep their original DataFrame unchanged.
    df = df.copy()
    df["bath_bed_ratio"] = df["bathrooms"] / df["bedrooms"]
    df = df[(df["bath_bed_ratio"] < 2) & (df["bath_bed_ratio"] > 0.10)]
    df = df.drop(columns="bath_bed_ratio")
    return df


def sqft_basement(df):
    # Exercise goal: Recompute `sqft_basement` from reliable source columns.
    # @TODO:
    # 1. Work on a DataFrame copy.
    # 2. Recompute `sqft_basement` as `sqft_living - sqft_above`.
    # 3. Return the cleaned DataFrame.
    # Reference solution: `03-notebook-to-python-scripts/src/king_county_refactoring/data_preparation_solution.py`.

    # Keep this function deterministic: same input DataFrame -> same cleaned output.
    df = df.copy()
    df["sqft_basement"] = df["sqft_living"] - df["sqft_above"]
    return df

def _get_year(yr):
    return yr["yr_built"] if pd.isna(yr["yr_renovated"]) else yr["yr_renovated"]

def calculate_last_change(df):
    # Exercise goal: Create `last_known_change` from `yr_renovated` and `yr_built`.
    # @TODO:
    # 1. Work on a DataFrame copy.
    # 2. If `yr_renovated` is missing or 0, use `yr_built`.
    # 4. Create a new column named `last_known_change`.
    # 5. Drop `yr_renovated` and `yr_built` after creating the new column.
    # Reference solution: `03-notebook-to-python-scripts/src/king_county_refactoring/data_preparation_solution.py`.

    df = df.copy()
    yr_renovated = df["yr_renovated"]
    df["last_known_change"] = yr_renovated.where(
        yr_renovated.notna() & (yr_renovated != 0), df["yr_built"]
    ).astype("int64")
    df.drop(columns=["yr_renovated", "yr_built"], inplace=True)
    return df


def fill_missings_view_wf(df):
    # Exercise goal: Fill missing values in `view` and `waterfront` with 0.
    # @TODO:
    # 1. Work on a DataFrame copy.
    # 2. Fill missing values in `view` with 0.
    # 3. Fill missing values in `waterfront` with 0.
    # 4. Return the cleaned DataFrame.
    # Reference solution: `03-notebook-to-python-scripts/src/king_county_refactoring/data_preparation_solution.py`.

    # The output should keep the same columns as the input.
    df = df.copy()
    df['view']=df['view'].fillna(0)
    df['waterfront']=df['waterfront'].fillna(0)
    
    return df


def main() -> None:
    """Load the teaching dataset and list the starter tasks."""

    data_path = (
        Path(__file__).resolve().parents[3]
        / "data"
        / "King_County_House_prices_dataset.csv"
    )
    df = pd.read_csv(data_path)

    print("King County starter module loaded successfully.")
    print(
        "This starter module runs successfully. The four cleaning functions are still yours to implement."
    )
    print(f"Loaded dataset shape: {df.shape}")
    print("Starter functions to complete:")
    print("- bath_bed_ratio_outlier(df)")
    print("- sqft_basement(df)")
    print("- calculate_last_change(df)")
    print("- fill_missings_view_wf(df)")


if __name__ == "__main__":
    main()
