from pydantic import BaseModel, Field
from typing import Optional


class CountryInput(BaseModel):
    """
    Input schema for predicting total medals for a country in a given year.
    """
    year: int = Field(..., ge=1896, le=2070, description="Olympic year")
    season: str = Field(..., pattern="^(Summer|Winter)$", description="Season: 'Summer' or 'Winter'")
    region: str = Field(..., min_length=1, description="Country/region name")
    num_athletes: int = Field(..., ge=1, description="Number of athletes from this country")
    prev_medals_1: int = Field(..., ge=0, description="Medals won in previous Olympic edition")
    prev_medals_2: int = Field(..., ge=0, description="Medals won two editions ago")
    prev_athletes: int = Field(..., ge=0, description="Number of athletes in previous edition")
    avg_age: float = Field(..., ge=15, le=50, description="Average age of athletes")
    avg_bmi: float = Field(..., ge=15, le=35, description="Average BMI of athletes")
    is_host: int = Field(..., ge=0, le=1, description="1 if this country is hosting, 0 otherwise")
    medal_change_prev: int = Field(..., ge=-100, le=100, description="Change in medals from previous edition")


class CountryOutput(BaseModel):
    """
    Response schema for country medal prediction.
    """
    predicted_total_medals: float = Field(..., ge=0, description="Predicted number of total medals")
    predicted_range_low: int = Field(..., description="Lower bound of expected range (rounded)")
    predicted_range_high: int = Field(..., description="Upper bound of expected range (rounded)")
    model_version: str = Field(default="xgboost-country-2026", description="Model identifier")