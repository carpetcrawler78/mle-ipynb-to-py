"""Reference transformers for the Seattle weather feature engineering exercises.

Each class follows the scikit-learn estimator API:
- `fit(...)` learns parameters from data (not needed here, so it returns `self`)
- `transform(...)` returns a transformed DataFrame copy
"""

import re
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class TempMinTransformer(BaseEstimator, TransformerMixin):
    """Convert `temp_min` strings (for example `42 F`) to Celsius floats."""

    def fit(self, X, y=None):
        # This transformer is stateless, but we still expose a fitted attribute so
        # sklearn pipelines can call `.transform(...)` later without errors.
        self.is_fitted_ = True
        return self

    def transform(self, X, y=None):
        # Always copy first so we do not mutate upstream data in a pipeline.
        X_transformed = X.copy()
        # Example conversion: "50 F" -> (50 - 32) / 1.8 = 10.0
        X_transformed["temp_min"] = X_transformed["temp_min"].apply(
            lambda value: (float(str(value).strip(" F")) - 32) / 1.8
        )
        return X_transformed


class WeatherColumnTransformer(BaseEstimator, TransformerMixin):
    """Normalize shorthand weather labels into consistent full-category names."""

    def fit(self, X, y=None):
        # No learned parameters are required, but we still set a fitted flag for
        # sklearn's pipeline checks.
        self.is_fitted_ = True
        return self

    def transform(self, X, y=None):
        X_transformed = X.copy()
        # Map short labels to canonical labels used later in preprocessing.
        expressions = {
            r"\br\b": "rain",
            r"\bf\b": "fog",
            r"\b(sw|sn)\b": "snow",
            r"\bs\b": "sun",
            r"\b(d|driz)\b": "drizzle",
        }

        def normalize_weather(value):
            # Missing values often arrive as float NaN; keep them untouched.
            if isinstance(value, float):
                return value

            # Normalize casing/punctuation before regex replacement.
            cleaned_value = str(value).lower().strip(".")
            for key, replacement in expressions.items():
                cleaned_value = re.sub(key, replacement, cleaned_value)
            return cleaned_value

        X_transformed["weather"] = X_transformed["weather"].apply(normalize_weather)
        return X_transformed


class FloatColumnTransformer(BaseEstimator, TransformerMixin):
    """Clean the `precipitation` column and cast it to numeric."""

    def fit(self, X, y=None):
        # Stateless transformer; set a fitted flag so the pipeline can be reused.
        self.is_fitted_ = True
        return self

    def transform(self, X, y=None):
        X_transformed = X.copy()
        # Some rows may contain `$` or leading/trailing spaces from raw input.
        cleaned_column = (
            X_transformed["precipitation"]
            .astype(str)
            .str.replace("$", "", regex=False)
            .str.strip()
        )
        # `errors="coerce"` converts invalid entries to NaN instead of raising.
        X_transformed["precipitation"] = pd.to_numeric(cleaned_column, errors="coerce")
        return X_transformed


class DateColumnTransformer(BaseEstimator, TransformerMixin):
    """Convert the `date` column to pandas datetime values for pipeline use."""

    def fit(self, X, y=None):
        # Stateless transformer; set a fitted flag so the pipeline can be reused.
        self.is_fitted_ = True
        return self

    def transform(self, X, y=None):
        X_transformed = X.copy()
        # Invalid or malformed values become NaT (“Not a Time”) via `errors="coerce"`.
        # We cast to `object` afterward so ColumnTransformer can concatenate the
        # passthrough date column with numeric pipeline outputs in this example.
        X_transformed["date"] = pd.to_datetime(
            X_transformed["date"], errors="coerce"
        ).astype("object")
        return X_transformed
