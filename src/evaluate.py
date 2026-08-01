"""Evaluation: RMSE, MAE, Precision@K, Recall@K, NDCG@K for the BD recommender."""
import os
import numpy as np
from data_loader import BDDataLoader
from recommender import CollaborativeFilter, HybridRecommender


def rmse_mae(cf_model, test_df):
    errors = np.array([cf_model.predict(r.user_id, r.destination_id) - r.rating for r in test_df.itertuples()])
    return np.sqrt(np.mean(errors ** 2)), np.mean(np.abs(errors))


def precision_recall_ndcg_at_k(hybrid_model, test_df, k=10, threshold=4):
    precisions, recalls, ndcgs = [], [], []
    for user_id in test_df["user_id"].unique():
        relevant = set(test_df[(test_df.user_id == user_id) & (test_df.rating >= threshold)]["destination_id"])
        if not relevant:
            continue
        recs = hybrid_model.recommend(user_id, top_n=k)
        rec_ids = recs["destination_id"].tolist()
        hits = len(set(rec_ids) & relevant)
        precisions.append(hits / k)
        recalls.append(hits / len(relevant))
        dcg = sum(1 / np.log2(i + 2) for i, d in enumerate(rec_ids) if d in relevant)
        idcg = sum(1 / np.log2(i + 2) for i in range(min(len(relevant), k)))
        ndcgs.append(dcg / idcg if idcg > 0 else 0.0)
    return np.mean(precisions), np.mean(recalls), np.mean(ndcgs)


if __name__ == "__main__":
    loader = BDDataLoader(data_dir=os.path.join(os.path.dirname(__file__), "..", "data"))
    users, dests, ratings = loader.load_all()
    train_df, test_df = loader.train_test_split(test_size=0.2)

    cf = CollaborativeFilter().fit(train_df)
    rmse, mae = rmse_mae(cf, test_df)
    print(f"RMSE: {rmse:.4f}  MAE: {mae:.4f}")

    hybrid = HybridRecommender().fit(users, dests, train_df)
    p, r, n = precision_recall_ndcg_at_k(hybrid, test_df, k=10)
    print(f"Precision@10: {p:.4f}  Recall@10: {r:.4f}  NDCG@10: {n:.4f}")
