import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler

from src.pipeline.custom_transformer_seattle_solution import (
    TempMinTransformer,
    WeatherColumnTransformer,
    FloatColumnTransformer,
    DateColumnTransformer,
)


class PreprocessingSeattleWeather:
    """Reusable preprocessing wrapper for Seattle weather exercises.

    Pass feature lists to `preprocess_fit_transform(...)`, for example:
    - numerical: `["precipitation", "temp_max", "temp_min", "wind"]`
    - categorical: `["weather"]`

    The class mirrors the notebook flow:
    1. clean raw Seattle weather columns with custom transformers
    2. impute/scale numeric features
    3. impute/encode categorical features
    """

    def __init__(self):
        self.numerical_features = []
        self.categorical_features = []
        # Clean raw columns before we hand them to the column-wise preprocessor.
        self.data_cleaning_pipeline = Pipeline(
            [
                ("temp_min", TempMinTransformer()),
                ("weather_strings", WeatherColumnTransformer()),
                ("precipitation_float", FloatColumnTransformer()),
                ("date_datetime", DateColumnTransformer()),
            ]
        )
        # Standard numeric branch for features that only need imputation + scaling.
        self.num_impute_scaling_pipeline = Pipeline(
            [
                ("imputer_num", SimpleImputer(strategy="median")),
                ("std_scaling", StandardScaler()),
            ]
        )
        # Special numeric branch for the final numeric feature, which the notebook
        # treats as `wind` and routes through a sqrt transform before scaling.
        self.num_impute_sqrt_scaling_pipeline = Pipeline(
            [
                ("imputer_num", SimpleImputer(strategy="median")),
                ("sqrt", FunctionTransformer(np.sqrt, validate=True)),
                ("std_scaling", StandardScaler()),
            ]
        )
        # Categorical branch: impute the mode, then one-hot encode labels.
        self.cat_pipeline = Pipeline(
            [
                ("imputer_cat", SimpleImputer(strategy="most_frequent")),
                (
                    "one_hot",
                    OneHotEncoder(
                        drop="first", handle_unknown="ignore", sparse_output=False
                    ),
                ),
            ]
        )
        self.preprocessor_pipe = self._build_preprocessor_pipeline()

    def _build_preprocessor_pipeline(self):
        # Split features into three branches:
        # - most numeric features
        # - the final numeric feature that gets sqrt + scaling
        # - categorical features
        preprocessor = ColumnTransformer(
            [
                (
                    "num_scaling_impute",
                    self.num_impute_scaling_pipeline,
                    self.numerical_features[:-1],
                ),
                (
                    "num_sqrt_scaling_impute",
                    self.num_impute_sqrt_scaling_pipeline,
                    self.numerical_features[-1:],
                ),
                ("cat", self.cat_pipeline, self.categorical_features),
            ],
            remainder="passthrough",
        )
        return Pipeline(
            [
                ("data_cleaning", self.data_cleaning_pipeline),
                ("preprocessor", preprocessor),
            ]
        )

    def preprocess_fit_transform(self, df, num_features, cat_features):
        """Fit the full preprocessing pipeline on `df` and return transformed data."""

        self.numerical_features = num_features
        self.categorical_features = cat_features
        self.preprocessor_pipe = self._build_preprocessor_pipeline()
        return self.preprocessor_pipe.fit_transform(df)

    def preprocess_transform(self, df):
        """Apply the already-fitted preprocessing pipeline to new data."""

        return self.preprocessor_pipe.transform(df)
