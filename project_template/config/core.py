from pathlib import Path

from pydantic import BaseModel
from strictyaml import YAML, load

import project_template

# Relative paths for directories inside your project.
# It's imperative you use this variables to access files. Never a hardcoded path.

PACKAGE_ROOT = Path(project_template.__file__).resolve().parent
ROOT = PACKAGE_ROOT.parent
ARTIFACTS_DIR = ROOT / "artifacts"
DATA_DIR = ARTIFACTS_DIR / "data"
RAW_DATASET_DIR = DATA_DIR / "raw"
PROCESSED_DATASET_DIR = DATA_DIR / "processed"
TRAINED_MODEL_DIR = ARTIFACTS_DIR / "trained_models"
PIPELINE_DIR = ARTIFACTS_DIR / "pipeline"
METRICS_DIR = ARTIFACTS_DIR / "metrics"
CONFIG_FILE_PATH = ROOT / "config.yml"


# TODO: Input here all configuration that isn't related with the model
# or experimentation. Such as files location, object names and etc.
class AppConfig(BaseModel):
    author: str
    squad: str
    pass


# TODO: Input here all configuration related with the model and experimentation.
# For example: target, variable names, hyperparameters configuration and etc.
class ModelConfig(BaseModel):
    target: str


# There is no need to change this object.
class Config(BaseModel):
    """Master config object."""

    app_config: AppConfig
    model_config: ModelConfig


# Here we read and parse the config.yml file.
# No need to alter anything from this point onwards


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
