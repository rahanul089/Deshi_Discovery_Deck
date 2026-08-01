"""
Hybrid recommender for the BD Gen Z travel dataset:
Collaborative Filtering (SVD) + Content-Based Filtering (TF-IDF on
description + vibe_tags) + context filters (division, budget, season).
"""
import os
import numpy as np
import pandas as pd
from scipy.sparse.linalg import svds
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from data_loader import BDDataLoader


class CollaborativeFilter:
    def __init__(self, n_factors=15):
        self.n_factors = n_factors
        self.user_ids = None
        self.item_ids = None
        self.user_means = None
        self.pred_matrix = None

    def fit(self, ratings_df):
        matrix = ratings_df.pivot_table(index="user_id", columns="destination_id", values="rating")
        self.user_ids = matrix.index.to_numpy()
        self.item_ids = matrix.columns.to_numpy()
        self.user_means = matrix.mean(axis=1)
        filled = matrix.sub(self.user_means, axis=0).fillna(0).to_numpy()

        k = max(1, min(self.n_factors, min(filled.shape) - 1))
        U, sigma, Vt = svds(filled, k=k)
        sigma = np.diag(sigma)
        reconstructed = np.dot(np.dot(U, sigma), Vt)
        self.pred_matrix = reconstructed + self.user_means.to_numpy().reshape(-1, 1)
        return self

    def predict(self, user_id, destination_id):
        if user_id not in self.user_ids or destination_id not in self.item_ids:
            return float(np.nanmean(self.pred_matrix))
        u_idx = np.where(self.user_ids == user_id)[0][0]
        i_idx = np.where(self.item_ids == destination_id)[0][0]
        return float(np.clip(self.pred_matrix[u_idx, i_idx], 1, 5))


class ContentBasedFilter:
    def fit(self, destinations_df):
        self.destinations_df = destinations_df.reset_index(drop=True)
        self.dest_index = {d: i for i, d in enumerate(self.destinations_df["destination_id"])}

        text = (self.destinations_df["description"].fillna("") + " " +
                self.destinations_df["vibe_tags"].fillna("").str.replace("|", " "))
        tfidf = TfidfVectorizer(stop_words="english", max_features=400)
        text_matrix = tfidf.fit_transform(text)

        cat_features = pd.get_dummies(self.destinations_df[["category", "budget_level", "division"]])
        combined = np.hstack([text_matrix.toarray(), cat_features.to_numpy()])
        self.similarity_matrix = cosine_similarity(combined)
        return self

    def similar_to(self, destination_id, top_n=10):
        if destination_id not in self.dest_index:
            return []
        idx = self.dest_index[destination_id]
        scores = sorted(enumerate(self.similarity_matrix[idx]), key=lambda x: x[1], reverse=True)
        return [self.destinations_df.iloc[i]["destination_id"] for i, s in scores if i != idx][:top_n]

    def recommend_for_user(self, liked_ids, exclude_ids=None, top_n=10):
        exclude_ids = exclude_ids or set()
        valid = [d for d in liked_ids if d in self.dest_index]
        if not valid:
            return []
        idxs = [self.dest_index[d] for d in valid]
        avg_scores = self.similarity_matrix[idxs].mean(axis=0)
        ranked = sorted(enumerate(avg_scores), key=lambda x: x[1], reverse=True)
        recs = []
        for i, _ in ranked:
            d_id = self.destinations_df.iloc[i]["destination_id"]
            if d_id not in exclude_ids and d_id not in valid:
                recs.append(d_id)
            if len(recs) >= top_n:
                break
        return recs


class HybridRecommender:
    def __init__(self, cf_weight=0.6, cbf_weight=0.4):
        self.cf_weight = cf_weight
        self.cbf_weight = cbf_weight
        self.cf = CollaborativeFilter()
        self.cbf = ContentBasedFilter()

    def fit(self, users_df, destinations_df, ratings_df):
        self.destinations_df = destinations_df
        self.ratings_df = ratings_df
        self.cf.fit(ratings_df)
        self.cbf.fit(destinations_df)
        return self

    def recommend(self, user_id, top_n=10, division=None, budget=None, category=None):
        rated = set(self.ratings_df[self.ratings_df.user_id == user_id]["destination_id"])
        liked = self.ratings_df[
            (self.ratings_df.user_id == user_id) & (self.ratings_df.rating >= 4)
        ]["destination_id"].tolist()

        all_ids = self.destinations_df["destination_id"].tolist()
        cf_scores = {d: self.cf.predict(user_id, d) for d in all_ids if d not in rated}

        if liked:
            cbf_ranked = self.cbf.recommend_for_user(liked, exclude_ids=rated, top_n=len(all_ids))
            max_rank = max(len(cbf_ranked), 1)
            cbf_scores = {d: (max_rank - i) / max_rank * 5 for i, d in enumerate(cbf_ranked)}
        else:
            cbf_scores = {}

        combined = {
            d: self.cf_weight * cf_scores.get(d, 3.0) + self.cbf_weight * cbf_scores.get(d, 3.0)
            for d in cf_scores
        }

        candidates = self.destinations_df[self.destinations_df["destination_id"].isin(combined.keys())].copy()
        if division:
            candidates = candidates[candidates["division"] == division]
        if budget:
            candidates = candidates[candidates["budget_level"] == budget]
        if category:
            candidates = candidates[candidates["category"] == category]

        if candidates.empty:
            candidates = self.destinations_df[self.destinations_df["destination_id"].isin(combined.keys())].copy()

        candidates["hybrid_score"] = candidates["destination_id"].map(combined)
        candidates = candidates.sort_values("hybrid_score", ascending=False).head(top_n)
        return candidates

    def explain(self, user_id, destination_id):
        cf_score = self.cf.predict(user_id, destination_id)
        row = self.destinations_df[self.destinations_df.destination_id == destination_id].iloc[0]
        liked = self.ratings_df[
            (self.ratings_df.user_id == user_id) & (self.ratings_df.rating >= 4)
        ]["destination_id"].tolist()
        similar_liked = [d for d in liked if destination_id in self.cbf.similar_to(d, top_n=15)]

        reasons = [f"Predicted vibe match: {cf_score:.1f}/5 based on people like you"]
        if similar_liked:
            names = self.destinations_df[self.destinations_df.destination_id.isin(similar_liked[:2])]["name"].tolist()
            reasons.append(f"Similar energy to places you rated high: {', '.join(names)}")
        reasons.append(f"{row['category'].title()} vibe · {row['budget_level']} budget · best in {row['best_season']}")
        return reasons


if __name__ == "__main__":
    loader = BDDataLoader(data_dir=os.path.join(os.path.dirname(__file__), "..", "data"))
    users, dests, ratings = loader.load_all()
    model = HybridRecommender().fit(users, dests, ratings)

    sample_user = ratings["user_id"].iloc[0]
    print(f"Top picks for user {sample_user}:\n")
    print(model.recommend(sample_user, top_n=5)[["name", "division", "category", "hybrid_score"]].to_string(index=False))
