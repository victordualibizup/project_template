from sklearn.pipeline import Pipeline
from houses_regression import features
from houses_regression.config.core import config
from sklearn.ensemble import RandomForestRegressor

pipeline_list = [
    ("SelectFeatures", features.FilterFeaturesTransformer(
        config.model_config.selected_features_pipeline
    )),
    ("NewHouseStyle", features.NewHouseStyleTransformer(
        config.model_config.house_style
    )),
    ("median_missing_imputer", features.MedianInputerTransformer(
        config.model_config.lot_frontage
    )),
    ("mode_missing_imputer", features.ModeInputerTransformer(
        config.model_config.bsm_type_1
    )),
    ("StandardScaler", features.StandardScalerTransformer(
        config.model_config.numeric_features,
        config.model_config.scaled_features
        )
     ),
    ("OneHotEncoder_NewHouseStyle", features.OneHotEncoderTransformer(
        config.model_config.new_house_style
    )),
    ("OneHotEncoder_BsmtFinType1", features.OneHotEncoderTransformer(
        config.model_config.bsm_type_1
    )),
    ("DropVariables", features.DeleteFeaturesTransformer(
        config.model_config.to_drop_unused_features +
        config.model_config.numeric_features
    ))
]


preprocess_pipeline = Pipeline(pipeline_list)

model = RandomForestRegressor(
              n_estimators=config.model_config.n_estimators,
              random_state=config.model_config.random_state
              )
