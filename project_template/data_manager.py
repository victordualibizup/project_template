import pandas as pd
import joblib


def load_dataset(file_name: str) -> pd.DataFrame:
    """

    Parameters
    ----------
    file_name (str): File's name.

    Returns
    -------

    """
    file_path = "enter/your/path/{}.csv".format(file_name)
    dataframe = pd.read_csv(file_path)
    return dataframe


def load_model(file_name: str):
    """

    Parameters
    ----------
    file_name (str) The model's file name.

    Returns
    -------

    """

    file_path = "enter/your/path/{}.pkl".format(file_name)
    trained_model = joblib.load(filename=file_path)
    return trained_model


def save_model(file_name: str):
    """
    Saves the trained model in the specified path.
    Returns
    -------

    """
    save_path = "enter/your/path/{}.pkl".format(file_name)
    joblib.dump(file_name, save_path)
