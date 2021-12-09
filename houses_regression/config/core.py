import os
from pathlib import Path
from typing import List
from pydantic import BaseModel
from strictyaml import YAML, load

import houses_regression

# Relative paths for directories inside your project.
# It's imperative you use this variables to access files. Never a hardcoded path.

PACKAGE_ROOT = Path(houses_regression.__file__).resolve().parent
ROOT = PACKAGE_ROOT.parent
CONFIG_FILE_PATH = ROOT / "config.yml"
prefix = '/opt/ml/'
model_path = os.path.join(prefix, 'model')


class AppConfig(BaseModel):
    author: str
    squad: str
    bucket_name: str
    train_features_file_name: str
    train_features_save_name: str
    target_feature_save_name: str


class ModelConfig(BaseModel):
    model_name: str
    target: str
    selected_features: List
    selected_features_pipeline: List
    numeric_features: List
    scaled_features: List
    to_drop_unused_features: List
    house_style: str
    new_house_style: str
    one_story: str
    two_story: str
    other_house_style: str
    bsm_type_1: str
    lot_frontage: str
    left_merge: str
    test_size: float
    random_state: int
    n_estimators: int
    model_random_state: int
    x_train: str
    x_test: str
    y_train: str
    y_test: str
    model_key: str
    train_mae: str
    test_mae: str


class Config(BaseModel):
    """Master config object."""

    app_config: AppConfig
    model_config: ModelConfig


def find_config_file() -> Path:
    """
    Locate the configuration file.
    """
    if CONFIG_FILE_PATH.is_file():
        return CONFIG_FILE_PATH
    raise Exception(f"Config not found at {CONFIG_FILE_PATH!r}")


def fetch_config_from_yaml(cfg_path: Path = None) -> YAML:
    """
    Parse YAML containing the package configuration.
    """

    if not cfg_path:
        cfg_path = find_config_file()

    if cfg_path:
        with open(cfg_path, "r") as conf_file:
            parsed_config = load(conf_file.read())
            return parsed_config
    raise OSError(f"Did not find config file at path: {cfg_path}")


def create_and_validate_config(parsed_config: YAML = None) -> Config:
    """
    Run validation on config values.
    """
    if parsed_config is None:
        parsed_config = fetch_config_from_yaml()

    # specify the data attribute from the strictyaml YAML type.
    _config = Config(
        app_config=AppConfig(**parsed_config.data),
        model_config=ModelConfig(**parsed_config.data),
    )

    return _config


config = create_and_validate_config()
