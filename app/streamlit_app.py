"""
Deshi Discovery Deck — BD Travel Recommender
Run: streamlit run app/streamlit_app.py
"""
import os
import sys
import streamlit as st
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from data_loader import BDDataLoader
from recommender import HybridRecommender

st.set_page_config(page_title="Deshi Discovery Deck 🇧🇩", page_icon="🛺", layout="wide")

# ---------------------------------------------------------------------------
# AESTHETIC DESIGN SYSTEM
# ---------------------------------------------------------------------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;800;900&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-primary: #0A0F0D;
    --bg-secondary: #141E18;
    --bg-card: rgba(20, 30, 24, 0.85);
    --gold: #D4A847;
    --gold-light: #F0D080;
    --gold-gradient: linear-gradient(135deg, #D4A847, #F0D080, #D4A847);
    --teal: #2A9D8F;
    --teal-light: #5ECFB8;
    --rose: #E76F51;
    --rose-light: #F4A08A;
    --text-primary: #F5F0E8;
    --text-secondary: #C5BFA8;
    --text-muted: #8A8470;
    --border-gold: rgba(212, 168, 71, 0.3);
    --shadow-gold: 0 8px 32px rgba(212, 168, 71, 0.1);
}

/* Main container */
.stApp {
    background: var(--bg-primary);
    color: var(--text-primary);
    font-family: 'Inter', sans-serif;
}

/* Background Image Overlay */
.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: 
        url('https://images.unsplash.com/photo-1585409677983-0f6c41ca9c3b?w=1600&q=80'),
        url('https://images.unsplash.com/photo-1585409677983-0f6c41ca9c3b?w=1600&q=80');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    opacity: 0.08;
    z-index: 0;
    pointer-events: none;
}

/* Content overlay */
.stApp > div {
    position: relative;
    z-index: 1;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(10, 15, 13, 0.92) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid var(--border-gold);
}
section[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}

/* Hero Section */
.hero-title {
    font-family: 'Playfair Display', serif;
    font-weight: 900;
    font-size: 3.5rem;
    background: var(--gold-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2rem;
    text-shadow: none;
}
.hero-sub {
    font-family: 'Inter', sans-serif;
    font-size: 1.1rem;
    color: var(--text-secondary);
    font-weight: 300;
    letter-spacing: 0.05em;
    margin-bottom: 0.5rem;
}

/* Gold Divider */
.gold-divider {
    border: none;
    height: 2px;
    background: var(--gold-gradient);
    margin: 1.5rem 0;
    border-radius: 2px;
    opacity: 0.6;
}

/* Destination Cards */
.dest-card {
    background: var(--bg-card);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border-gold);
    border-radius: 20px;
    padding: 1.5rem;
    margin-bottom: 1.2rem;
    transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    position: relative;
    overflow: hidden;
}
.dest-card:hover {
    transform: translateY(-4px);
    border-color: var(--gold);
    box-shadow: var(--shadow-gold);
}
.dest-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: var(--gold-gradient);
}
.dest-name {
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    font-size: 1.5rem;
    color: var(--text-primary);
    margin-bottom: 0.2rem;
}
.dest-meta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: var(--gold);
    letter-spacing: 0.08em;
    margin-bottom: 0.6rem;
    text-transform: uppercase;
}
.dest-desc {
    font-size: 0.9rem;
    color: var(--text-secondary);
    line-height: 1.7;
    font-weight: 300;
}

/* Vibe Score */
.vibe-score {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: var(--gold-gradient);
    color: var(--bg-primary);
    font-family: 'Playfair Display', serif;
    font-weight: 800;
    border-radius: 50%;
    width: 60px;
    height: 60px;
    font-size: 1.2rem;
    float: right;
    border: 2px solid var(--gold);
    box-shadow: 0 4px 20px rgba(212, 168, 71, 0.3);
}

/* Chips / Tags */
.chip {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    padding: 4px 14px;
    border-radius: 999px;
    margin: 2px 4px 2px 0;
    background: rgba(212, 168, 71, 0.08);
    border: 1px solid rgba(212, 168, 71, 0.2);
    color: var(--gold-light);
    letter-spacing: 0.04em;
}
.chip-teal {
    background: rgba(42, 157, 143, 0.15);
    border-color: rgba(42, 157, 143, 0.3);
    color: var(--teal-light);
}
.chip-rose {
    background: rgba(231, 111, 81, 0.15);
    border-color: rgba(231, 111, 81, 0.3);
    color: var(--rose-light);
}

/* Buttons */
.stButton > button {
    background: var(--gold-gradient) !important;
    color: var(--bg-primary) !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 0.7rem 2rem !important;
    transition: all 0.3s ease !important;
    letter-spacing: 0.04em;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(212, 168, 71, 0.3) !important;
}

/* Profile Stats */
.stat-box {
    background: var(--bg-card);
    backdrop-filter: blur(8px);
    border: 1px solid var(--border-gold);
    border-radius: 14px;
    padding: 0.8rem 1rem;
    text-align: center;
}
.stat-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: var(--gold);
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.stat-value {
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    font-size: 1.15rem;
    color: var(--text-primary);
}

/* Footer */
.footer {
    text-align: center;
    padding: 2rem 0 1rem 0;
    color: var(--text-muted);
    font-size: 0.8rem;
    border-top: 1px solid var(--border-gold);
    margin-top: 2rem;
    font-weight: 300;
    letter-spacing: 0.04em;
}
.footer strong {
    color: var(--gold);
}

/* Hide Streamlit branding */
footer, #MainMenu, header {
    visibility: hidden;
}

/* Responsive */
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

/* Dropdowns and Selectors */
.stSelectbox > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-gold) !important;
    border-radius: 10px !important;
}
.stSelectbox label {
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
}

/* Slider */
.stSlider > div > div {
    background: var(--border-gold) !important;
}
.stSlider > div > div > div {
    background: var(--gold) !important;
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

model, users_df, dests_df, ratings_df = load_model()

# ---------------------------------------------------------------------------
# HERO SECTION
# ---------------------------------------------------------------------------
st.markdown(
    '<div class="hero-title">Deshi Discovery Deck</div>'
    '<div class="hero-sub">AI-powered travel recommendations for Bangladesh</div>',
    unsafe_allow_html=True,
)
st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

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
    top_n = st.slider("Number of Recommendations", 3, 15, 6)
    st.markdown("---")
    go = st.button("✨ Discover", type="primary", use_container_width=True)

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

st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

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
            top_n=top_n,
            division=division_arg,
            budget=budget_arg,
            category=category_arg
        )

    if recs.empty:
        st.warning("No destinations match your filters. Try adjusting your preferences.")
    else:
        st.markdown(f"### ✦ Top {len(recs)} Recommendations")
        st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

        cols = st.columns(2)
        for i, (_, row) in enumerate(recs.iterrows()):
            emoji = CATEGORY_EMOJI.get(row["category"], "📍")
            tags = row["vibe_tags"].split("|")
            chips_html = "".join(
                f'<span class="chip{" chip-teal" if j==0 else (" chip-rose" if j==1 else "")}">#{t}</span>'
                for j, t in enumerate(tags[:3])
            )

            card_html = f"""
            <div class="dest-card">
                <div class="vibe-score">{row['hybrid_score']:.1f}</div>
                <div class="dest-name">{emoji} {row['name']}</div>
                <div class="dest-meta">{row['division'].upper()} · {row['budget_level'].upper()} BUDGET · BEST IN {row['best_season'].upper()}</div>
                <div style="margin-bottom:0.6rem;">{chips_html}</div>
                <div class="dest-desc">{row['description']}</div>
            </div>
            """
            with cols[i % 2]:
                st.markdown(card_html, unsafe_allow_html=True)

else:
    st.info(
        "👈 Set your preferences in the sidebar and click **Discover** to find your next adventure in Bangladesh."
    )

# ---------------------------------------------------------------------------
# FOOTER
# ---------------------------------------------------------------------------
st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
st.markdown(
    """
    <div class="footer">
        <strong>Deshi Discovery Deck</strong> — Powered by SVD + TF-IDF Hybrid Recommender<br>
        40 real Bangladesh destinations · 120 Gen Z personas · 3,000 ratings
    </div>
    """,
    unsafe_allow_html=True,
)
