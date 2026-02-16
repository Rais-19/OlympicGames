# Olympic Medal Prediction App & API 

**Live App** (Streamlit UI)  
➜ https://olympicgamesui.onrender.com   

**API Endpoint** (FastAPI backend)  
➜ https://olympicgamesfastapi.onrender.com

* OpenAPI docs: https://olympicgamesfastapi.onrender.com/docs
* Health check: https://olympicgamesfastapi.onrender.com/health

## Project Overview

A modern, beginner-friendly full-stack machine learning project that predicts:  
- Probability an athlete wins a medal in an Olympic event  
- Total number of medals a country might win in a given Olympic year  

Uses **XGBoost** models trained on the famous **120 Years of Olympic History** dataset (Kaggle).  
Includes a clean **FastAPI** backend for predictions + a beautiful **Streamlit** frontend for easy interaction.

## Features

- Accurate predictions using historical Olympic data  
- Athlete model: probability based on age, height, weight, sport, country, experience, etc.  
- Country model: medal forecast based on year, athletes sent, historical performance, host status  
- Clean REST API with **FastAPI** (interactive docs at /docs)  
- User-friendly web interface with **Streamlit** — tabs, forms, metrics, and embedded EDA visuals  
- Input validation (prevents invalid data)  
- Friendly explanations & visuals (probability gauge, medal range, historical insights)  
- Ready for deployment (Render-ready structure)

## Project Structure
 olympic-prediction-api/
├── app.py                    # FastAPI backend (main API routes)
├── requirements.txt
├── schemas/                  # Pydantic models for input/output validation
│   ├── athlete_prediction.py
│   └── country_prediction.py
├── services/                 # Model loading & prediction logic
│   ├── athlete_prediction_service.py
│   └── country_prediction_service.py
├── models/                   # Trained models
│   ├── athlete_medal_model.pkl
│   └── country_medal_model.pkl
├── frontend/
│   └── app.py                # Streamlit web frontend
├── assets/
│   └── eda/                  # Selected EDA images
└── README.md



## How It Works

### Data & Model Training (done in Colab notebooks)
- Source: [120 Years of Olympic History](https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results)  
- Cleaning: missing values, duplicates, imputations (median per sport/sex)  
- Feature engineering: BMI, age groups, experience, NOC historical medals, host advantage  
- Two models:  
  - Athlete: XGBoost Classifier (F1 ~0.48–0.50, AUC ~0.85)  
  - Country: XGBoost Regressor (MAE ~1.2, R² ~0.96)  
- Saved as pickle files with scaler & feature names

### Backend (FastAPI)
- Loads models once at startup  
- Exposes `/predict/athlete` and `/predict/country` endpoints  
- Validates input with Pydantic  
- Returns structured JSON results

### Frontend (Streamlit)
- Calls the API with user input  
- Shows friendly forms + instant results with metrics & visuals  
- Includes selected EDA insights (participation trends, sport stats, country rankings)

