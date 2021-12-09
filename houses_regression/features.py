import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler

from houses_regression.config.core import config


class NewHouseStyleTransformer(BaseEstimator, TransformerMixin):
    """
    Create the NewHouseStyle variable.
    """

    def __init__(self, feature_name: str):
        self.feature_name = feature_name

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        return self

    def transform(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        dataframe = dataframe.copy()
        dataframe["NewHouseStyle"] = np.where(
            (dataframe[self.feature_name] != config.model_config.one_story)
            & (dataframe[self.feature_name] != config.model_config.two_story),
            config.model_config.other_house_style,
            dataframe[self.feature_name],
        )
        return dataframe


class StandardScalerTransformer(BaseEstimator, TransformerMixin):
    """
    Create the Standard Scaler Transformer to apply data standarization.
    """

    def __init__(self, feature_list: list, column_names: list):
        self.feature_list = feature_list
        self.column_names = column_names

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        return self

    def transform(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        dataframe = dataframe.copy()
        transformed_dataframe = StandardScaler().fit_transform(
            dataframe[self.feature_list]
        )

        scaled_dataframe = pd.DataFrame(
            transformed_dataframe, columns=self.column_names
        )

        dataframe = dataframe.merge(
            scaled_dataframe,
            how=config.model_config.left_merge,
            left_index=True,
            right_index=True,
        )

        return dataframe


class OneHotEncoderTransformer(BaseEstimator, TransformerMixin):
    """
    Applies the one-hot-encoding on categorical variables.
    """

    def __init__(self, feature_name: str):
        self.feature_name = feature_name

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        return self

    def transform(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        dataframe = dataframe.copy()
        dummy_dataframe = pd.get_dummies(dataframe[self.feature_name])

        dataframe = pd.concat([dummy_dataframe, dataframe], axis=1)

        return dataframe


class DeleteFeaturesTransformer(BaseEstimator, TransformerMixin):
    """
    Drops unwanted variables.
    """

    def __init__(self, feature_list: list):
        self.feature_list = feature_list

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        return self

    def transform(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        dataframe = dataframe.copy()

        dataframe = dataframe.drop(self.feature_list, axis=1)

        return dataframe


class FilterFeaturesTransformer(BaseEstimator, TransformerMixin):
    """
    Filters dataframe variables.
    """

    def __init__(self, feature_list: list):
        self.feature_list = feature_list

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        return self

    def transform(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        dataframe = dataframe.copy()

        dataframe = dataframe[self.feature_list]

        return dataframe


class MedianInputerTransformer(BaseEstimator, TransformerMixin):
    """
    Fills missing values using the Median.
    """

    def __init__(self, feature_name: str):
        self.feature_name = feature_name

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        return self

    def transform(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        dataframe = dataframe.copy()
        dataframe[self.feature_name] = dataframe[self.feature_name].fillna(
            dataframe[self.feature_name].median()
        )

        return dataframe


class ModeInputerTransformer(BaseEstimator, TransformerMixin):
    """
    Fills missing values using the mode.
    """

    def __init__(self, feature_name: str):
        self.feature_name = feature_name

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        return self

    def transform(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        dataframe = dataframe.copy()
        dataframe[self.feature_name] = dataframe[self.feature_name].fillna(
            dataframe[self.feature_name].mode().values[0]
        )

        return dataframe
