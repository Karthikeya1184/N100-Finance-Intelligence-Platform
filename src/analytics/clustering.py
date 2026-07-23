from pathlib import Path
import sqlite3

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


class CompanyClustering:

    def __init__(self):

        self.project_root = Path(__file__).resolve().parents[2]

        self.db_path = self.project_root / "db" / "nifty100.db"

        self.output_dir = self.project_root / "output"
        self.report_dir = self.project_root / "reports"

        self.output_dir.mkdir(exist_ok=True)
        self.report_dir.mkdir(exist_ok=True)

        self.conn = sqlite3.connect(self.db_path)

        print("Database Connected Successfully")


    # ============================================================
    # Load Latest Financial Data
    # ============================================================

    def load_data(self):

        query = """
        SELECT
            c.id AS company_id,
            c.company_name,
            s.broad_sector,

            fr.return_on_equity_pct,
            fr.debt_to_equity,
            fr.revenue_cagr_5yr,
            fr.free_cash_flow_cr,
            fr.operating_profit_margin_pct

        FROM companies c

        LEFT JOIN sectors s
            ON c.id = s.company_id

        LEFT JOIN financial_ratios fr
            ON c.id = fr.company_id

        WHERE fr.year = (
            SELECT MAX(fr2.year)
            FROM financial_ratios fr2
            WHERE fr2.company_id = fr.company_id
        )

        ORDER BY c.company_name
        """

        df = pd.read_sql_query(query, self.conn)

        print(f"Loaded {len(df)} companies")

        return df


    # ============================================================
    # Impute Missing Values using Sector Median
    # ============================================================

    def impute_missing_values(self, df):

        features = [
            "return_on_equity_pct",
            "debt_to_equity",
            "revenue_cagr_5yr",
            "free_cash_flow_cr",
            "operating_profit_margin_pct",
        ]

        for feature in features:

            df[feature] = (
                df.groupby("broad_sector")[feature]
                .transform(lambda x: x.fillna(x.median()))
            )

        # Fill any remaining missing values (if an entire sector has NaNs)
        imputer = SimpleImputer(strategy="median")

        df[features] = imputer.fit_transform(df[features])

        print("Missing values imputed successfully")

        return df



    # ============================================================
    # Scale Features
    # ============================================================

    def scale_features(self, df):

        features = [
            "return_on_equity_pct",
            "debt_to_equity",
            "revenue_cagr_5yr",
            "free_cash_flow_cr",
            "operating_profit_margin_pct",
        ]

        X = df[features]

        scaler = StandardScaler()

        X_scaled = scaler.fit_transform(X)

        print("Features scaled successfully")

        return X_scaled, scaler



    # ============================================================
    # Train KMeans and Generate Elbow Plot
    # ============================================================

    def train_kmeans(self, X_scaled):

        inertias = []

        k_values = range(2, 11)

        for k in k_values:

            model = KMeans(
                n_clusters=k,
                random_state=42,
                n_init=10
            )

            model.fit(X_scaled)

            inertias.append(model.inertia_)

        plt.figure(figsize=(8, 5))
        plt.plot(k_values, inertias, marker="o")
        plt.xlabel("Number of Clusters (k)")
        plt.ylabel("Inertia")
        plt.title("Elbow Method")

        elbow_path = self.report_dir / "elbow_plot.png"

        plt.savefig(elbow_path, dpi=300, bbox_inches="tight")
        plt.close()

        print(f"Elbow plot saved to {elbow_path}")

        kmeans = KMeans(
            n_clusters=5,
            random_state=42,
            n_init=10
        )

        cluster_labels = kmeans.fit_predict(X_scaled)

        print("KMeans model trained successfully")

        return kmeans, cluster_labels



    # ============================================================
    # Generate Cluster Labels
    # ============================================================

    def generate_cluster_labels(self, df, X_scaled, kmeans, cluster_labels):

        cluster_names = {
            0: "Growth Leaders",
            1: "Value Builders",
            2: "Stable Performers",
            3: "High Debt Companies",
            4: "Emerging Businesses"
        }

        distances = kmeans.transform(X_scaled)

        df["cluster_id"] = cluster_labels

        df["cluster_name"] = df["cluster_id"].map(cluster_names)

        df["distance_from_centroid"] = [
            distances[i, cluster_labels[i]]
            for i in range(len(df))
        ]

        output = df[
            [
                "company_id",
                "cluster_id",
                "cluster_name",
                "distance_from_centroid",
            ]
        ]

        output_path = self.output_dir / "cluster_labels.csv"

        output.to_csv(output_path, index=False)

        print(f"Cluster labels saved to {output_path}")

        return output



    # ============================================================
    # Close Database Connection
    # ============================================================

    def close(self):

        self.conn.close()

        print("Database Connection Closed")



# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    app = CompanyClustering()

    df = app.load_data()

    df = app.impute_missing_values(df)

    X_scaled, scaler = app.scale_features(df)

    kmeans, cluster_labels = app.train_kmeans(X_scaled)

    app.generate_cluster_labels(
        df,
        X_scaled,
        kmeans,
        cluster_labels
    )

    app.close()