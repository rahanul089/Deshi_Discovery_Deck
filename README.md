# 🛺 Deshi Discovery Deck — BD Travel Recommender (Gen Z Edition)

A hybrid ML recommender for **40 real Bangladeshi destinations**, styled with a
rickshaw-art × Gen-Z internet aesthetic instead of a generic dashboard look.

---

## 1. Dataset (CSV, built from scratch for this project)

| File | Rows | Description |
|---|---|---|
| `data/bd_destinations.csv` | 40 | Real BD places — Cox's Bazar, Sajek Valley, Sundarbans, Sylhet tea gardens, Panam City, Ratargul Swamp Forest, etc. Fields: division, category, vibe tags, budget, best season, avg cost (BDT/day), instagrammability score, lat/lon, description |
| `data/bd_users.csv` | 120 | Synthetic Gen Z personas (age 18–27) with a travel "persona" (Beach Baddie, Cloud Chaser, Heritage Nerd, Jungle Junkie, Waterfall Hunter, Chai & Chill, Street Food Explorer, Off-Grid Wanderer) |
| `data/bd_ratings.csv` | 3000 | Simulated ratings biased toward each user's persona/budget, so the model has real signal to learn from |

Regenerate anytime: `python src/generate_bd_dataset.py`

> This is synthetic demo data (real destinations, invented people/ratings) — swap in real survey/booking data by keeping the same column names in `data/bd_*.csv`.

---

## 2. Project Structure
```
bd-travel-genz/
├── data/
│   ├── bd_destinations.csv
│   ├── bd_users.csv
│   └── bd_ratings.csv
├── src/
│   ├── generate_bd_dataset.py   # builds the 3 CSVs
│   ├── data_loader.py           # loads + cleans CSVs
│   ├── recommender.py           # SVD (CF) + TF-IDF (CBF) hybrid model
│   └── evaluate.py              # RMSE, MAE, Precision@K, Recall@K, NDCG@K
├── app/
│   └── streamlit_app.py         # Gen Z styled interactive UI
└── requirements.txt
```

---

## 3. Setup

```bash
cd bd-travel-genz
python3 -m venv venv && source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

# dataset already included — regenerate only if you want fresh random ratings
python src/generate_bd_dataset.py

python src/data_loader.py     # sanity check
python src/recommender.py     # sample recommendation
python src/evaluate.py        # RMSE / MAE / Precision@K / Recall@K / NDCG@K

streamlit run app/streamlit_app.py
```
Opens at `http://localhost:8501`.

---

## 4. The Aesthetic

- **Palette**: jungle-black background, flag red, rickshaw yellow, doel green, shapla cream, neon paan-green accent
- **Type**: Baloo 2 (rounded display) + Space Grotesk (body) + Space Mono (data chips)
- **Signature elements**: rickshaw-painting stripe dividers, sticker-style circular "vibe score" badges, hashtag-style vibe-tag chips
- Copy is written in Gen Z register ("who's swiping?", "run it 🔥", "why tho? 🤔") on purpose — change the strings in `streamlit_app.py` if you want a more neutral tone

---

## 5. How the Model Works

- **Collaborative Filtering**: SVD matrix factorization on the user × destination rating matrix
- **Content-Based Filtering**: TF-IDF over description + vibe tags, plus one-hot category/budget/division, cosine similarity
- **Hybrid**: weighted blend (default 60% CF / 40% CBF), then filtered by division/budget/category
- **Explainability**: `model.explain(user_id, destination_id)` — shown via the "why tho?" checkbox on each card

---

## 6. Extending
- Add more destinations to `DESTINATIONS` in `generate_bd_dataset.py` (structure is a plain list of tuples)
- Swap synthetic ratings for real survey data — just match the CSV column names
- Add photos: extend `bd_destinations.csv` with an `image_url` column and add `st.image()` to the card
- Deploy: `streamlit run` works as-is on Streamlit Community Cloud — push this folder to a GitHub repo and connect it
