"""Seattle weather custom transformer exercises for notebook 02.

This file is the starter version used alongside the notebook.
Two example transformers are already implemented so the remaining TODO
exercises can stay focused. The solution file is there as a later
reference after your own attempt.
"""

import re

from sklearn.base import BaseEstimator, TransformerMixin


class TempMinTransformer(BaseEstimator, TransformerMixin):
    """Example transformer that converts `temp_min` from Fahrenheit to Celsius."""

    def fit(self, X, y=None):
        # Mark the transformer as fitted so sklearn pipelines can reuse it safely.
        self.is_fitted_ = True
        return self

    def transform(self, X, y=None):
        # Always work on a copy so earlier pipeline steps are not mutated in place.
        X_transformed = X.copy()
        X_transformed["temp_min"] = X_transformed["temp_min"].apply(
            lambda value: (float(str(value).strip(" F")) - 32) / 1.8
        )
        return X_transformed


class WeatherColumnTransformer(BaseEstimator, TransformerMixin):
    """Example transformer that normalizes shorthand weather labels."""

    def fit(self, X, y=None):
        # Regex cleanup is stateless, but we still mark the transformer as fitted.
        self.is_fitted_ = True
        return self

    def transform(self, X, y=None):
        # Copy first so repeated calls stay predictable inside a pipeline.
        X_transformed = X.copy()
        expressions = {
            r"\br\b": "rain",
            r"\bf\b": "fog",
            r"\b(sw|sn)\b": "snow",
            r"\bs\b": "sun",
            r"\b(d|driz)\b": "drizzle",
        }

        def normalize_weather(value):
            # Keep missing values untouched so later imputers can handle them.
            if isinstance(value, float):
                return value

            # Normalize case and punctuation before the regex replacements run.
            cleaned_value = str(value).lower().strip(".")
            for key, replacement in expressions.items():
                cleaned_value = re.sub(key, replacement, cleaned_value)
            return cleaned_value

        X_transformed["weather"] = X_transformed["weather"].apply(normalize_weather)
        return X_transformed


class FloatColumnTransformer(BaseEstimator, TransformerMixin):
    # Exercise goal: Clean `precipitation` and convert it to numeric.
    # @TODO:
    # 1. Keep the `X.copy()` pattern so this transformer does not mutate inputs.
    # 2. Remove `$` from `precipitation` (hint: use string methods).
    # 3. Convert values to numeric with `errors="coerce"` (hint: `pd.to_numeric`).
    # 4. Assign the cleaned result back to `X_transformed["precipitation"]`.
    # 5. Add `import pandas as pd` at the top of this file.
    # Starter file: `02-feature-engineering-with-sklearn-pipelines/src/pipeline/custom_transformer_seattle.py`.
    # Reference solution: `02-feature-engineering-with-sklearn-pipelines/src/pipeline/custom_transformer_seattle_solution.py`.
    def fit(self, X, y=None):
        # This transformer is also stateless, but sklearn still expects a fitted
        # estimator before a pipeline calls `.transform(...)` on new data.
        self.is_fitted_ = True
        return self

    def transform(self, X, y=None):
        # Work on a copy so the original DataFrame stays unchanged.
        X_transformed = X.copy()
        # Your implementation goes here.
        _ = X_transformed["precipitation"]
        return X_transformed


class DateColumnTransformer(BaseEstimator, TransformerMixin):
    # Exercise goal: Convert `date` to pandas datetime format.
    # @TODO:
    # 1. Keep the `X.copy()` pattern so this transformer is pipeline-safe.
    # 2. Convert `date` with `pd.to_datetime(..., errors="coerce")`.
    # 3. Cast the converted values to `object` so ColumnTransformer can
    #    pass the column through together with numeric outputs later on.
    # 4. Assign the result back to `X_transformed["date"]`.
    # 5. Add `import pandas as pd` at the top of this file if it's not there yet.
    # Starter file: `02-feature-engineering-with-sklearn-pipelines/src/pipeline/custom_transformer_seattle.py`.
    # Reference solution: `02-feature-engineering-with-sklearn-pipelines/src/pipeline/custom_transformer_seattle_solution.py`.
    def fit(self, X, y=None):
        # No learned parameters are needed, but we still mark the estimator as fitted.
        self.is_fitted_ = True
        return self

    def transform(self, X, y=None):
        # Work on a copy so later debugging stays easier.
        X_transformed = X.copy()
        # Your implementation goes here.
        _ = X_transformed["date"]
        return X_transformed
