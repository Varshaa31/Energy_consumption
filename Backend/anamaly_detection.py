# app/models.py
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

class EnergyAnalyzer:
    def __init__(self, n_clusters=3, contamination=0.05):
        self.n_clusters = n_clusters
        self.contamination = contamination
        self.scaler = StandardScaler()
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        self.iso_forest = IsolationForest(contamination=contamination, random_state=42)

    def detect_patterns(self, df: pd.DataFrame):
        features = df[["hour_of_day", "energy_usage"]]
        df["cluster"] = self.kmeans.fit_predict(features)
        return df, df["cluster"].tolist()

    def detect_anomalies(self, df: pd.DataFrame):
        features = df[["hour_of_day", "energy_usage"]]
        df["anomaly_score"] = self.iso_forest.fit_predict(features)
        return df, df["anomaly_score"].tolist()

    def analyze(self, df: pd.DataFrame):
        """
        Analyze energy usage patterns and detect anomalies
        
        Args:
            df: DataFrame with columns ['hour_of_day', 'energy_usage']
        
        Returns:
            dict with analysis results including clusters and anomalies
        """
        # Scale the features
        scaled_data = self.scaler.fit_transform(df[["hour_of_day", "energy_usage"]])
        
        # Cluster the data points
        clusters = self.kmeans.fit_predict(scaled_data)
        
        # Simple anomaly detection (consider points far from cluster centers as anomalies)
        distances = self.kmeans.transform(scaled_data)
        min_distances = distances.min(axis=1)
        anomalies = np.where(min_distances > np.percentile(min_distances, 95), -1, 1)
        
        return {
            'clusters': clusters,
            'anomalies': anomalies,
            'data': df.assign(cluster=clusters, anomaly_score=anomalies).to_dict(orient="records")  # send full annotated data
        }
