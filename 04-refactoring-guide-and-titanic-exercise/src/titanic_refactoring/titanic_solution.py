"""Reference script for the Titanic notebook-to-Python refactoring exercise.

The goal is not to reproduce every notebook cell. The goal is to keep the
stable workflow in three readable steps: load data, preprocess features, and
compare baseline models.
"""

from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split


def load_data() -> pd.DataFrame:
    """Load the Titanic dataset from the repository data folder."""

    data_path = Path(__file__).resolve().parents[3] / "data" / "titanic.csv"
    return pd.read_csv(data_path)


def preprocess(dataframe: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Prepare model-ready features and target labels.

    Returns:
        X: preprocessed feature matrix
        y: binary survival target
    """

    # Copy-first keeps the helper predictable and avoids mutating caller-owned
    # DataFrames.
    df = dataframe.copy()

    # Median/mode imputations are simple, robust baselines for this kind of
    # small tabular dataset.
    df["Age"] = df["Age"].fillna(df["Age"].median())
    df["Fare"] = df["Fare"].fillna(df["Fare"].median())
    df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode().iloc[0])

    # Separate the target first so the remaining steps are clearly feature-only.
    y = df["Survived"].astype(int)

    # Drop ID and text-heavy columns that are outside the scope of this simple
    # baseline workflow.
    features = df.drop(columns=["Survived", "PassengerId", "Name", "Ticket", "Cabin"])

    # One-hot encode the remaining categorical columns. `drop_first=True` keeps
    # the matrix a little smaller for this compact baseline workflow.
    X = pd.get_dummies(features, columns=["Sex", "Embarked"], drop_first=True)
    return X, y


def train_and_score_models(X: pd.DataFrame, y: pd.Series) -> pd.DataFrame:
    """Train four baseline classifiers and return validation accuracy ranking.

    We use a single train/validation split for a compact baseline example.
    """

    # Stratification keeps the class balance similar across the split.
    X_train, X_valid, y_train, y_valid = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Model settings are kept simple and reproducible so the emphasis stays on
    # the refactoring pattern rather than hyperparameter tuning.
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42),
        "Gaussian NB": GaussianNB(),
    }

    scores: list[dict[str, float | str]] = []
    for name, model in models.items():
        # Fit on the training split, then score on held-out validation data.
        model.fit(X_train, y_train)
        score = model.score(X_valid, y_valid)
        scores.append({"Model": name, "ValidationAccuracy": round(score, 4)})

    # Sort best-performing models to the top for easy comparison
    return (
        pd.DataFrame(scores)
        .sort_values("ValidationAccuracy", ascending=False)
        .reset_index(drop=True)
    )


def main() -> None:
    """Run the full Titanic workflow and print a compact score table."""

    data = load_data()
    X, y = preprocess(data)
    results = train_and_score_models(X, y)
    print(f"Loaded Titanic data: {data.shape[0]} rows x {data.shape[1]} columns")
    print(f"Prepared feature matrix: {X.shape[0]} rows x {X.shape[1]} columns")
    print(results.to_string(index=False))


if __name__ == "__main__":
    main()
