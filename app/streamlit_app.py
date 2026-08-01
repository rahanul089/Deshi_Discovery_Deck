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
# BLUE THEME DESIGN SYSTEM
# ---------------------------------------------------------------------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;800;900&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-primary: #080E14;
    --bg-secondary: #0F1A24;
    --bg-card: rgba(15, 26, 36, 0.88);
    --blue-deep: #1A5276;
    --blue-primary: #2E86C1;
    --blue-light: #5DADE2;
    --blue-gradient: linear-gradient(135deg, #1A5276, #2E86C1, #5DADE2);
    --cyan: #48C9B0;
    --cyan-light: #76D7C4;
    --text-primary: #F0F4F8;
    --text-secondary: #B0C4DE;
    --text-muted: #7F8FA6;
    --border-blue: rgba(46, 134, 193, 0.3);
    --shadow-blue: 0 8px 32px rgba(46, 134, 193, 0.15);
}

.stApp {
    background: var(--bg-primary);
    color: var(--text-primary);
    font-family: 'Inter', sans-serif;
}

.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: 
        url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1600&q=80'),
        url('https://images.unsplash.com/photo-1585409677983-0f6c41ca9c3b?w=1600&q=80');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    opacity: 0.06;
    z-index: 0;
    pointer-events: none;
}

.stApp > div {
    position: relative;
    z-index: 1;
}

section[data-testid="stSidebar"] {
    background: rgba(8, 14, 20, 0.95) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid var(--border-blue);
}
section[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-weight: 900;
    font-size: 3.5rem;
    background: var(--blue-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2rem;
}
.hero-sub {
    font-family: 'Inter', sans-serif;
    font-size: 1.1rem;
    color: var(--text-secondary);
    font-weight: 300;
    letter-spacing: 0.05em;
}

.blue-divider {
    border: none;
    height: 2px;
    background: var(--blue-gradient);
    margin: 1.5rem 0;
    border-radius: 2px;
    opacity: 0.6;
}

.dest-card {
    background: var(--bg-card);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border-blue);
    border-radius: 20px;
    padding: 1.5rem;
    margin-bottom: 1.2rem;
    transition: all 0.4s ease;
    position: relative;
    overflow: hidden;
}
.dest-card:hover {
    transform: translateY(-4px);
    border-color: var(--blue-primary);
    box-shadow: var(--shadow-blue);
}
.dest-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: var(--blue-gradient);
}
.dest-name {
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    font-size: 1.4rem;
    color: var(--text-primary);
}
.dest-meta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: var(--blue-light);
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.dest-desc {
    font-size: 0.9rem;
    color: var(--text-secondary);
    line-height: 1.7;
    font-weight: 300;
}

.vibe-score {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: var(--blue-gradient);
    color: white;
    font-family: 'Playfair Display', serif;
    font-weight: 800;
    border-radius: 50%;
    width: 60px;
    height: 60px;
    font-size: 1.2rem;
    float: right;
    border: 2px solid var(--blue-primary);
    box-shadow: 0 4px 20px rgba(46, 134, 193, 0.3);
}

.chip {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    padding: 4px 14px;
    border-radius: 999px;
    margin: 2px 4px 2px 0;
    background: rgba(46, 134, 193, 0.1);
    border: 1px solid rgba(46, 134, 193, 0.2);
    color: var(--blue-light);
    letter-spacing: 0.04em;
}
.chip-cyan {
    background: rgba(72, 201, 176, 0.12);
    border-color: rgba(72, 201, 176, 0.25);
    color: var(--cyan-light);
}

.stButton > button {
    background: var(--blue-gradient) !important;
    color: white !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 0.7rem 2rem !important;
    transition: all 0.3s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(46, 134, 193, 0.3) !important;
}

.stat-box {
    background: var(--bg-card);
    backdrop-filter: blur(8px);
    border: 1px solid var(--border-blue);
    border-radius: 14px;
    padding: 0.8rem 1rem;
    text-align: center;
}
.stat-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    color: var(--blue-light);
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.stat-value {
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    font-size: 1.1rem;
    color: var(--text-primary);
}

footer, #MainMenu, header {
    visibility: hidden;
}

@media (max-width: 768px) {
    .hero-title {
        font-size: 2.2rem;
    }
    .dest-card {
        padding: 1.2rem;
    }
    .vibe-score {
        width: 48px;
        height: 48px;
        font-size: 1rem;
    }
}

.stSelectbox > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-blue) !important;
    border-radius: 10px !important;
}
.stSelectbox label {
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
}

.stSlider > div > div {
    background: var(--border-blue) !important;
}
.stSlider > div > div > div {
    background: var(--blue-primary) !important;
}

.stAlert {
    background: var(--bg-card) !important;
    backdrop-filter: blur(8px);
    border: 1px solid var(--border-blue) !important;
    color: var(--text-primary) !important;
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
# HERO SECTION
# ---------------------------------------------------------------------------
st.markdown(
    '<div class="hero-title">Deshi Discovery Deck</div>'
    '<div class="hero-sub">AI-powered travel recommendations for Bangladesh</div>',
    unsafe_allow_html=True,
)
st.markdown('<hr class="blue-divider">', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ✦ Your Profile")
    user_id = st.selectbox(
        "Select Traveler",
        sorted(users_df["user_id"].tolist()),
        format_func=lambda uid: f"{users_df[users_df.user_id == uid]['name'].values[0]} · #{uid}"
    )
    st.markdown("---")
    st.markdown("### ✦ Filter Destinations")
    division = st.selectbox("Division", ["Any"] + sorted(dests_df["division"].unique().tolist()))
    budget = st.selectbox("Budget Level", ["Any", "low", "medium", "high"])
    category = st.selectbox("Category", ["Any"] + sorted(dests_df["category"].unique().tolist()))
    st.markdown("---")
    st.markdown("### ✦ Settings")
    top_n = st.slider("Number of Recommendations", 3, 15, 7)
    sort_by = st.selectbox("Sort By", ["Vibe Score", "Alphabetical", "Budget (Low to High)", "Budget (High to Low)"])
    st.markdown("---")
    st.markdown("### ✦ Quick Stats")
    st.metric("Total Destinations", len(dests_df))
    st.metric("Your Ratings", len(ratings_df[ratings_df.user_id == user_id]))
    
    if st.session_state.favorites:
        st.markdown("---")
        st.markdown("### ⭐ Favorites")
        for fav in list(st.session_state.favorites)[:3]:
            fav_name = dests_df[dests_df.destination_id == fav]["name"].values[0] if fav in dests_df.destination_id.values else f"#{fav}"
            st.markdown(f"- {fav_name}")

# ---------------------------------------------------------------------------
# DISCOVER BUTTON - MOVED TO TOP
# ---------------------------------------------------------------------------
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    go = st.button("✨ Discover", type="primary", use_container_width=True)

st.markdown('<hr class="blue-divider">', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# USER PROFILE
# ---------------------------------------------------------------------------
user_row = users_df[users_df.user_id == user_id].iloc[0]

col1, col2, col3, col4 = st.columns(4)
for col, label, val in zip(
    [col1, col2, col3, col4],
    ["Persona", "Home City", "Budget", "Age"],
    [user_row["persona"], user_row["home_city"], user_row["preferred_budget"], user_row["age"]],
):
    col.markdown(
        f'<div class="stat-box"><div class="stat-label">{label}</div><div class="stat-value">{val}</div></div>',
        unsafe_allow_html=True,
    )

st.markdown('<hr class="blue-divider">', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# RECOMMENDATIONS
# ---------------------------------------------------------------------------
if go:
    division_arg = None if division == "Any" else division
    budget_arg = None if budget == "Any" else budget
    category_arg = None if category == "Any" else category

    with st.spinner("Curating your perfect itinerary..."):
        recs = model.recommend(
            user_id,
            top_n=top_n * 2,
            division=division_arg,
            budget=budget_arg,
            category=category_arg
        )

    if recs.empty:
        st.warning("No destinations match your filters. Try adjusting your preferences.")
    else:
        if sort_by == "Alphabetical":
            recs = recs.sort_values("name")
        elif sort_by == "Budget (Low to High)":
            budget_order = {"low": 0, "medium": 1, "high": 2}
            recs["budget_rank"] = recs["budget_level"].map(budget_order)
            recs = recs.sort_values("budget_rank")
            recs = recs.drop(columns=["budget_rank"])
        elif sort_by == "Budget (High to Low)":
            budget_order = {"low": 0, "medium": 1, "high": 2}
            recs["budget_rank"] = recs["budget_level"].map(budget_order)
            recs = recs.sort_values("budget_rank", ascending=False)
            recs = recs.drop(columns=["budget_rank"])
        else:
            recs = recs.sort_values("hybrid_score", ascending=False)
        
        recs = recs.head(top_n)
        
        st.markdown(f"### ✦ Top {len(recs)} Recommendations")
        st.markdown('<hr class="blue-divider">', unsafe_allow_html=True)

        cols = st.columns(2)
        for i, (_, row) in enumerate(recs.iterrows()):
            emoji = CATEGORY_EMOJI.get(row["category"], "📍")
            season_emoji = SEASON_EMOJI.get(row["best_season"], "")
            tags = row["vibe_tags"].split("|")
            
            chips_html = "".join(
                f'<span class="chip{" chip-cyan" if j==0 else ""}">#{t}</span>'
                for j, t in enumerate(tags[:3])
            )

            is_fav = row["destination_id"] in st.session_state.favorites
            fav_icon = "⭐" if is_fav else "☆"

            card_html = f"""
            <div class="dest-card">
                <div class="vibe-score">{row['hybrid_score']:.1f}</div>
                <div class="dest-name">{emoji} {row['name']} {season_emoji}</div>
                <div class="dest-meta">{row['division'].upper()} · {row['budget_level'].upper()} BUDGET · BEST IN {row['best_season'].upper()}</div>
                <div style="margin-bottom:0.6rem;">{chips_html}</div>
                <div class="dest-desc">{row['description']}</div>
            </div>
            """
            with cols[i % 2]:
                st.markdown(card_html, unsafe_allow_html=True)
                
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    if st.button(f"{fav_icon} Favorite", key=f"fav_{row['destination_id']}"):
                        if row["destination_id"] in st.session_state.favorites:
                            st.session_state.favorites.remove(row["destination_id"])
                        else:
                            st.session_state.favorites.add(row["destination_id"])
                        st.rerun()
                with col_b:
                    if st.button("📍 Map", key=f"map_{row['destination_id']}"):
                        st.info(f"📍 {row['name']}: {row['latitude']}, {row['longitude']}")
                with col_c:
                    if st.button("📋 Details", key=f"details_{row['destination_id']}"):
                        with st.expander("📖 More Info", expanded=True):
                            st.markdown(f"**Category:** {row['category']}")
                            st.markdown(f"**Budget:** {row['budget_level']}")
                            st.markdown(f"**Best Season:** {row['best_season']}")
                            st.markdown(f"**Avg Cost:** {row['avg_cost_bdt_per_day']} BDT/day")
                            st.markdown(f"**Instagrammability:** {'⭐' * int(row['instagrammability'])}")
                
                if row["destination_id"] not in st.session_state.history:
                    st.session_state.history.append(row["destination_id"])

else:
    st.info(
        "👈 Set your preferences in the sidebar and click **Discover** to find your next adventure in Bangladesh."
    )

# ---------------------------------------------------------------------------
# FEELING LUCKY
# ---------------------------------------------------------------------------
st.markdown('<hr class="blue-divider">', unsafe_allow_html=True)
col_r1, col_r2 = st.columns([3, 1])
with col_r1:
    st.markdown("### 🎲 Feeling Lucky?")
with col_r2:
    if st.button("🎲 Surprise Me!", use_container_width=True):
        random_dest = dests_df.sample(1).iloc[0]
        st.success(f"✨ Check out **{random_dest['name']}** in {random_dest['division']}!")
        st.markdown(f"> {random_dest['description']}")

# ---------------------------------------------------------------------------
# RECENTLY VIEWED
# ---------------------------------------------------------------------------
if st.session_state.history:
    st.markdown('<hr class="blue-divider">', unsafe_allow_html=True)
    st.markdown("### 🕐 Recently Viewed")
    recent_cols = st.columns(min(4, len(st.session_state.history)))
    for idx, dest_id in enumerate(list(st.session_state.history)[-4:]):
        if dest_id in dests_df.destination_id.values:
            dest_row = dests_df[dests_df.destination_id == dest_id].iloc[0]
            with recent_cols[idx % len(recent_cols)]:
                st.markdown(f"**{dest_row['name']}**")
                st.caption(f"{dest_row['division']} · {dest_row['budget_level']}")
