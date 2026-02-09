from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas.athlete_prediction import AthleteInput, AthleteOutput
from schemas.country_prediction import CountryInput, CountryOutput
from services.athlete_prediction_service import predict_athlete
from services.country_prediction_service import predict_country

app = FastAPI(
    title="Olympic Prediction API",
    description="API for predicting athlete medal probability and country medal counts",
    version="1.0.0"
)

# Allow CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501", "*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/", tags=["Info"])
async def root():
    return {
        "message": "Welcome to the Olympic Prediction API"
    }
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Simple health endpoint to confirm the API is running.
    """
    return {
        "status": "healthy",
        "models_loaded": True
    }


@app.post("/predict/athlete", response_model=AthleteOutput, tags=["Predictions"])
async def predict_athlete_endpoint(input_data: AthleteInput):
    """
    Predict the probability that an athlete wins a medal.
    """
    try:
        result = predict_athlete(input_data)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/predict/country", response_model=CountryOutput, tags=["Predictions"])
async def predict_country_endpoint(input_data: CountryInput):
    """
    Predict the total number of medals a country is expected to win.
    """
    try:
        result = predict_country(input_data)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


