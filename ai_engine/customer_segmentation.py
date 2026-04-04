"""
Customer segmentation and analysis
"""
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from typing import Dict, List
from loguru import logger


class CustomerSegmentation:
    """Segment customers using RFM analysis and clustering"""

    def __init__(self, n_segments: int = 4):
        self.n_segments = n_segments
        self.model = KMeans(n_clusters=n_segments, random_state=42)
        self.scaler = StandardScaler()
        self.segment_labels = {
            0: "Champions",
            1: "Loyal Customers",
            2: "At Risk",
            3: "Lost Customers"
        }

    def calculate_rfm(self, transactions_df: pd.DataFrame,
                     customers_df: pd.DataFrame) -> pd.DataFrame:
        """Calculate RFM (Recency, Frequency, Monetary) metrics"""
        logger.info("Calculating RFM metrics...")

        # Get the most recent date in transactions
        max_date = transactions_df['date'].max()

        # Calculate RFM metrics
        rfm = transactions_df.groupby('customer_id').agg({
            'date': lambda x: (max_date - x.max()).days,  # Recency
            'transaction_id': 'count',  # Frequency
            'total_amount': 'sum'  # Monetary
        }).reset_index()

        rfm.columns = ['customer_id', 'recency', 'frequency', 'monetary']

        # Merge with customer data
        if customers_df is not None:
            rfm = rfm.merge(customers_df[['customer_id', 'name']], on='customer_id', how='left')

        return rfm

    def segment_customers(self, rfm_df: pd.DataFrame) -> pd.DataFrame:
        """Segment customers using K-means clustering"""
        logger.info("Segmenting customers...")

        # Prepare features for clustering
        features = rfm_df[['recency', 'frequency', 'monetary']].fillna(0)

        # Scale features
        features_scaled = self.scaler.fit_transform(features)

        # Perform clustering
        rfm_df['segment_id'] = self.model.fit_predict(features_scaled)

        # Assign meaningful labels based on RFM scores
        rfm_df['segment'] = rfm_df['segment_id'].map(self._assign_segment_labels(rfm_df))

        return rfm_df

    def _assign_segment_labels(self, rfm_df: pd.DataFrame) -> Dict[int, str]:
        """Assign meaningful labels to segments based on characteristics"""
        segment_profiles = {}

        for segment_id in range(self.n_segments):
            segment_data = rfm_df[rfm_df['segment_id'] == segment_id]

            avg_recency = segment_data['recency'].mean()
            avg_frequency = segment_data['frequency'].mean()
            avg_monetary = segment_data['monetary'].mean()

            # Determine label based on characteristics
            if avg_recency < 30 and avg_frequency > 5 and avg_monetary > rfm_df['monetary'].median():
                segment_profiles[segment_id] = "Champions"
            elif avg_recency < 60 and avg_frequency > 3:
                segment_profiles[segment_id] = "Loyal Customers"
            elif avg_recency < 90:
                segment_profiles[segment_id] = "Potential Loyalists"
            elif avg_recency < 180:
                segment_profiles[segment_id] = "At Risk"
            else:
                segment_profiles[segment_id] = "Lost Customers"

        return segment_profiles

    def get_segment_insights(self, rfm_df: pd.DataFrame) -> Dict[str, Dict]:
        """Generate insights for each segment"""
        insights = {}

        for segment in rfm_df['segment'].unique():
            segment_data = rfm_df[rfm_df['segment'] == segment]

            insights[segment] = {
                'customer_count': len(segment_data),
                'avg_recency': segment_data['recency'].mean(),
                'avg_frequency': segment_data['frequency'].mean(),
                'avg_monetary': segment_data['monetary'].mean(),
                'total_revenue': segment_data['monetary'].sum(),
                'revenue_percentage': (segment_data['monetary'].sum() / rfm_df['monetary'].sum()) * 100
            }

        return insights
