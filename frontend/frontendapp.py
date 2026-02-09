import streamlit as st
import requests
import json
from datetime import datetime



API_BASE_URL = "https://olympicgamesfastapi.onrender.com"   


EDA_IMAGES = {
    "medals_per_year": "assets/eda/medals_per_year.png",
    "athlete_distribution": "assets/eda/athlete_distribution_country_sport.png",
    "top10sports_average": "assets/eda/avg_age_height_weight_top10_sports.png",
    "top_countries": "assets/eda/top_10_countries_athletes.png",
    "top_sports_participation": "assets/eda/top_10_sports_participation.png",
    "top_countries_winrate": "assets/eda/top_countries_athletes_medals_winrate.png",
}


st.set_page_config(
    page_title="Olympic Prediction App",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a clean Olympic-style look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton > button { background-color: #1a73e8; color: white; border-radius: 8px; }
    .stButton > button:hover { background-color: #0d5bd9; }
    h1, h2, h3 { color: #1a3c6d; }
    .metric-box { background-color: #e3f2fd; padding: 16px; border-radius: 10px; text-align: center; }
    </style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.title("Olympic Prediction App")
    st.markdown("Predict medal chances for athletes or countries")
    
    current_year = datetime.now().year
    st.info(f"Current year: {current_year}")
    


# MAIN TABS
tab1, tab2, tab3 = st.tabs(["🏅 Athlete Medal Chance", "🌍 Country Medal Forecast", "📊 About & Insights"])

#tab 1:
with tab1:
    st.header("🏅 Athlete Medal Chance")
    st.markdown("Enter athlete details to predict the probability of winning a medal.")
    
    with st.form("athlete_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            age = st.number_input("Age", min_value=10, max_value=80, value=24, help="Athlete's age in years")
            height = st.number_input("Height (cm)", min_value=120, max_value=250, value=180)
            weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=75)
        
        with col2:
            sex = st.selectbox("Sex", options=["M", "F"], index=0)
            season = st.selectbox("Season", options=["Summer", "Winter"], index=0)
            sport = st.selectbox("Sport", options=[
                "Swimming", "Athletics", "Gymnastics", "Football", "Basketball",
                "Volleyball", "Rowing", "Weightlifting", "Judo", "Boxing", "Other"
            ])
        
        with col3:
            region = st.selectbox("Country", options=[
                "United States", "France", "China", "Germany", "Japan",
                "Italy", "Australia", "Great Britain", "Russia", "Other"
            ])
            years_since_first = st.number_input("Years since first participation", min_value=0, max_value=40, value=4)
            is_team = st.checkbox("Is team sport?", value=False)
            is_first = st.checkbox("First Olympic appearance?", value=False)
        
        submit_athlete = st.form_submit_button("Predict Medal Chance", type="primary", use_container_width=True)
    
    if submit_athlete:
        with st.spinner("Predicting..."):
            payload = {
                "age": float(age),
                "height": float(height),
                "weight": float(weight),
                "bmi": round(weight / ((height / 100) ** 2), 1),
                "years_since_first": int(years_since_first),
                "is_team_sport": 1 if is_team else 0,
                "is_first_appearance": 1 if is_first else 0,
                "noc_athletes_this_year": 500, 
                "prev_medals_noc": 100,        
                "sex": sex,
                "season": season,
                "sport": sport,
                "age_group": "24-28" if 24 <= age <= 28 else "Other", 
                "region": region
            }
            
            try:
                response = requests.post(f"{API_BASE_URL}/predict/athlete", json=payload, timeout=10)
                response.raise_for_status()
                result = response.json()
                
                st.success("Prediction complete!")
                #display:
                col_res1, col_res2 = st.columns([2, 3])
                with col_res1:
                    st.metric("Medal Probability", f"{result['probability']*100:.1f}%")
                    st.caption(f"Confidence: **{result['confidence']}**")
                
                with col_res2:
                    st.write(f"**{result['predicted_label']}**")
                
                # Show related EDA image (no width parameter)
                st.image(
                    EDA_IMAGES["top_sports_participation"],
                    caption="Top 10 sports by athlete participation"
                )
            
            except Exception as e:
                st.error(f"Error contacting API: {str(e)}")

#tab 2:
with tab2:
    st.header("🌍 Country Medal Forecast")
    st.markdown("Predict how many medals a country might win in a future Olympic year.")
    
    with st.form("country_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            year = st.number_input("Year", min_value=1896, max_value=2070, value=2028, step=4)
            season = st.selectbox("Season", options=["Summer", "Winter"], index=0)
            region = st.selectbox("Country", options=[
                "United States", "France", "China", "Germany", "Japan",
                "Italy", "Australia", "Great Britain", "Russia", "Other"
            ])
            num_athletes = st.number_input("Number of athletes", min_value=1, max_value=2000, value=420)
        
        with col2:
            prev_medals_1 = st.number_input("Medals in previous Games", min_value=0, value=45)
            prev_medals_2 = st.number_input("Medals two Games ago", min_value=0, value=38)
            avg_age = st.number_input("Average team age", min_value=15.0, max_value=50.0, value=26.8, step=0.1)
            is_host = st.checkbox("Country is hosting?", value=False)
        
        submit_country = st.form_submit_button("Predict Medal Count", type="primary", use_container_width=True)
    
    if submit_country:
        with st.spinner("Predicting..."):
            payload = {
                "year": int(year),
                "season": season,
                "region": region,
                "num_athletes": int(num_athletes),
                "prev_medals_1": int(prev_medals_1),
                "prev_medals_2": int(prev_medals_2),
                "prev_athletes": int(num_athletes * 0.98),  
                "avg_age": float(avg_age),
                "avg_bmi": 22.5,  
                "is_host": 1 if is_host else 0,
                "medal_change_prev": 5 
            }
            
            try:
                response = requests.post(f"{API_BASE_URL}/predict/country", json=payload, timeout=10)
                response.raise_for_status()
                result = response.json()
                
                st.success("Prediction complete!")
                
                #display 
                st.metric(
                    "Predicted Total Medals",
                    f"{result['predicted_total_medals']:.1f}",
                    delta=None,
                    help="Estimated medal haul"
                )
                
                st.write(f"**Expected range**: {result['predicted_range_low']} – {result['predicted_range_high']} medals")
                
                # Show related EDA image (no width parameter)
                st.image(
                    EDA_IMAGES["top_countries"],
                    caption="Top 10 countries by number of athletes"
                )
            
            except Exception as e:
                st.error(f"Error contacting API: {str(e)}")

# tab 3
with tab3:
    st.header("📊 About & EDA Insights")
    st.markdown("""
    This app uses two XGBoost models trained on the 120 Years of Olympic History dataset to predict:
    - Medal probability for individual athletes
    - Total medal counts for countries
    
    Models were trained on cleaned data with thoughtful feature engineering.
    """)
    
    st.subheader("Selected Insights from EDA")
    
    cols = st.columns(3)
    
    images_to_show = [
        ("medals_per_year", "Total medals awarded per Olympic year"),
        ("athlete_distribution", "Athlete distribution by country and sport"),
        ("top10sports_average", "Average age, height, and weight in top 10 sports"),
        ("top_countries", "Top 10 countries by number of athletes"),
        ("top_sports_participation", "Top 10 sports by athlete participation"),
        ("top_countries_winrate", "Top countries by athletes, medals, and win rate")
    ]
    
    for i, (key, caption) in enumerate(images_to_show):
        if key in EDA_IMAGES:
            with cols[i % 3]:
                st.image(
                    EDA_IMAGES[key],
                    caption=caption
                )
        else:
            with cols[i % 3]:
                st.warning(f"Image not found: {key}")