from pydantic import BaseModel, Field
from typing import Optional


class AthleteInput(BaseModel):
    """
    Input schema for predicting if an athlete wins a medal.
    """
    age: float = Field(..., ge=10, le=80, description="Age of the athlete")
    height: float = Field(..., ge=120, le=250, description="Height in cm")
    weight: float = Field(..., ge=30, le=200, description="Weight in kg")
    bmi: float = Field(..., ge=10, le=60, description="Body Mass Index")
    years_since_first: int = Field(..., ge=0, description="Years since first Olympic participation")
    is_team_sport: int = Field(..., ge=0, le=1, description="1 if team sport, 0 otherwise")
    is_first_appearance: int = Field(..., ge=0, le=1, description="1 if first Olympic participation")
    noc_athletes_this_year: int = Field(..., ge=1, description="Number of athletes from the same NOC this year")
    prev_medals_noc: int = Field(..., ge=0, description="Cumulative medals of the NOC before this year")

    # Categorical fields – these will be one-hot encoded later
    sex: str = Field(..., pattern="^(M|F)$", description="Sex: 'M' or 'F'")
    season: str = Field(..., pattern="^(Summer|Winter)$", description="Season: 'Summer' or 'Winter'")
    sport: str = Field(..., min_length=1, description="Sport name")
    age_group: str = Field(..., description="Age group bin (e.g. '18-23', '24-28')")
    region: str = Field(..., min_length=1, description="Country/region name")


class AthleteOutput(BaseModel):
    """
    Response schema for athlete medal prediction.
    """
    probability: float = Field(..., ge=0, le=1, description="Probability of winning a medal (0.0 to 1.0)")
    predicted_label: str = Field(..., description="Simple text label (e.g. 'High chance', 'Medium chance', 'Low chance')")
    confidence: str = Field(..., description="Confidence level (Low / Medium / High)")
    model_version: str = Field(default="xgboost-athlete-2026", description="Model identifier")
