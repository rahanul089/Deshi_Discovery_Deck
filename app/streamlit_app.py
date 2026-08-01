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
# PROFESSIONAL DESIGN SYSTEM
# ---------------------------------------------------------------------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;700&display=swap');

:root {
    --primary: #1A3C34;
    --secondary: #E4232B;
    --accent: #FFC900;
    --success: #1C7A4D;
    --background: #0F1A16;
    --surface: #1A2F26;
    --text: #FFFFFF;
    --text-secondary: #B8D4C8;
    --border: #2A4A3A;
}

/* Main container */
.stApp {
    background: var(--background);
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--surface);
    border-right: 2px solid var(--accent);
    padding-top: 2rem;
}
section[data-testid="stSidebar"] * {
    color: var(--text) !important;
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stSlider label {
    color: var(--text-secondary) !important;
    font-weight: 500;
}

/* Headers */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
}

/* Hero Title */
.hero-title {
    font-family: 'Inter', sans-serif;
    font-weight: 800;
    font-size: 3rem;
    color: var(--text);
    margin-bottom: 0.2rem;
}
.hero-title span {
    color: var(--accent);
}
.hero-sub {
    font-size: 1.1rem;
    color: var(--text-secondary);
    font-weight: 400;
    margin-bottom: 0.5rem;
}

/* Divider Lines */
.professional-divider {
    border: none;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--secondary), var(--success));
    margin: 1.5rem 0;
    border-radius: 2px;
}

/* Destination Cards */
.dest-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
    position: relative;
}
.dest-card:hover {
    border-color: var(--accent);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.3);
}
.dest-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--secondary), var(--accent), var(--success));
    border-radius: 16px 16px 0 0;
}
.dest-name {
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: 1.4rem;
    color: var(--text);
    margin-bottom: 0.2rem;
}
.dest-meta {
    font-family: 'Inter', sans-serif;
    font-size: 0.8rem;
    color: var(--text-secondary);
    letter-spacing: 0.02em;
    margin-bottom: 0.6rem;
}
.dest-desc {
    font-size: 0.9rem;
    color: var(--text-secondary);
    line-height: 1.6;
}

/* Vibe Score Badge */
.vibe-score {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: var(--accent);
    color: var(--primary);
    font-family: 'Inter', sans-serif;
    font-weight: 800;
    border-radius: 50%;
    width: 56px;
    height: 56px;
    font-size: 1.1rem;
    float: right;
    border: 3px solid var(--primary);
}

/* Chips / Tags */
.chip {
    display: inline-block;
    font-family: 'Inter', sans-serif;
    font-size: 0.7rem;
    padding: 4px 12px;
    border-radius: 999px;
    margin: 2px 4px 2px 0;
    background: rgba(124, 255, 178, 0.1);
    border: 1px solid var(--success);
    color: var(--success);
}
.chip-red {
    background: rgba(228, 35, 43, 0.15);
    border-color: var(--secondary);
    color: #FF6B6B;
}
.chip-yellow {
    background: rgba(255, 201, 0, 0.15);
    border-color: var(--accent);
    color: var(--accent);
}

/* Buttons */
.stButton > button {
    background: var(--secondary) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 0.7rem 1.5rem !important;
    transition: all 0.3s ease !important;
}
.stButton > button:hover {
    background: #C41E24 !important;
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(228, 35, 43, 0.4);
}

/* Profile Stats */
.stat-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0.8rem 1rem;
    text-align: center;
}
.stat-label {
    font-family: 'Inter', sans-serif;
    font-size: 0.7rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.stat-value {
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: 1.1rem;
    color: var(--text);
}

/* Footer */
.footer {
    text-align: center;
    padding: 2rem 0 1rem 0;
    color: var(--text-secondary);
    font-size: 0.85rem;
    border-top: 1px solid var(--border);
    margin-top: 2rem;
}

/* Hide Streamlit branding */
footer, #MainMenu, header {
    visibility: hidden;
}

/* Responsive */
@media (max-width: 768px) {
    .hero-title {
        font-size: 2rem;
    }
    .dest-card {
        padding: 1rem;
    }
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
    '<div class="hero-title">Deshi Discovery <span>Deck</span> 🛺</div>'
    '<div class="hero-sub">Discover your next Bangladeshi adventure with AI-powered recommendations</div>',
    unsafe_allow_html=True,
)
st.markdown('<hr class="professional-divider">', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🎯 Your Profile")
    user_id = st.selectbox(
        "Select User",
        sorted(users_df["user_id"].tolist()),
        format_func=lambda uid: f"{users_df[users_df.user_id == uid]['name'].values[0]} · #{uid}"
    )
    st.markdown("---")
    st.markdown("### 🔍 Filter Destinations")
    division = st.selectbox("Division", ["Any"] + sorted(dests_df["division"].unique().tolist()))
    budget = st.selectbox("Budget Level", ["Any", "low", "medium", "high"])
    category = st.selectbox("Category", ["Any"] + sorted(dests_df["category"].unique().tolist()))
    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    top_n = st.slider("Number of Recommendations", 3, 15, 6)
    st.markdown("---")
    go = st.button("🚀 Get Recommendations", type="primary", use_container_width=True)

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

st.markdown('<hr class="professional-divider">', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# RECOMMENDATIONS
# ---------------------------------------------------------------------------
if go:
    division_arg = None if division == "Any" else division
    budget_arg = None if budget == "Any" else budget
    category_arg = None if category == "Any" else category

    with st.spinner("Finding the best destinations for you..."):
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
        st.markdown(f"### 🎯 Top {len(recs)} Recommendations for You")
        st.markdown("---")

        cols = st.columns(2)
        for i, (_, row) in enumerate(recs.iterrows()):
            emoji = CATEGORY_EMOJI.get(row["category"], "📍")
            tags = row["vibe_tags"].split("|")
            chips_html = "".join(
                f'<span class="chip{" chip-red" if j==0 else (" chip-yellow" if j==1 else "")}">#{t}</span>'
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
                if st.checkbox(f"💡 Why this recommendation?", key=f"why_{row['destination_id']}"):
                    with st.expander("📖 Explanation", expanded=True):
                        for reason in model.explain(user_id, row["destination_id"]):
                            st.markdown(f"• {reason}")

else:
    st.info(
        "👈 Set your preferences in the sidebar and click **Get Recommendations** to discover your next adventure in Bangladesh."
    )

# ---------------------------------------------------------------------------
# FOOTER
# ---------------------------------------------------------------------------
st.markdown('<hr class="professional-divider">', unsafe_allow_html=True)
st.markdown(
    """
    <div class="footer">
        🇧🇩 <strong>Deshi Discovery Deck</strong> — Powered by SVD + TF-IDF Hybrid Recommender<br>
        Data: 40 real Bangladesh destinations · 120 synthetic Gen Z user personas · 3,000 ratings
    </div>
    """,
    unsafe_allow_html=True,
)
