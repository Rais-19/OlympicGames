import pickle
import pandas as pd
import numpy as np
from pathlib import Path
from schemas.athlete_prediction import AthleteInput, AthleteOutput

# Global variables
MODEL_PATH = Path(__file__).parent.parent / "models" / "athlete_medal_model.pkl"

# Load model and artifacts once
with open(MODEL_PATH, "rb") as f:
    artifacts = pickle.load(f)

ATHLETE_MODEL = artifacts["model"]
SCALER = artifacts["scaler"]
FEATURE_NAMES = artifacts["feature_names"]
NUMERIC_COLS = artifacts["numeric_cols"]

print("Athlete model loaded successfully")

COLUMN_RENAME_MAP = {
    "age": "Age",
    "height": "Height",
    "weight": "Weight",
    "bmi": "BMI",
    "years_since_first": "Years_since_first",
    "noc_athletes_this_year": "NOC_athletes_this_year",
    "prev_medals_noc": "Prev_medals_NOC"
}


def preprocess_athlete_input(data: AthleteInput) -> pd.DataFrame:
    input_dict = data.model_dump()
    df = pd.DataFrame([input_dict])

    # rename API fields to training feature names
    df = df.rename(columns=COLUMN_RENAME_MAP)

    # Check numeric columns
    missing_nums = [col for col in NUMERIC_COLS if col not in df.columns]
    if missing_nums:
        raise ValueError(f"Missing numeric columns in input: {missing_nums}")

    # Scale numeric columns
    df[NUMERIC_COLS] = SCALER.transform(df[NUMERIC_COLS])

    # One-hot encode categoricals
    categorical_cols = ["sex", "season", "sport", "age_group", "region"]
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    # Align with training features
    df = df.reindex(columns=FEATURE_NAMES, fill_value=0)

    return df


def predict_athlete(data: AthleteInput) -> AthleteOutput:
    """
    Main prediction function for athlete medal probability.
    """
    try:
        # Preprocess
        X = preprocess_athlete_input(data)

        # Predict
        probability = ATHLETE_MODEL.predict_proba(X)[0][1]  # probability of class 1 (medal)

        # Simple rule-based label & confidence
        if probability >= 0.70:
            label = "High chance"
            confidence = "High"
        elif probability >= 0.40:
            label = "Medium chance"
            confidence = "Medium"
        else:
            label = "Low chance"
            confidence = "Low"

        return AthleteOutput(
            probability=round(float(probability), 4),
            predicted_label=label,
            confidence=confidence,
            model_version="xgboost-athlete-2026"
        )

    except Exception as e:
        raise ValueError(f"Prediction failed: {str(e)}")