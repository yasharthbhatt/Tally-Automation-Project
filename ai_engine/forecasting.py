"""
AI-powered demand forecasting and prediction models
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Tuple
from loguru import logger
from models.schemas import ForecastResult


class DemandForecaster:
    """Forecast product demand using ML"""

    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.trained = False

    def prepare_features(self, transactions_df: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for demand forecasting"""
        # Group by product and date
        daily_demand = transactions_df.groupby(['product_id', 'date'])['quantity'].sum().reset_index()

        # Add time-based features
        daily_demand['day_of_week'] = daily_demand['date'].dt.dayofweek
        daily_demand['month'] = daily_demand['date'].dt.month
        daily_demand['day_of_month'] = daily_demand['date'].dt.day
        daily_demand['week_of_year'] = daily_demand['date'].dt.isocalendar().week

        # Calculate rolling statistics (7-day and 30-day windows)
        daily_demand = daily_demand.sort_values('date')
        daily_demand['rolling_mean_7d'] = daily_demand.groupby('product_id')['quantity'].transform(
            lambda x: x.rolling(window=7, min_periods=1).mean()
        )
        daily_demand['rolling_mean_30d'] = daily_demand.groupby('product_id')['quantity'].transform(
            lambda x: x.rolling(window=30, min_periods=1).mean()
        )
        daily_demand['rolling_std_7d'] = daily_demand.groupby('product_id')['quantity'].transform(
            lambda x: x.rolling(window=7, min_periods=1).std()
        )

        return daily_demand

    def train(self, transactions_df: pd.DataFrame) -> None:
        """Train the forecasting model"""
        logger.info("Training demand forecasting model...")

        features_df = self.prepare_features(transactions_df)

        # Select features for training
        feature_cols = ['day_of_week', 'month', 'day_of_month', 'week_of_year',
                       'rolling_mean_7d', 'rolling_mean_30d', 'rolling_std_7d']

        X = features_df[feature_cols].fillna(0)
        y = features_df['quantity']

        # Scale features
        X_scaled = self.scaler.fit_transform(X)

        # Train model
        self.model.fit(X_scaled, y)
        self.trained = True

        logger.info("Model training complete")

    def forecast_demand(self, product_id: str, product_name: str,
                       current_stock: int, transactions_df: pd.DataFrame,
                       days_ahead: int = 30) -> ForecastResult:
        """Forecast demand for a specific product"""
        if not self.trained:
            raise ValueError("Model not trained. Call train() first.")

        # Filter transactions for this product
        product_transactions = transactions_df[transactions_df['product_id'] == product_id]

        if len(product_transactions) < 7:
            logger.warning(f"Insufficient data for product {product_id}")
            # Return simple average-based forecast
            avg_demand = product_transactions['quantity'].mean() if len(product_transactions) > 0 else 0
            predicted_demand = avg_demand * days_ahead

            return ForecastResult(
                product_id=product_id,
                product_name=product_name,
                current_stock=current_stock,
                forecast_period=f"{days_ahead}d",
                predicted_demand=predicted_demand,
                recommended_order_quantity=max(0, int(predicted_demand - current_stock)),
                confidence_interval=(predicted_demand * 0.7, predicted_demand * 1.3),
                risk_level=self._assess_risk(current_stock, predicted_demand)
            )

        # Prepare recent data for prediction
        features_df = self.prepare_features(product_transactions)
        recent_data = features_df.iloc[-1:]

        feature_cols = ['day_of_week', 'month', 'day_of_month', 'week_of_year',
                       'rolling_mean_7d', 'rolling_mean_30d', 'rolling_std_7d']

        X = recent_data[feature_cols].fillna(0)
        X_scaled = self.scaler.transform(X)

        # Predict daily demand and multiply by forecast period
        daily_prediction = self.model.predict(X_scaled)[0]
        predicted_demand = daily_prediction * days_ahead

        # Calculate confidence interval
        std = recent_data['rolling_std_7d'].values[0] if not pd.isna(recent_data['rolling_std_7d'].values[0]) else predicted_demand * 0.2
        confidence_interval = (
            max(0, predicted_demand - 1.96 * std),
            predicted_demand + 1.96 * std
        )

        # Recommend order quantity
        safety_stock = std * 2  # 2 standard deviations
        recommended_order = max(0, int(predicted_demand + safety_stock - current_stock))

        return ForecastResult(
            product_id=product_id,
            product_name=product_name,
            current_stock=current_stock,
            forecast_period=f"{days_ahead}d",
            predicted_demand=predicted_demand,
            recommended_order_quantity=recommended_order,
            confidence_interval=confidence_interval,
            risk_level=self._assess_risk(current_stock, predicted_demand)
        )

    def _assess_risk(self, current_stock: int, predicted_demand: float) -> str:
        """Assess stockout risk"""
        ratio = current_stock / max(predicted_demand, 1)

        if ratio >= 1.5:
            return "low"
        elif ratio >= 0.75:
            return "medium"
        else:
            return "high"
