import pickle
import pandas as pd
import numpy as np
from pathlib import Path
from schemas.country_prediction import CountryInput, CountryOutput

# Global variables — loaded once
MODEL_PATH = Path(__file__).parent.parent / "models" / "country_medal_model.pkl"

with open(MODEL_PATH, "rb") as f:
    artifacts = pickle.load(f)

COUNTRY_MODEL = artifacts["model"]
SCALER = artifacts["scaler"]
FEATURE_NAMES = artifacts["feature_names"]
NUMERIC_COLS = artifacts["numeric_cols"]

print("Country model loaded successfully")


def preprocess_country_input(data: CountryInput) -> pd.DataFrame:
    """
    Convert input to DataFrame + apply preprocessing.
    """
    input_dict = data.model_dump()
    df = pd.DataFrame([input_dict])

    # Scale numeric columns
    if NUMERIC_COLS:
        df[NUMERIC_COLS] = SCALER.transform(df[NUMERIC_COLS])

    # One-hot encode categoricals (season, region)
    categorical_cols = [col for col in df.columns if col in ["season", "region"]]
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    # Align with training columns
    df = df.reindex(columns=FEATURE_NAMES, fill_value=0)

    return df


def predict_country(data: CountryInput) -> CountryOutput:
    """
    Main prediction function for country medal count.
    """
    try:
        X = preprocess_country_input(data)

        # Predict
        prediction = COUNTRY_MODEL.predict(X)[0]

        # Create simple confidence range 
        pred_rounded = round(prediction)
        margin = max(5, int(pred_rounded * 0.15))  
        low = max(0, pred_rounded - margin)
        high = pred_rounded + margin

        return CountryOutput(
            predicted_total_medals=round(float(prediction), 1),
            predicted_range_low=low,
            predicted_range_high=high,
            model_version="xgboost-country-2026"
        )

    except Exception as e:
        raise ValueError(f"Country prediction failed: {str(e)}")