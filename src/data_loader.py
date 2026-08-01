"""
Loads the Bangladesh Gen Z travel dataset from CSV files.
"""
import os
import pandas as pd


class BDDataLoader:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.users_df = None
        self.destinations_df = None
        self.ratings_df = None

    def load_all(self):
        self.users_df = pd.read_csv(os.path.join(self.data_dir, "bd_users.csv"))
        self.destinations_df = pd.read_csv(os.path.join(self.data_dir, "bd_destinations.csv"))
        self.ratings_df = pd.read_csv(os.path.join(self.data_dir, "bd_ratings.csv"))
        self._clean()
        return self.users_df, self.destinations_df, self.ratings_df

    def _clean(self):
        self.ratings_df = self.ratings_df.drop_duplicates(
            subset=["user_id", "destination_id"], keep="last"
        )
        self.ratings_df["rating"] = pd.to_numeric(self.ratings_df["rating"], errors="coerce")
        self.ratings_df = self.ratings_df.dropna(subset=["rating"])

        for col in ["category", "budget_level", "best_season", "division"]:
            if col in self.destinations_df.columns:
                self.destinations_df[col] = self.destinations_df[col].fillna("unknown")

    def train_test_split(self, test_size=0.2, seed=42):
        shuffled = self.ratings_df.sample(frac=1, random_state=seed)
        cutoff = int(len(shuffled) * (1 - test_size))
        return shuffled.iloc[:cutoff], shuffled.iloc[cutoff:]


if __name__ == "__main__":
    loader = BDDataLoader(data_dir=os.path.join(os.path.dirname(__file__), "..", "data"))
    users, dests, ratings = loader.load_all()
    print("Users:", users.shape)
    print("Destinations:", dests.shape)
    print("Ratings:", ratings.shape)
    print(dests[["name", "division", "category"]].head())
