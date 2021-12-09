import pandas as pd
from typing import Dict
from sklearn import metrics
from houses_regression import data_manager, pipeline
from houses_regression.config.core import config
from sklearn.model_selection import train_test_split


def generate_features(target: str) -> (pd.DataFrame, pd.Series):
    """
    Creates the features for model estimation.
    Parameters
    ----------
    target (str): The target variable for estimation.

    Returns
    -------

    """
    dataframe = data_manager.create_dataframe_from_s3(
        bucket=config.app_config.bucket_name,
        key=config.app_config.train_features_file_name
    )

    target_feature = dataframe[target]
    features = pipeline.preprocess_pipeline.fit_transform(dataframe)
    return features, target_feature


def train_model(features_dict: Dict) -> Dict:
    """
    Trains the model.

    Parameters
    ----------
    features_dict (Dict): A dict with the features set.

    Returns
    -------

    """
    model = pipeline.model
    X_train = features_dict[config.model_config.x_train]
    X_test = features_dict[config.model_config.x_test]
    y_train = features_dict[config.model_config.y_train]
    y_test = features_dict[config.model_config.y_test]

    model.fit(X_train, y_train)

    train_y_pred = model.predict(X_train)
    test_y_pred = model.predict(X_test)

    train_mae = metrics.mean_absolute_error(y_train, train_y_pred)
    test_mae = metrics.mean_absolute_error(y_test, test_y_pred)

    print("Train Mean Absolute Error    :", train_mae)
    print("Test Mean Absolute Error    :", test_mae)

    features_dict[config.model_config.model_key] = model
    features_dict[config.model_config.train_mae] = train_mae
    features_dict[config.model_config.test_mae] = test_mae

    return features_dict


def create_features_dict(train_features: pd.DataFrame, target_feature: pd.DataFrame) -> Dict:
    """
    Creates a dict to hold the data splits and later types of objects from the train step.

    Parameters
    ----------
    train_features (pd.DataFrame): The predictor variables.
    target (pd.DataFrame): The target variable.

    Returns
    -------

    """
    X = train_features
    y = target_feature

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=config.model_config.test_size,
        random_state=config.model_config.random_state
    )

    features_dict = {
        config.model_config.x_train: X_train,
        config.model_config.x_test: X_test,
        config.model_config.y_train: y_train,
        config.model_config.y_test: y_test
    }

    return features_dict
