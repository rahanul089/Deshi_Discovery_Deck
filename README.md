# 🛺 Deshi Discovery Deck — BD Travel Recommender

A hybrid machine learning recommendation system for **40 real Bangladeshi destinations**, styled with a rickshaw-art × Gen-Z internet aesthetic.

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.60.0-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/rahanu1089/Deshi_Discovery_Deck.svg)](https://github.com/rahanu1089/Deshi_Discovery_Deck/stargazers)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Dataset](#-dataset)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Model Architecture](#-model-architecture)
- [Evaluation](#-evaluation)
- [Configuration](#-configuration)
- [Deployment](#-deployment)
- [Extending the Project](#-extending-the-project)
- [Troubleshooting](#-troubleshooting)

---

## 🎯 Overview

**Deshi Discovery Deck** is a hybrid travel recommendation engine built specifically for Bangladesh. It combines collaborative filtering and content-based filtering to suggest personalized destinations based on user preferences.

### Key Technologies

| Component | Technology |
|-----------|------------|
| **Collaborative Filtering** | Matrix factorization using Truncated SVD |
| **Content-Based Filtering** | TF-IDF vectorization with cosine similarity |
| **Hybrid Approach** | Weighted ensemble (60% CF + 40% CBF) with context-aware re-ranking |
| **Interactive UI** | Streamlit web application with explanation capabilities |
| **Data Processing** | Pandas, NumPy, Scikit-learn |

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **40 Real Destinations** | Cox's Bazar, Sajek Valley, Sundarbans, Sylhet tea gardens, Panam City, and more |
| **8 Gen Z Personas** | Beach Baddie, Cloud Chaser, Heritage Nerd, Jungle Junkie, Waterfall Hunter, Chai & Chill, Street Food Explorer, Off-Grid Wanderer |
| **Dual Recommendation Engine** | Combines collaborative and content-based filtering for improved accuracy |
| **Context Awareness** | Filters recommendations by division, budget, and category |
| **Explainability** | Provides "why this recommendation?" explanations for each suggestion |
| **Interactive Dashboard** | Rickshaw-art inspired Gen Z styled Streamlit interface |
| **Comprehensive Evaluation** | RMSE, MAE, Precision@K, Recall@K, and NDCG@K metrics |

---

## 📊 Dataset

### Overview

| File | Rows | Description |
|------|------|-------------|
| `bd_destinations.csv` | 40 | Real BD destinations with division, category, vibe tags, budget, season, cost, instagrammability, lat/lon, description |
| `bd_users.csv` | 120 | Synthetic Gen Z personas (age 18–27) with travel personas |
| `bd_ratings.csv` | 3000 | Simulated ratings biased toward each user's persona/budget |

### Destination Categories

- 🏖️ Beach
- 🏝️ Island
- ⛰️ Hill
- 🌳 Forest
- 🍵 Tea Garden
- 🏛️ Heritage
- 🏙️ Urban
- 💦 Waterfall
- 🛶 Wetland

### User Personas

| Persona | Preferred Categories |
|---------|---------------------|
| **Beach Baddie** | beach, island |
| **Cloud Chaser** | hill |
| **Heritage Nerd** | heritage |
| **Jungle Junkie** | forest, wetland |
| **Waterfall Hunter** | waterfall |
| **Chai & Chill** | tea-garden |
| **Street Food Explorer** | urban |
| **Off-Grid Wanderer** | island, wetland |

---

## 📁 Project Structure

```
bd-travel-genz/
├── app/
│   └── streamlit_app.py          # Gen Z styled interactive web interface
├── data/                         # CSV dataset files
│   ├── bd_destinations.csv       # 40 real Bangladesh destinations
│   ├── bd_users.csv              # 120 synthetic user profiles
│   └── bd_ratings.csv            # 3000 user ratings
├── src/
│   ├── generate_bd_dataset.py    # Fresh dataset generator
│   ├── data_loader.py            # Data loading & preprocessing
│   ├── recommender.py            # Hybrid SVD + TF-IDF model
│   └── evaluate.py               # Model evaluation metrics
├── requirements.txt
└── README.md
```

---

## 🚀 Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Step-by-Step Setup

```bash
# 1. Clone the repository
git clone https://github.com/rahanu1089/Deshi_Discovery_Deck.git
cd bd-travel-genz

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate          # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate fresh dataset (optional — dataset already included)
python src/generate_bd_dataset.py

# 5. Verify installation
python src/data_loader.py
```

---

## 💻 Usage

### Testing Individual Components

```bash
# Test data loader
python src/data_loader.py

# Test recommender
python src/recommender.py

# Run evaluation suite
python src/evaluate.py
```

### Launching the Web Application

```bash
streamlit run app/streamlit_app.py
```

The application will open at `http://localhost:8501` in your default browser.

### Using the Interface

1. Select a user from the sidebar dropdown
2. Apply optional filters: Division, Budget, Category
3. Adjust number of recommendations (3–15)
4. Click **"run it 🔥"**
5. View destination cards with:
   - Vibe score (circular badge)
   - Division, budget, best season
   - Hashtag-style vibe tags
   - Description
6. Click **"why tho? 🤔"** for explanation

---

## 🧠 Model Architecture

### Module Overview

| Module | Technique | Output |
|--------|-----------|--------|
| **Collaborative Filtering** | Truncated SVD on mean-centered user-item matrix | Predicted ratings for (user, destination) pairs |
| **Content-Based Filtering** | TF-IDF vectorization + cosine similarity | Destinations similar to user's historical preferences |
| **Hybrid Recommender** | Weighted ensemble (60% CF + 40% CBF) with context re-ranking | Top-N ranked destinations with explanations |
| **Evaluation** | 80/20 train-test split | RMSE, MAE, Precision@K, Recall@K, NDCG@K |

### Recommendation Pipeline

1. **Collaborative Filtering**: Learns latent factors from user-item interactions to predict ratings
2. **Content-Based Filtering**: Compares destination features (description, vibe tags, category, budget, division) using TF-IDF and cosine similarity
3. **Hybrid Ensemble**: Combines scores from both models using configurable weights
4. **Context Re-ranking**: Applies division, budget, and category filters to refine recommendations
5. **Explanation Generation**: Provides interpretable reasons for each recommendation

---

## 📈 Evaluation

### Metrics

| Metric | Description | Score |
|--------|-------------|-------|
| **RMSE** | Root Mean Square Error — Rating prediction accuracy | 0.9840 |
| **MAE** | Mean Absolute Error — Rating prediction accuracy | 0.7943 |
| **Precision@10** | Fraction of relevant items in top-10 recommendations | 0.1208 |
| **Recall@10** | Fraction of relevant items retrieved in top-10 recommendations | 0.6209 |
| **NDCG@10** | Normalized Discounted Cumulative Gain — Ranking quality | 0.3834 |

### Running Evaluation

```bash
python src/evaluate.py
```

---

## ⚙️ Configuration

### Tuning Parameters

| Parameter | Location | Default | Description |
|-----------|----------|---------|-------------|
| CF/CBF blend weights | `HybridRecommender(cf_weight=0.6, cbf_weight=0.4)` | 60/40 | Balance between collaborative and content-based filtering |
| SVD latent factors | `CollaborativeFilter(n_factors=15)` | 15 | Number of latent features in matrix factorization |
| Evaluation cutoff | `evaluate.py` → `k=10` | 10 | Number of recommendations for ranking metrics |
| Dataset size | `generate_bd_dataset.py` | 120 users, 40 destinations | Size of generated synthetic dataset |

---

## 🌐 Deployment

### Streamlit Community Cloud (Recommended)

1. Push your code to GitHub
2. Navigate to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub credentials
4. Click **"New app"** and select your repository
5. Set branch to `main` and main file to `app/streamlit_app.py`
6. Click **"Deploy"**

Your application will be live at: `https://deshi-discovery-deck.streamlit.app`

### Local Deployment

```bash
streamlit run app/streamlit_app.py --server.port 8501
```

---

## 🔧 Extending the Project

### Add More Destinations

Edit the `DESTINATIONS` list in `src/generate_bd_dataset.py`:

```python
DESTINATIONS = [
    # Add new destinations as tuples
    ("Destination Name", "Division", "category", "vibe-tags", "budget", "season", cost, insta_score, lat, lon, "description"),
]
```

### Add Images to Destinations

1. Extend `bd_destinations.csv` with an `image_url` column
2. Add `st.image()` to the card in `app/streamlit_app.py`

### Use Real Data

Replace synthetic ratings with real survey data by matching the CSV column names:
- `bd_users.csv`: user_id, name, age, home_city, persona, preferred_categories, preferred_budget
- `bd_ratings.csv`: user_id, destination_id, rating, visited_season

### Algorithm Enhancements

| Enhancement | Description |
|-------------|-------------|
| **Surprise Library** | Replace SVD with KNN, SVD++, or NMF algorithms |
| **Learning-to-Rank** | Combine CF + CBF scores as features in XGBoost/LightGBM |
| **Google Places API** | Add real-time photos, hours, and reviews |

---

## ❓ Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Ensure virtual environment is activated and run `pip install -r requirements.txt` |
| `streamlit: command not found` | Activate virtual environment: `source venv/bin/activate` (Windows: `venv\Scripts\activate`) |
| `FileNotFoundError: data/bd_*.csv` | Run `python src/generate_bd_dataset.py` |
| Port 8501 in use | Use `streamlit run app/streamlit_app.py --server.port 8502` |
| Blank Streamlit page | Run from project root: `cd /d/bd-travel-genz` |
| `sklearn` not found | Activate venv and install: `pip install scikit-learn` |
| `scipy` not found | Activate venv and install: `pip install scipy` |

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- Real Bangladesh destinations researched from travel blogs and guides
- Gen Z personas inspired by travel behavior patterns
- Streamlit for the interactive web framework
- Scikit-learn and SciPy communities for ML libraries

---

## 📬 Contact

**Maintainer**: Rahanul  
**GitHub**: [@rahanu1089](https://github.com/rahanul089)  
**Project Link**: [https://github.com/rahanu1089/Deshi_Discovery_Deck](https://github.com/rahanu1089/Deshi_Discovery_Deck)

---

## ⭐ Show Your Support

If you found this project helpful, please consider giving it a star on GitHub.

---

Made with ❤️ for exploring Bangladesh 🇧🇩 🛺
