"""Starter script for the Titanic notebook-to-Python refactoring exercise.

Use this file to turn the exploratory Titanic notebook into a small,
reusable Python workflow. The starter stays incomplete on purpose so you can
implement the key preprocessing and model-comparison steps yourself.
"""

from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split


def load_data() -> pd.DataFrame:
    """Load the local Titanic dataset.

    Data loading is already implemented so the exercise can focus on the two
    main refactoring tasks: preprocessing and model comparison.
    """

    data_path = Path(__file__).resolve().parents[3] / "data" / "titanic.csv"
    return pd.read_csv(data_path)


def preprocess(dataframe: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Convert raw Titanic rows into model-ready features and labels.

    Exercise steps:
    1. Work on a copy of the incoming DataFrame so helper functions stay safe.
    2. Fill missing values in `Age`, `Fare` and `Embarked`.
    3. Build `y` from `Survived`.
    4. Drop columns that are not part of this simple baseline feature set.
    5. One-hot encode categorical columns and return `(X, y)`.
    """

    # Copy-first is a good default in preprocessing code because it prevents
    # helper functions from mutating DataFrames owned by the caller.
    raise NotImplementedError(
        "Implement preprocess() using the notebook and lesson guide as reference."
    )


def train_and_score_models(X: pd.DataFrame, y: pd.Series) -> pd.DataFrame:
    """Train a few baseline models and compare their validation accuracy.

    Exercise steps:
    1. Split `(X, y)` into training and validation sets.
    2. Fit the baseline models listed below.
    3. Score each model on the validation split, not on the full training data.
    4. Return a sorted DataFrame with readable model names and scores.
    """

    # Keeping the model list imported here makes the exercise self-contained,
    # even before the function body is implemented.
    _ = (
        LogisticRegression,
        DecisionTreeClassifier,
        RandomForestClassifier,
        GaussianNB,
        train_test_split,
    )
    raise NotImplementedError(
        "Implement train_and_score_models() to return a readable score table."
    )


def main() -> None:
    """Load the dataset and explain the next implementation steps.

    The starter is meant to run, show the dataset shape, and point you toward
    the two functions you still need to complete.
    """

    data = load_data()
    print(f"Loaded Titanic data: {data.shape[0]} rows x {data.shape[1]} columns")
    print(
        "This starter module runs successfully, and the two core refactoring steps are still yours to implement."
    )

    try:
        X, y = preprocess(data)
        results = train_and_score_models(X, y)
    except NotImplementedError as exc:
        print(exc)
        print(
            "Next step: complete preprocess() and train_and_score_models() "
            "based on the notebook workflow. After your own attempt, "
            "titanic_solution.py can help you review your approach."
        )
        return

    print(results.to_string(index=False))


if __name__ == "__main__":
    main()
