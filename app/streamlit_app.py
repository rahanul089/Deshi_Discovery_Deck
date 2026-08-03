"""
Deshi Discovery Deck — BD Travel Recommender
Run: streamlit run app/streamlit_app.py
"""
import os
import sys
import streamlit as st
import pandas as pd
import random

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from data_loader import BDDataLoader
from recommender import HybridRecommender

st.set_page_config(page_title="Deshi Discovery Deck 🇧🇩", page_icon="🛺", layout="wide")

# ---------------------------------------------------------------------------
# COOL MINIMALIST THEME
# ---------------------------------------------------------------------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --bg: #0a0a0f;
    --bg-card: rgba(20, 20, 30, 0.85);
    --primary: #00d4ff;
    --primary-dark: #0099cc;
    --gradient: linear-gradient(135deg, #00d4ff, #7b2ffc);
    --text: #ffffff;
    --text-secondary: #8899aa;
    --border: rgba(0, 212, 255, 0.15);
}

.stApp {
    background: var(--bg);
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(ellipse at 20% 50%, rgba(0, 212, 255, 0.03) 0%, transparent 70%),
                radial-gradient(ellipse at 80% 20%, rgba(123, 47, 252, 0.03) 0%, transparent 70%);
    z-index: 0;
    pointer-events: none;
}

.stApp > div {
    position: relative;
    z-index: 1;
}

section[data-testid="stSidebar"] {
    background: rgba(10, 10, 15, 0.98) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * {
    color: var(--text) !important;
}

.hero-title {
    font-weight: 700;
    font-size: 3rem;
    background: var(--gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2rem;
}
.hero-sub {
    color: var(--text-secondary);
    font-weight: 300;
    letter-spacing: 0.1em;
}

.divider {
    border: none;
    height: 1px;
    background: var(--gradient);
    margin: 1.5rem 0;
    opacity: 0.3;
}

.dest-card {
    background: var(--bg-card);
    backdrop-filter: blur(10px);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}
.dest-card:hover {
    border-color: var(--primary);
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(0, 212, 255, 0.05);
}
.dest-name {
    font-weight: 600;
    font-size: 1.3rem;
    color: var(--text);
}
.dest-meta {
    font-size: 0.75rem;
    color: var(--primary);
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.dest-desc {
    font-size: 0.9rem;
    color: var(--text-secondary);
    line-height: 1.6;
}

.vibe-score {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: var(--gradient);
    color: white;
    font-weight: 700;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    font-size: 1.1rem;
    float: right;
}

.chip {
    display: inline-block;
    font-size: 0.65rem;
    padding: 3px 12px;
    border-radius: 20px;
    margin: 2px 4px 2px 0;
    background: rgba(0, 212, 255, 0.08);
    border: 1px solid rgba(0, 212, 255, 0.1);
    color: var(--primary);
}

.stButton > button {
    background: var(--gradient) !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    border: none !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.3s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 212, 255, 0.2) !important;
}

.stat-box {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.8rem;
    text-align: center;
}
.stat-label {
    font-size: 0.65rem;
    color: var(--primary);
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.stat-value {
    font-weight: 600;
    font-size: 1.1rem;
    color: var(--text);
}

footer, #MainMenu, header {
    display: none !important;
}

.stSelectbox > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}
.stSelectbox label {
    color: var(--text-secondary) !important;
}

.stSlider > div > div {
    background: var(--border) !important;
}
.stSlider > div > div > div {
    background: var(--primary) !important;
}

.stAlert {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# LOAD MODEL
# ---------------------------------------------------------------------------
@st.cache_resource
def load_model():
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    loader = BDDataLoader(data_dir=data_dir)
    users, dests, ratings = loader.load_all()
    model = HybridRecommender().fit(users, dests, ratings)
    return model, users, dests, ratings

CATEGORY_EMOJI = {
    "beach": "🏖️", "island": "🏝️", "hill": "⛰️", "forest": "🌳",
    "tea-garden": "🍵", "heritage": "🏛️", "urban": "🏙️", "waterfall": "💦", "wetland": "🛶",
}

SEASON_EMOJI = {
    "winter": "❄️",
    "summer": "☀️",
    "monsoon": "🌧️",
    "any": "🌤️"
}

model, users_df, dests_df, ratings_df = load_model()

# ---------------------------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------------------------
if "favorites" not in st.session_state:
    st.session_state.favorites = set()
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### Profile")
    user_id = st.selectbox(
        "Traveler",
        sorted(users_df["user_id"].tolist()),
        format_func=lambda uid: f"{users_df[users_df.user_id == uid]['name'].values[0]}"
    )
    
    st.markdown("---")
    st.markdown("### Filters")
    division = st.selectbox("Division", ["Any"] + sorted(dests_df["division"].unique().tolist()))
    budget = st.selectbox("Budget", ["Any", "low", "medium", "high"])
    category = st.selectbox("Category", ["Any"] + sorted(dests_df["category"].unique().tolist()))
    
    st.markdown("---")
    st.markdown("### Settings")
    top_n = st.slider("Results", 3, 15, 7)
    sort_by = st.selectbox("Sort", ["Vibe Score", "A-Z", "Budget ↑", "Budget ↓"])
    
    st.markdown("---")
    st.markdown("### Stats")
    st.metric("Destinations", len(dests_df))
    st.metric("Ratings", len(ratings_df[ratings_df.user_id == user_id]))

# ---------------------------------------------------------------------------
# HERO
# ---------------------------------------------------------------------------
st.markdown(
    '<div class="hero-title">Deshi Discovery</div>'
    '<div class="hero-sub">AI travel recommendations for Bangladesh</div>',
    unsafe_allow_html=True,
)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# DISCOVER BUTTON
# ---------------------------------------------------------------------------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    go = st.button("✨ Discover", type="primary", use_container_width=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# USER PROFILE
# ---------------------------------------------------------------------------
user_row = users_df[users_df.user_id == user_id].iloc[0]

cols = st.columns(4)
for col, label, val in zip(cols, ["Persona", "Home", "Budget", "Age"], 
                          [user_row["persona"], user_row["home_city"], 
                           user_row["preferred_budget"], user_row["age"]]):
    col.markdown(
        f'<div class="stat-box"><div class="stat-label">{label}</div><div class="stat-value">{val}</div></div>',
        unsafe_allow_html=True,
    )

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# RECOMMENDATIONS
# ---------------------------------------------------------------------------
if go:
    division_arg = None if division == "Any" else division
    budget_arg = None if budget == "Any" else budget
    category_arg = None if category == "Any" else category

    with st.spinner("Curating..."):
        recs = model.recommend(
            user_id,
            top_n=top_n * 2,
            division=division_arg,
            budget=budget_arg,
            category=category_arg
        )

    if recs.empty:
        st.warning("No matches found. Try different filters.")
    else:
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
        else:
            recs = recs.sort_values("hybrid_score", ascending=False)
        
        recs = recs.head(top_n)
        
        st.markdown(f"### Top {len(recs)} Picks")
        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        cols = st.columns(2)
        for i, (_, row) in enumerate(recs.iterrows()):
            emoji = CATEGORY_EMOJI.get(row["category"], "📍")
            season_emoji = SEASON_EMOJI.get(row["best_season"], "")
            tags = row["vibe_tags"].split("|")[:3]
            
            chips_html = "".join(f'<span class="chip">#{t}</span>' for t in tags)

            card_html = f"""
            <div class="dest-card">
                <div class="vibe-score">{row['hybrid_score']:.1f}</div>
                <div class="dest-name">{emoji} {row['name']} {season_emoji}</div>
                <div class="dest-meta">{row['division']} · {row['budget_level']} · {row['best_season']}</div>
                <div style="margin: 0.5rem 0;">{chips_html}</div>
                <div class="dest-desc">{row['description']}</div>
            </div>
            """
            with cols[i % 2]:
                st.markdown(card_html, unsafe_allow_html=True)
                
                ca, cb = st.columns(2)
                with ca:
                    if st.button("⭐ Favorite", key=f"fav_{row['destination_id']}"):
                        if row["destination_id"] in st.session_state.favorites:
                            st.session_state.favorites.remove(row["destination_id"])
                        else:
                            st.session_state.favorites.add(row["destination_id"])
                        st.rerun()
                with cb:
                    if st.button("ℹ️ Details", key=f"details_{row['destination_id']}"):
                        with st.expander("More Info"):
                            st.write(f"**Category:** {row['category']}")
                            st.write(f"**Budget:** {row['budget_level']}")
                            st.write(f"**Best Season:** {row['best_season']}")
                            st.write(f"**Cost:** {row['avg_cost_bdt_per_day']} BDT/day")
                            st.write(f"**Instagram:** {'⭐' * int(row['instagrammability'])}")

else:
    st.info("👈 Set preferences in the sidebar and click **Discover**")

# ---------------------------------------------------------------------------
# RANDOM PICK
# ---------------------------------------------------------------------------
st.markdown('<hr class="divider">', unsafe_allow_html=True)
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("### 🎲 Random Pick")
with col2:
    if st.button("🎲 Surprise", use_container_width=True):
        random_dest = dests_df.sample(1).iloc[0]
        st.success(f"Try **{random_dest['name']}** in {random_dest['division']}!")
        st.caption(random_dest['description'])

# ---------------------------------------------------------------------------
# RECENTLY VIEWED
# ---------------------------------------------------------------------------
if st.session_state.history:
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("### 🕐 Recent")
    recent_cols = st.columns(min(4, len(st.session_state.history)))
    for idx, dest_id in enumerate(list(st.session_state.history)[-4:]):
        if dest_id in dests_df.destination_id.values:
            dest_row = dests_df[dests_df.destination_id == dest_id].iloc[0]
            with recent_cols[idx % len(recent_cols)]:
                st.markdown(f"**{dest_row['name']}**")
                st.caption(f"{dest_row['division']} · {dest_row['budget_level']}")
