"""
DESHI DISCOVERY DECK — a Gen Z coded travel recommender for Bangladesh.
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
# DESIGN SYSTEM — rickshaw-art x Gen Z internet culture
# ---------------------------------------------------------------------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;700;800&family=Space+Grotesk:wght@400;500;700&family=Space+Mono:wght@400;700&display=swap');

:root{
  --ink:#0D1B14;
  --panel:#132A1E;
  --red:#E4232B;
  --yellow:#FFC900;
  --green:#1C7A4D;
  --cream:#FFF3D6;
  --neon:#7CFFB2;
}

html, body, [class*="css"]  { font-family: 'Space Grotesk', sans-serif; }

.stApp {
  background:
    radial-gradient(circle at 15% 10%, rgba(228,35,43,0.15), transparent 35%),
    radial-gradient(circle at 85% 90%, rgba(124,255,178,0.10), transparent 40%),
    var(--ink);
  color: var(--cream);
}

/* Rickshaw-stripe divider */
.stripe-bar {
  height: 10px;
  border-radius: 6px;
  margin: 0.4rem 0 1.6rem 0;
  background: repeating-linear-gradient(
    45deg,
    var(--red) 0px, var(--red) 14px,
    var(--yellow) 14px, var(--yellow) 28px,
    var(--green) 28px, var(--green) 42px
  );
}

.hero-title {
  font-family: 'Baloo 2', sans-serif;
  font-weight: 800;
  font-size: 3.2rem;
  line-height: 1.05;
  color: var(--cream);
  margin-bottom: 0.2rem;
}
.hero-title span { color: var(--yellow); }
.hero-sub {
  font-size: 1.05rem;
  color: var(--neon);
  font-family: 'Space Mono', monospace;
  margin-bottom: 0.5rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
  background: var(--panel);
  border-right: 3px solid var(--yellow);
}
section[data-testid="stSidebar"] * { color: var(--cream) !important; }

/* Destination card */
.dest-card {
  background: linear-gradient(160deg, #14311F 0%, #0F2419 100%);
  border: 2px solid rgba(255,201,0,0.35);
  border-radius: 22px;
  padding: 1.3rem 1.4rem;
  margin-bottom: 1.1rem;
  position: relative;
  overflow: hidden;
}
.dest-card::before{
  content:"";
  position:absolute; top:0; left:0; right:0; height:6px;
  background: repeating-linear-gradient(90deg, var(--red) 0 10px, var(--yellow) 10px 20px, var(--green) 20px 30px);
}
.dest-name {
  font-family: 'Baloo 2', sans-serif;
  font-weight: 700;
  font-size: 1.5rem;
  color: var(--cream);
  margin-bottom: 0.1rem;
}
.dest-meta {
  font-family: 'Space Mono', monospace;
  font-size: 0.78rem;
  color: var(--neon);
  letter-spacing: 0.02em;
  margin-bottom: 0.6rem;
}
.vibe-score {
  display:inline-flex; align-items:center; justify-content:center;
  background: var(--yellow);
  color: var(--ink);
  font-family:'Baloo 2', sans-serif;
  font-weight:800;
  border-radius: 50%;
  width: 58px; height: 58px;
  font-size: 1.15rem;
  float:right;
  transform: rotate(-6deg);
  box-shadow: 0 4px 0 rgba(0,0,0,0.25);
  border: 3px solid var(--ink);
}
.chip {
  display:inline-block;
  font-family:'Space Mono', monospace;
  font-size:0.7rem;
  padding: 3px 10px;
  border-radius: 999px;
  margin: 2px 4px 2px 0;
  background: rgba(124,255,178,0.12);
  border: 1px solid var(--neon);
  color: var(--neon);
}
.chip-red { background: rgba(228,35,43,0.15); border-color: var(--red); color:#FF9098; }
.chip-yellow { background: rgba(255,201,0,0.15); border-color: var(--yellow); color: var(--yellow); }

.dest-desc { font-size: 0.92rem; color: rgba(255,243,214,0.85); line-height:1.45; }

/* Buttons */
.stButton>button {
  background: var(--red) !important;
  color: var(--cream) !important;
  font-family:'Baloo 2', sans-serif;
  font-weight:700;
  border-radius: 14px !important;
  border: none !important;
  padding: 0.6rem 1.4rem !important;
  box-shadow: 0 4px 0 #8f1216;
}
.stButton>button:hover { background:#c81e25 !important; transform: translateY(1px); box-shadow: 0 3px 0 #8f1216; }

/* Metric-like profile stat */
.stat-box {
  background: var(--panel);
  border: 1px solid rgba(255,201,0,0.3);
  border-radius: 14px;
  padding: 0.7rem 0.9rem;
  text-align:center;
}
.stat-label { font-family:'Space Mono', monospace; font-size:0.68rem; color: var(--neon); text-transform:uppercase; }
.stat-value { font-family:'Baloo 2', sans-serif; font-weight:700; font-size:1.15rem; color: var(--cream); }

footer, #MainMenu, header {visibility: hidden;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


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
# HERO
# ---------------------------------------------------------------------------
st.markdown(
    '<div class="hero-title">Deshi Discovery <span>Deck</span> 🛺</div>'
    '<div class="hero-sub">// find your next BD trip before it goes viral</div>',
    unsafe_allow_html=True,
)
st.markdown('<div class="stripe-bar"></div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🧢 pick your fit")
    user_id = st.selectbox("who's swiping?", sorted(users_df["user_id"].tolist()),
                            format_func=lambda uid: f"{users_df[users_df.user_id==uid]['name'].values[0]} · #{uid}")
    division = st.selectbox("division check", ["Any"] + sorted(dests_df["division"].unique().tolist()))
    budget = st.selectbox("budget bestie", ["Any", "low", "medium", "high"])
    category = st.selectbox("vibe category", ["Any"] + sorted(dests_df["category"].unique().tolist()))
    top_n = st.slider("how many spots", 3, 15, 6)
    go = st.button("run it 🔥", type="primary", use_container_width=True)

user_row = users_df[users_df.user_id == user_id].iloc[0]

c1, c2, c3, c4 = st.columns(4)
for col, label, val in zip(
    [c1, c2, c3, c4],
    ["persona", "home city", "usual budget", "age"],
    [user_row["persona"], user_row["home_city"], user_row["preferred_budget"], user_row["age"]],
):
    col.markdown(f'<div class="stat-box"><div class="stat-label">{label}</div><div class="stat-value">{val}</div></div>', unsafe_allow_html=True)

st.markdown('<div class="stripe-bar"></div>', unsafe_allow_html=True)

if go:
    division_arg = None if division == "Any" else division
    budget_arg = None if budget == "Any" else budget
    category_arg = None if category == "Any" else category

    with st.spinner("cooking your feed... 🍳"):
        recs = model.recommend(user_id, top_n=top_n, division=division_arg, budget=budget_arg, category=category_arg)

    if recs.empty:
        st.warning("no matches bestie 😭 try loosening a filter")
    else:
        st.markdown(f"### {len(recs)} spots that match your energy")
        cols = st.columns(2)
        for i, (_, row) in enumerate(recs.iterrows()):
            emoji = CATEGORY_EMOJI.get(row["category"], "📍")
            tags = row["vibe_tags"].split("|")
            chips_html = "".join(
                f'<span class="chip{" chip-red" if j==0 else (" chip-yellow" if j==1 else "")}">#{t}</span>'
                for j, t in enumerate(tags)
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
                if st.checkbox(f"why tho? 🤔", key=f"why_{row['destination_id']}"):
                    for reason in model.explain(user_id, row["destination_id"]):
                        st.markdown(f"- {reason}")
else:
    st.info("set your vibe in the sidebar and smash **run it 🔥**")

st.markdown('<div class="stripe-bar"></div>', unsafe_allow_html=True)
st.caption("data: 40 real BD destinations · synthetic Gen Z user personas & ratings for demo purposes · built with SVD + TF-IDF hybrid recommender")
