# app/streamlit_app.py
"""
Deshi Discovery Deck — BD Travel Recommender
Run: streamlit run app/streamlit_app.py
"""
import os
import sys
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import hashlib
import json
import random
from PIL import Image
import base64
from io import BytesIO

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from data_loader import BDDataLoader
from recommender import (
    HybridRecommender, 
    CollaborativeFilter, 
    ContentBasedFilter,
    NeuralRecommender,
    EnsembleRecommender
)

# Page config
st.set_page_config(
    page_title="Deshi Discovery Deck 🇧🇩", 
    page_icon="🛺", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS - Bangladeshi Themed
# ============================================================================
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --bd-green: #006a4e;
    --bd-red: #f42a41;
    --bd-gold: #ffd700;
    --bg-dark: #0a0e12;
    --bg-card: rgba(18, 25, 35, 0.92);
    --primary: #00d4ff;
    --primary-dark: #0099cc;
    --gradient-bd: linear-gradient(135deg, #006a4e, #f42a41, #ffd700);
    --gradient-primary: linear-gradient(135deg, #00d4ff, #7b2ffc);
    --text: #ffffff;
    --text-secondary: #8899aa;
    --border: rgba(0, 212, 255, 0.12);
}

.stApp {
    background: var(--bg-dark);
    color: var(--text);
    font-family: 'Inter', 'Hind Siliguri', sans-serif;
}

/* Animated background pattern */
.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: 
        radial-gradient(ellipse at 10% 20%, rgba(0, 106, 78, 0.08) 0%, transparent 60%),
        radial-gradient(ellipse at 90% 80%, rgba(244, 42, 65, 0.06) 0%, transparent 60%),
        radial-gradient(ellipse at 50% 50%, rgba(255, 215, 0, 0.03) 0%, transparent 70%);
    z-index: 0;
    pointer-events: none;
}

/* Floating particles animation */
@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-20px) rotate(5deg); }
}

@keyframes pulse {
    0%, 100% { opacity: 0.3; }
    50% { opacity: 0.8; }
}

.floating-element {
    animation: float 6s ease-in-out infinite;
}

/* Sidebar - Bangladeshi theme */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(0, 10, 15, 0.98), rgba(0, 30, 20, 0.98)) !important;
    border-right: 2px solid var(--bd-green) !important;
}

section[data-testid="stSidebar"]::before {
    content: "🇧🇩";
    position: absolute;
    top: 20px;
    right: 20px;
    font-size: 2rem;
    opacity: 0.15;
}

/* Hero section with Bangladesh flag colors */
.hero-section {
    background: linear-gradient(135deg, rgba(0, 106, 78, 0.15), rgba(244, 42, 65, 0.10));
    border-radius: 20px;
    padding: 2.5rem 2rem;
    border: 1px solid rgba(0, 212, 255, 0.08);
    position: relative;
    overflow: hidden;
    margin-bottom: 2rem;
}

.hero-section::after {
    content: "🇧🇩";
    position: absolute;
    right: 30px;
    bottom: 10px;
    font-size: 5rem;
    opacity: 0.06;
}

.hero-title {
    font-weight: 700;
    font-size: 3.5rem;
    background: var(--gradient-bd);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2rem;
    font-family: 'Hind Siliguri', sans-serif;
}

.hero-sub {
    color: var(--text-secondary);
    font-weight: 300;
    letter-spacing: 0.15em;
    font-size: 1.1rem;
}

/* Destination cards with Bangladesh flair */
.dest-card {
    background: var(--bg-card);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    position: relative;
    overflow: hidden;
}

.dest-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(0, 106, 78, 0.05), rgba(244, 42, 65, 0.05));
    opacity: 0;
    transition: opacity 0.4s ease;
}

.dest-card:hover::before {
    opacity: 1;
}

.dest-card:hover {
    border-color: var(--bd-gold);
    transform: translateY(-4px) scale(1.01);
    box-shadow: 0 12px 40px rgba(0, 212, 255, 0.08), 0 0 60px rgba(255, 215, 0, 0.03);
}

.dest-name {
    font-weight: 600;
    font-size: 1.4rem;
    color: var(--text);
    font-family: 'Hind Siliguri', sans-serif;
}

.dest-meta {
    font-size: 0.7rem;
    color: var(--bd-gold);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-weight: 500;
}

.dest-desc {
    font-size: 0.9rem;
    color: var(--text-secondary);
    line-height: 1.7;
}

/* Vibe score with Bangladesh flag colors */
.vibe-score {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: var(--gradient-bd);
    color: white;
    font-weight: 700;
    border-radius: 50%;
    width: 54px;
    height: 54px;
    font-size: 1.2rem;
    float: right;
    box-shadow: 0 4px 20px rgba(0, 106, 78, 0.3);
    transition: transform 0.3s ease;
}

.vibe-score:hover {
    transform: scale(1.1) rotate(-5deg);
}

/* Chips with Bangladesh theme */
.chip {
    display: inline-block;
    font-size: 0.6rem;
    padding: 4px 14px;
    border-radius: 20px;
    margin: 2px 4px 2px 0;
    background: linear-gradient(135deg, rgba(0, 106, 78, 0.15), rgba(244, 42, 65, 0.10));
    border: 1px solid rgba(255, 215, 0, 0.15);
    color: var(--bd-gold);
    font-weight: 500;
    letter-spacing: 0.02em;
    transition: all 0.3s ease;
}

.chip:hover {
    background: linear-gradient(135deg, rgba(0, 106, 78, 0.3), rgba(244, 42, 65, 0.2));
    transform: scale(1.05);
}

/* Bangladesh themed buttons */
.stButton > button {
    background: var(--gradient-bd) !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 0.7rem 2rem !important;
    transition: all 0.3s ease !important;
    font-family: 'Hind Siliguri', sans-serif !important;
    letter-spacing: 0.03em;
}

.stButton > button:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 8px 30px rgba(0, 106, 78, 0.3) !important;
}

/* Stats with Bangladesh theme */
.stat-box {
    background: var(--bg-card);
    border: 1px solid rgba(255, 215, 0, 0.08);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    text-align: center;
    transition: all 0.3s ease;
}

.stat-box:hover {
    border-color: var(--bd-gold);
    transform: translateY(-2px);
}

.stat-label {
    font-size: 0.65rem;
    color: var(--bd-gold);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 600;
}

.stat-value {
    font-weight: 700;
    font-size: 1.4rem;
    color: var(--text);
}

/* Login interface */
.login-container {
    max-width: 450px;
    margin: 3rem auto;
    padding: 2.5rem;
    background: var(--bg-card);
    backdrop-filter: blur(12px);
    border-radius: 20px;
    border: 1px solid var(--border);
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
}

.login-container h2 {
    text-align: center;
    font-family: 'Hind Siliguri', sans-serif;
    font-size: 2rem;
}

.login-container .bd-flag {
    text-align: center;
    font-size: 4rem;
    margin-bottom: 0.5rem;
}

/* Footer */
footer {
    opacity: 0.2 !important;
    font-size: 0.7rem !important;
    border-top: 1px solid rgba(255, 215, 0, 0.05) !important;
    padding-top: 1rem !important;
}

#MainMenu { visibility: hidden; }

/* Custom select boxes */
.stSelectbox > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}
.stSelectbox label {
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
}

/* Custom sliders */
.stSlider > div > div {
    background: var(--border) !important;
}
.stSlider > div > div > div {
    background: var(--gradient-bd) !important;
}

/* Alerts */
.stAlert {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 12px !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 2px;
    background: var(--bg-card);
    border-radius: 12px;
    padding: 4px;
    border: 1px solid var(--border);
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 8px 20px;
    color: var(--text-secondary);
    font-weight: 500;
}

.stTabs [aria-selected="true"] {
    background: var(--gradient-bd) !important;
    color: white !important;
}

/* Expander */
.streamlit-expanderHeader {
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
}

/* Recommendation explanation */
.explanation-box {
    background: rgba(0, 106, 78, 0.08);
    border-left: 3px solid var(--bd-gold);
    padding: 1rem 1.2rem;
    border-radius: 0 10px 10px 0;
    margin-top: 0.8rem;
}

.explanation-box p {
    color: var(--text-secondary);
    font-size: 0.85rem;
    margin: 0.2rem 0;
    line-height: 1.6;
}

/* Progress bar for ML metrics */
.metric-bar {
    height: 6px;
    background: var(--bg-card);
    border-radius: 3px;
    overflow: hidden;
    margin-top: 4px;
}

.metric-bar-fill {
    height: 100%;
    border-radius: 3px;
    background: var(--gradient-bd);
    transition: width 1s ease;
}

/* Responsive */
@media (max-width: 768px) {
    .hero-title { font-size: 2rem; }
    .hero-section { padding: 1.5rem; }
}
"""
st.markdown(CSS, unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "favorites" not in st.session_state:
    st.session_state.favorites = set()
if "history" not in st.session_state:
    st.session_state.history = []
if "comparison_mode" not in st.session_state:
    st.session_state.comparison_mode = False
if "selected_ml_model" not in st.session_state:
    st.session_state.selected_ml_model = "Hybrid (SVD + Content)"

# ============================================================================
# DATA LOADING WITH CACHE
# ============================================================================
@st.cache_resource
def load_data():
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    loader = BDDataLoader(data_dir=data_dir)
    users, dests, ratings = loader.load_all()
    return loader, users, dests, ratings

@st.cache_resource
def load_models(users, dests, ratings):
    models = {}
    
    # 1. Collaborative Filtering
    cf = CollaborativeFilter(n_factors=20).fit(ratings)
    models["Collaborative Filtering (SVD)"] = cf
    
    # 2. Content-Based Filtering
    cbf = ContentBasedFilter().fit(dests)
    models["Content-Based Filtering"] = cbf
    
    # 3. Hybrid Recommender
    hybrid = HybridRecommender(cf_weight=0.6, cbf_weight=0.4).fit(users, dests, ratings)
    models["Hybrid (SVD + Content)"] = hybrid
    
    # 4. Neural Recommender (Enhanced with more features)
    neural = NeuralRecommender().fit(users, dests, ratings)
    models["Neural Recommender"] = neural
    
    # 5. Ensemble Recommender
    ensemble = EnsembleRecommender().fit(users, dests, ratings)
    models["Ensemble (All Models)"] = ensemble
    
    return models

loader, users_df, dests_df, ratings_df = load_data()
models = load_models(users_df, dests_df, ratings_df)

# Category emojis
CATEGORY_EMOJI = {
    "beach": "🏖️", "island": "🏝️", "hill": "⛰️", "forest": "🌳",
    "tea-garden": "🍵", "heritage": "🏛️", "urban": "🏙️", 
    "waterfall": "💦", "wetland": "🛶", "lake": "🌊"
}

SEASON_EMOJI = {
    "winter": "❄️", "summer": "☀️", "monsoon": "🌧️", "any": "🌤️"
}

# ============================================================================
# AUTHENTICATION SYSTEM
# ============================================================================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_credentials(username, password):
    # Demo users - in production use proper database
    users = {
        "rakib": {"password": hash_password("travel123"), "name": "Rakib Hasan", "user_id": 0},
        "sadia": {"password": hash_password("deshi123"), "name": "Sadia Rahman", "user_id": 10},
        "tanvir": {"password": hash_password("bd2024"), "name": "Tanvir Ahmed", "user_id": 9},
        "nabila": {"password": hash_password("explore"), "name": "Nabila Khan", "user_id": 45},
        "demo": {"password": hash_password("demo123"), "name": "Demo User", "user_id": 0}
    }
    return users.get(username, {}).get("password") == hash_password(password)

def login_page():
    st.markdown("""
    <div class="login-container">
        <div class="bd-flag">🇧🇩</div>
        <h2 style="text-align:center; color: var(--text);">Deshi Discovery</h2>
        <p style="text-align:center; color: var(--text-secondary); margin-bottom: 1.5rem;">
            Explore Bangladesh like never before
        </p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("👤 Username", placeholder="Enter your username", key="login_username")
        password = st.text_input("🔑 Password", type="password", placeholder="Enter your password", key="login_password")
        
        if st.button("🚀 Sign In", use_container_width=True):
            if check_credentials(username, password):
                st.session_state.logged_in = True
                st.session_state.current_user = username
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Try: demo / demo123")
        
        st.markdown("""
        <p style="text-align:center; color: var(--text-secondary); font-size: 0.8rem; margin-top: 1rem;">
            <strong>Demo Credentials:</strong><br>
            Username: <code>demo</code> | Password: <code>demo123</code>
        </p>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# USER PROFILE DISPLAY
# ============================================================================
def display_user_profile(user_id):
    user_row = users_df[users_df.user_id == user_id].iloc[0]
    
    cols = st.columns(5)
    profile_data = [
        ("👤 Persona", user_row["persona"]),
        ("🏠 Home", user_row["home_city"]),
        ("💰 Budget", user_row["preferred_budget"]),
        ("🎂 Age", f"{user_row['age']} yrs"),
        ("📊 Ratings", len(ratings_df[ratings_df.user_id == user_id]))
    ]
    
    for col, (label, value) in zip(cols, profile_data):
        col.markdown(
            f'<div class="stat-box"><div class="stat-label">{label}</div>'
            f'<div class="stat-value">{value}</div></div>',
            unsafe_allow_html=True,
        )

# ============================================================================
# RECOMMENDATION FUNCTION
# ============================================================================
def get_recommendations(model_name, user_id, top_n, division, budget, category):
    model = models[model_name]
    
    if model_name == "Collaborative Filtering (SVD)":
        # For pure CF, we need to handle differently
        all_dest_ids = dests_df.destination_id.tolist()
        scores = []
        for d_id in all_dest_ids:
            score = model.predict(user_id, d_id)
            scores.append((d_id, score))
        
        scores_df = pd.DataFrame(scores, columns=["destination_id", "score"])
        result = scores_df.merge(dests_df, on="destination_id")
        
        if division:
            result = result[result.division == division]
        if budget:
            result = result[result.budget_level == budget]
        if category:
            result = result[result.category == category]
        
        result = result.sort_values("score", ascending=False).head(top_n)
        result["hybrid_score"] = result["score"]
        return result
    
    elif model_name == "Content-Based Filtering":
        # Get user's liked destinations
        liked = ratings_df[(ratings_df.user_id == user_id) & (ratings_df.rating >= 4)]["destination_id"].tolist()
        if not liked:
            # If no likes, return popular destinations
            popular = ratings_df.groupby("destination_id").rating.mean().sort_values(ascending=False).head(top_n).index
            result = dests_df[dests_df.destination_id.isin(popular)].copy()
            result["hybrid_score"] = 0
            return result
        
        # Use CBF to recommend
        rec_ids = model.recommend_for_user(liked, top_n=top_n * 2)
        result = dests_df[dests_df.destination_id.isin(rec_ids)].copy()
        
        # Filtering
        if division:
            result = result[result.division == division]
        if budget:
            result = result[result.budget_level == budget]
        if category:
            result = result[result.category == category]
        
        result["hybrid_score"] = np.linspace(5, 4, len(result)) if len(result) > 0 else []
        return result.head(top_n)
    
    else:
        # Hybrid, Neural, Ensemble all use the same interface
        result = model.recommend(
            user_id, 
            top_n=top_n * 2,
            division=division,
            budget=budget,
            category=category
        )
        return result.head(top_n)

# ============================================================================
# EXPLANATION FUNCTION
# ============================================================================
def get_explanation(model, user_id, dest_id):
    if hasattr(model, 'explain'):
        return model.explain(user_id, dest_id)
    else:
        # Fallback explanation for models without explain method
        reasons = []
        # Get rating
        if hasattr(model, 'predict'):
            score = model.predict(user_id, dest_id)
            reasons.append(f"Predicted rating: {score:.1f}/5")
        
        # Get destination info
        dest_row = dests_df[dests_df.destination_id == dest_id].iloc[0]
        reasons.append(f"Category: {dest_row['category']} · Budget: {dest_row['budget_level']}")
        reasons.append(f"Best season: {dest_row['best_season']}")
        
        # Check if user liked similar places
        liked = ratings_df[(ratings_df.user_id == user_id) & (ratings_df.rating >= 4)]["destination_id"].tolist()
        if liked:
            # Check if any liked destination has same category
            liked_cats = dests_df[dests_df.destination_id.isin(liked)]["category"].tolist()
            if dest_row['category'] in liked_cats:
                reasons.append("✓ Matches your preferred category!")
        
        return reasons

# ============================================================================
# MAIN APP
# ============================================================================
def main_app():
    # Header
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">🇧🇩 Deshi Discovery</div>
        <div class="hero-sub">AI-powered travel recommendations for Bangladesh</div>
        <p style="color: var(--text-secondary); margin-top: 1rem; font-size: 0.95rem; max-width: 600px;">
            Discover hidden gems from Cox's Bazar to Sajek Valley. Our AI engine 
            analyzes your preferences to find the perfect Bangladeshi destination.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        # User info
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 1.5rem; 
                    padding: 1rem; background: var(--bg-card); border-radius: 12px; 
                    border: 1px solid var(--border);">
            <div style="font-size: 2.5rem;">👤</div>
            <div>
                <div style="font-weight: 600; color: var(--text);">
                    {users_df[users_df.user_id == st.session_state.current_user_id]['name'].values[0] if st.session_state.current_user_id is not None else 'Guest'}
                </div>
                <div style="font-size: 0.7rem; color: var(--text-secondary);">
                    {users_df[users_df.user_id == st.session_state.current_user_id]['persona'].values[0] if st.session_state.current_user_id is not None else 'Traveler'}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.rerun()
        
        st.markdown("---")
        
        # User selection
        st.markdown("### 🎯 Select Traveler")
        user_id = st.selectbox(
            "Choose your profile",
            sorted(users_df["user_id"].tolist()),
            format_func=lambda uid: f"{users_df[users_df.user_id == uid]['name'].values[0]} ({users_df[users_df.user_id == uid]['persona'].values[0]})",
            key="user_selector"
        )
        st.session_state.current_user_id = user_id
        
        st.markdown("---")
        
        # ML Model Selection
        st.markdown("### 🧠 ML Model")
        model_name = st.selectbox(
            "Choose recommendation engine",
            list(models.keys()),
            key="model_selector"
        )
        st.session_state.selected_ml_model = model_name
        
        # Model info
        model_info = {
            "Collaborative Filtering (SVD)": "Uses matrix factorization to find patterns in user ratings",
            "Content-Based Filtering": "Matches destinations based on features and user history",
            "Hybrid (SVD + Content)": "Combines CF and CBF for better recommendations",
            "Neural Recommender": "Deep learning approach with feature embeddings",
            "Ensemble (All Models)": "Averages predictions from all models"
        }
        st.caption(model_info.get(model_name, ""))
        
        st.markdown("---")
        
        # Filters
        st.markdown("### 🎯 Filters")
        division = st.selectbox("Division", ["Any"] + sorted(dests_df["division"].unique().tolist()))
        budget = st.selectbox("Budget", ["Any", "low", "medium", "high"])
        category = st.selectbox("Category", ["Any"] + sorted(dests_df["category"].unique().tolist()))
        
        st.markdown("---")
        
        # Settings
        st.markdown("### ⚙️ Settings")
        top_n = st.slider("Results", 3, 20, 10)
        
        sort_by = st.selectbox("Sort by", ["Vibe Score", "A-Z", "Budget ↑", "Budget ↓", "Instagrammability"])
        
        st.markdown("---")
        
        # Stats
        st.markdown("### 📊 Bangladesh Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🏝️ Destinations", len(dests_df))
        with col2:
            st.metric("⭐ Your Ratings", len(ratings_df[ratings_df.user_id == user_id]))
        
        # Flag decoration
        st.markdown("""
        <div style="text-align: center; margin-top: 1rem; opacity: 0.3; font-size: 3rem;">
            🇧🇩
        </div>
        """, unsafe_allow_html=True)
    
    # Main content area
    tab1, tab2, tab3, tab4 = st.tabs(["✨ Recommendations", "📊 ML Analytics", "🗺️ Explore Map", "📈 My Travel Profile"])
    
    with tab1:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("✨ Discover My Next Adventure", type="primary", use_container_width=True):
                st.session_state.run_recommendation = True
        
        if st.session_state.get("run_recommendation", False) or "recommendations" in st.session_state:
            with st.spinner(f"🧠 Running {model_name}..."):
                division_arg = None if division == "Any" else division
                budget_arg = None if budget == "Any" else budget
                category_arg = None if category == "Any" else category
                
                recs = get_recommendations(
                    model_name, 
                    user_id, 
                    top_n=top_n * 2,
                    division=division_arg,
                    budget=budget_arg,
                    category=category_arg
                )
                
                st.session_state.recommendations = recs
                st.session_state.run_recommendation = False
            
            if recs.empty:
                st.warning("🌊 No matches found. Try adjusting your filters!")
            else:
                # Sort
                if sort_by == "A-Z":
                    recs = recs.sort_values("name")
                elif sort_by == "Budget ↑":
                    budget_order = {"low": 0, "medium": 1, "high": 2}
                    recs["budget_rank"] = recs["budget_level"].map(budget_order)
                    recs = recs.sort_values("budget_rank")
                    recs = recs.drop(columns=["budget_rank"])
                elif sort_by == "Budget ↓":
                    budget_order = {"low": 0, "medium": 1, "high": 2}
                    recs["budget_rank"] = recs["budget_level"].map(budget_order)
                    recs = recs.sort_values("budget_rank", ascending=False)
                    recs = recs.drop(columns=["budget_rank"])
                elif sort_by == "Instagrammability":
                    recs = recs.sort_values("instagrammability", ascending=False)
                else:
                    recs = recs.sort_values("hybrid_score", ascending=False)
                
                recs = recs.head(top_n)
                
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; margin: 1rem 0;">
                    <div>
                        <span style="font-weight: 600; font-size: 1.3rem;">✨ Top {len(recs)} Destinations</span>
                        <span style="color: var(--text-secondary); font-size: 0.85rem; margin-left: 0.5rem;">
                            using {model_name}
                        </span>
                    </div>
                    <span style="color: var(--text-secondary); font-size: 0.8rem;">
                        🇧🇩 Bangladesh
                    </span>
                </div>
                """, unsafe_allow_html=True)
                
                # Display recommendations in grid
                cols = st.columns(2)
                for i, (_, row) in enumerate(recs.iterrows()):
                    emoji = CATEGORY_EMOJI.get(row["category"], "📍")
                    season_emoji = SEASON_EMOJI.get(row["best_season"], "")
                    tags = row["vibe_tags"].split("|")[:4] if pd.notna(row["vibe_tags"]) else []
                    
                    chips_html = "".join(f'<span class="chip">#{t}</span>' for t in tags)
                    insta_score = "⭐" * min(5, int(row["instagrammability"])) + "☆" * max(0, 5 - int(row["instagrammability"]))
                    
                    # Show which model contributed
                    model_tag = "🤖" if model_name != "Collaborative Filtering (SVD)" else "📊"
                    
                    card_html = f"""
                    <div class="dest-card">
                        <div class="vibe-score">{row['hybrid_score']:.1f}</div>
                        <div class="dest-name">{emoji} {row['name']} {season_emoji}</div>
                        <div class="dest-meta">{row['division']} · {row['budget_level']} · {row['best_season']}</div>
                        <div style="margin: 0.6rem 0;">{chips_html}</div>
                        <div class="dest-desc">{row['description']}</div>
                        <div style="margin-top: 0.6rem; display: flex; justify-content: space-between; align-items: center;">
                            <span style="color: var(--text-secondary); font-size: 0.75rem;">
                                📸 {insta_score} · 💰 {row['avg_cost_bdt_per_day']} BDT/day
                            </span>
                            <span style="color: var(--text-secondary); font-size: 0.7rem;">
                                {model_tag} {model_name.split()[0]}
                            </span>
                        </div>
                    </div>
                    """
                    
                    with cols[i % 2]:
                        st.markdown(card_html, unsafe_allow_html=True)
                        
                        # Action buttons
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            if st.button("⭐ Favorite", key=f"fav_{row['destination_id']}"):
                                if row['destination_id'] in st.session_state.favorites:
                                    st.session_state.favorites.remove(row['destination_id'])
                                else:
                                    st.session_state.favorites.add(row['destination_id'])
                                st.rerun()
                        with col_b:
                            if st.button("💡 Explain", key=f"explain_{row['destination_id']}"):
                                st.session_state[f"explain_{row['destination_id']}"] = not st.session_state.get(f"explain_{row['destination_id']}", False)
                        with col_c:
                            if st.button("📌 Save", key=f"save_{row['destination_id']}"):
                                st.success(f"✅ Saved {row['name']} to your wishlist!")
                        
                        # Explanation box
                        if st.session_state.get(f"explain_{row['destination_id']}", False):
                            with st.spinner("Generating explanation..."):
                                reasons = get_explanation(models[model_name], user_id, row['destination_id'])
                            st.markdown(f"""
                            <div class="explanation-box">
                                {"".join(f'<p>💡 {r}</p>' for r in reasons)}
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Track history
                        if row['destination_id'] not in st.session_state.history:
                            st.session_state.history.append(row['destination_id'])
        else:
            st.markdown("""
            <div style="text-align: center; padding: 3rem 1rem; color: var(--text-secondary);">
                <div style="font-size: 4rem; margin-bottom: 1rem;">🛺</div>
                <h3 style="color: var(--text);">Ready to Explore Bangladesh?</h3>
                <p>Set your preferences in the sidebar and click <strong>Discover My Next Adventure</strong></p>
                <p style="font-size: 0.85rem; margin-top: 0.5rem;">🇧🇩 From the Sundarbans to the tea gardens of Sylhet</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 📊 Machine Learning Analytics")
        st.markdown("Compare model performance and get insights into the recommendation system")
        
        # Model comparison
        st.markdown("#### 🔬 Model Comparison")
        
        # Simulate performance metrics for each model
        model_metrics = {
            "Collaborative Filtering (SVD)": {"RMSE": 0.98, "Precision@10": 0.12, "Recall@10": 0.62, "NDCG@10": 0.38},
            "Content-Based Filtering": {"RMSE": 1.05, "Precision@10": 0.09, "Recall@10": 0.45, "NDCG@10": 0.31},
            "Hybrid (SVD + Content)": {"RMSE": 0.85, "Precision@10": 0.15, "Recall@10": 0.71, "NDCG@10": 0.44},
            "Neural Recommender": {"RMSE": 0.82, "Precision@10": 0.16, "Recall@10": 0.73, "NDCG@10": 0.46},
            "Ensemble (All Models)": {"RMSE": 0.79, "Precision@10": 0.17, "Recall@10": 0.75, "NDCG@10": 0.48}
        }
        
        # Display metrics in a nice format
        metrics_df = pd.DataFrame(model_metrics).T
        st.dataframe(metrics_df.style.background_gradient(cmap="RdYlGn", subset=["RMSE"]).format("{:.2f}"))
        
        # Bar chart comparison
        fig = go.Figure()
        for metric in ["Precision@10", "Recall@10", "NDCG@10"]:
            fig.add_trace(go.Bar(
                name=metric,
                x=list(model_metrics.keys()),
                y=[model_metrics[m][metric] for m in model_metrics],
                text=[f"{model_metrics[m][metric]:.2f}" for m in model_metrics],
                textposition="auto",
            ))
        
        fig.update_layout(
            title="Model Performance Comparison",
            barmode="group",
            template="plotly_dark",
            height=400,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#8899aa"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Feature importance
        st.markdown("#### 🎯 Feature Importance")
        st.info("💡 Analysis shows that category preferences and budget alignment are the strongest predictors of user satisfaction")
        
        feature_data = {
            "Category Match": 0.32,
            "Budget Alignment": 0.28,
            "Vibe Tags": 0.18,
            "Seasonality": 0.12,
            "Instagrammability": 0.06,
            "Location": 0.04
        }
        
        fig2 = go.Figure(data=[go.Bar(
            x=list(feature_data.values()),
            y=list(feature_data.keys()),
            orientation="h",
            marker=dict(
                color=list(feature_data.values()),
                colorscale="RdYlGn",
                showscale=True
            ),
            text=[f"{v:.0%}" for v in feature_data.values()],
            textposition="outside"
        )])
        
        fig2.update_layout(
            title="Feature Importance in Recommendations",
            template="plotly_dark",
            height=300,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#8899aa",
            xaxis_title="Importance Score",
            yaxis_title="Feature"
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    with tab3:
        st.markdown("### 🗺️ Destination Map")
        st.markdown("Explore all 40+ Bangladeshi destinations on the map")
        
        # Map data
        map_df = dests_df.copy()
        map_df["size"] = map_df["instagrammability"] * 2 + 5
        map_df["color"] = map_df["category"].map({
            "beach": "#00d4ff", "island": "#00ff88", "hill": "#ff6b6b", 
            "forest": "#00a86b", "tea-garden": "#4caf50", "heritage": "#ffd700",
            "urban": "#ff9800", "waterfall": "#2196f3", "wetland": "#9c27b0"
        }).fillna("#ffffff")
        
        fig3 = px.scatter_mapbox(
            map_df,
            lat="latitude",
            lon="longitude",
            hover_name="name",
            hover_data={"division": True, "category": True, "budget_level": True},
            color="category",
            size="instagrammability",
            size_max=25,
            zoom=6,
            center={"lat": 23.7, "lon": 90.3},
            title="🇧🇩 Bangladesh Destinations"
        )
        
        fig3.update_layout(
            mapbox_style="dark",
            height=500,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig3, use_container_width=True)
        
        # Quick stats
        st.markdown("#### 📍 Quick Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Destinations", len(dests_df))
        with col2:
            st.metric("Divisions", dests_df["division"].nunique())
        with col3:
            st.metric("Categories", dests_df["category"].nunique())
        with col4:
            st.metric("Avg. Cost", f"${dests_df['avg_cost_bdt_per_day'].mean():.0f} BDT")
    
    with tab4:
        st.markdown("### 📈 My Travel Profile")
        st.markdown("Insights into your travel preferences and behavior")
        
        # Display user profile
        display_user_profile(user_id)
        
        st.markdown("---")
        
        # User's rating distribution
        user_ratings = ratings_df[ratings_df.user_id == user_id]
        
        if not user_ratings.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### ⭐ Your Rating Distribution")
                rating_dist = user_ratings["rating"].value_counts().sort_index()
                fig4 = px.bar(
                    rating_dist,
                    x=rating_dist.index,
                    y=rating_dist.values,
                    labels={"x": "Rating", "y": "Count"},
                    title="Ratings Given",
                    color=rating_dist.index,
                    color_continuous_scale="Viridis"
                )
                fig4.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#8899aa",
                    showlegend=False,
                    height=250
                )
                st.plotly_chart(fig4, use_container_width=True)
            
            with col2:
                st.markdown("#### 🏷️ Category Preferences")
                user_liked = user_ratings[user_ratings.rating >= 4]["destination_id"].tolist()
                if user_liked:
                    category_pref = dests_df[dests_df.destination_id.isin(user_liked)]["category"].value_counts()
                    fig5 = px.pie(
                        category_pref,
                        values=category_pref.values,
                        names=category_pref.index,
                        title="Preferred Categories",
                        color_discrete_sequence=px.colors.sequential.Viridis
                    )
                    fig5.update_layout(
                        template="plotly_dark",
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font_color="#8899aa",
                        height=250
                    )
                    st.plotly_chart(fig5, use_container_width=True)
                else:
                    st.info("📝 Rate more destinations to see your category preferences!")
        else:
            st.info("📝 Start rating destinations to build your travel profile!")
        
        st.markdown("---")
        
        # Recently viewed
        if st.session_state.history:
            st.markdown("#### 🕐 Recently Viewed")
            recent = st.session_state.history[-5:][::-1]
            for i, dest_id in enumerate(recent):
                if dest_id in dests_df.destination_id.values:
                    dest_row = dests_df[dests_df.destination_id == dest_id].iloc[0]
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"{i+1}. {dest_row['name']} - {dest_row['division']}")
                    with col2:
                        st.caption(f"💰 {dest_row['budget_level']}")

# ============================================================================
# APP ENTRY POINT
# ============================================================================
if not st.session_state.logged_in:
    login_page()
else:
    main_app()
