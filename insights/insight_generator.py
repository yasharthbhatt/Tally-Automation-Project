"""
Generate actionable insights for traders
"""
import pandas as pd
from typing import List, Dict
from datetime import datetime, timedelta
from loguru import logger
from models.schemas import Insight, ForecastResult


class InsightGenerator:
    """Generate business insights from data and AI predictions"""

    def __init__(self, low_stock_threshold: int = 10):
        self.low_stock_threshold = low_stock_threshold
        self.insights: List[Insight] = []

    def generate_all_insights(self,
                             products_df: pd.DataFrame,
                             customers_df: pd.DataFrame,
                             transactions_df: pd.DataFrame,
                             forecasts: List[ForecastResult],
                             rfm_df: pd.DataFrame) -> List[Insight]:
        """Generate all types of insights"""
        logger.info("Generating insights...")

        self.insights = []

        # Stock alerts
        self.insights.extend(self._generate_stock_alerts(products_df, forecasts))

        # Customer insights
        self.insights.extend(self._generate_customer_insights(rfm_df))

        # Sales pattern insights
        self.insights.extend(self._generate_sales_patterns(transactions_df, products_df))

        # Product performance insights
        self.insights.extend(self._generate_product_insights(transactions_df, products_df))

        logger.info(f"Generated {len(self.insights)} insights")
        return self.insights

    def _generate_stock_alerts(self, products_df: pd.DataFrame,
                               forecasts: List[ForecastResult]) -> List[Insight]:
        """Generate stock-related alerts"""
        alerts = []

        # Critical low stock
        low_stock = products_df[products_df['current_stock'] < self.low_stock_threshold]
        for _, product in low_stock.iterrows():
            alerts.append(Insight(
                insight_type='alert',
                title=f"Critical: Low Stock for {product['name']}",
                description=f"Only {product['current_stock']} units remaining. Consider immediate reorder.",
                priority='critical',
                action_required=True,
                related_products=[product['product_id']],
                confidence_score=1.0
            ))

        # High-risk stockout predictions
        for forecast in forecasts:
            if forecast.risk_level == 'high':
                alerts.append(Insight(
                    insight_type='alert',
                    title=f"Stockout Risk: {forecast.product_name}",
                    description=f"Current stock ({forecast.current_stock} units) insufficient for predicted demand "
                              f"({forecast.predicted_demand:.0f} units). Recommend ordering {forecast.recommended_order_quantity} units.",
                    priority='high',
                    action_required=True,
                    related_products=[forecast.product_id],
                    confidence_score=0.85
                ))

        return alerts

    def _generate_customer_insights(self, rfm_df: pd.DataFrame) -> List[Insight]:
        """Generate customer-related insights"""
        insights = []

        # At-risk customers
        at_risk = rfm_df[rfm_df['segment'] == 'At Risk']
        if len(at_risk) > 0:
            customer_names = at_risk['name'].tolist()[:5] if 'name' in at_risk.columns else []
            insights.append(Insight(
                insight_type='recommendation',
                title=f"{len(at_risk)} Customers At Risk",
                description=f"These customers haven't purchased recently. Consider re-engagement campaigns. "
                          f"Top customers: {', '.join(customer_names[:3])}...",
                priority='medium',
                action_required=True,
                related_customers=at_risk['customer_id'].tolist(),
                confidence_score=0.75
            ))

        # Champions
        champions = rfm_df[rfm_df['segment'] == 'Champions']
        if len(champions) > 0:
            total_revenue = champions['monetary'].sum()
            insights.append(Insight(
                insight_type='pattern',
                title=f"{len(champions)} Champion Customers",
                description=f"Your top customers contribute ${total_revenue:,.2f} in revenue. "
                          f"Maintain strong relationships with loyalty programs.",
                priority='high',
                action_required=False,
                related_customers=champions['customer_id'].tolist(),
                confidence_score=0.90
            ))

        return insights

    def _generate_sales_patterns(self, transactions_df: pd.DataFrame,
                                 products_df: pd.DataFrame) -> List[Insight]:
        """Identify sales patterns and trends"""
        insights = []

        # Calculate weekly sales trends
        transactions_df['week'] = transactions_df['date'].dt.to_period('W')
        weekly_sales = transactions_df.groupby('week')['total_amount'].sum()

        if len(weekly_sales) >= 4:
            recent_4_weeks = weekly_sales.tail(4)
            trend = (recent_4_weeks.iloc[-1] - recent_4_weeks.iloc[0]) / recent_4_weeks.iloc[0] * 100

            if abs(trend) > 10:
                direction = "increased" if trend > 0 else "decreased"
                insights.append(Insight(
                    insight_type='pattern',
                    title=f"Sales {direction.capitalize()} by {abs(trend):.1f}%",
                    description=f"Weekly sales have {direction} by {abs(trend):.1f}% over the last 4 weeks. "
                              f"Current weekly revenue: ${recent_4_weeks.iloc[-1]:,.2f}",
                    priority='medium',
                    confidence_score=0.80
                ))

        # Best-selling products
        top_products = transactions_df.groupby('product_id').agg({
            'quantity': 'sum',
            'total_amount': 'sum'
        }).nlargest(5, 'total_amount')

        if len(top_products) > 0:
            product_names = [products_df[products_df['product_id'] == pid]['name'].values[0]
                           if len(products_df[products_df['product_id'] == pid]) > 0 else pid
                           for pid in top_products.index]

            insights.append(Insight(
                insight_type='pattern',
                title="Top 5 Revenue-Generating Products",
                description=f"Products: {', '.join(product_names[:3])}... "
                          f"Total revenue: ${top_products['total_amount'].sum():,.2f}",
                priority='low',
                related_products=top_products.index.tolist(),
                confidence_score=0.95
            ))

        return insights

    def _generate_product_insights(self, transactions_df: pd.DataFrame,
                                   products_df: pd.DataFrame) -> List[Insight]:
        """Generate product-specific insights"""
        insights = []

        # Slow-moving inventory
        product_sales = transactions_df.groupby('product_id')['quantity'].sum()
        products_with_sales = products_df.merge(
            product_sales.reset_index(),
            on='product_id',
            how='left'
        )
        products_with_sales['quantity'] = products_with_sales['quantity'].fillna(0)

        slow_movers = products_with_sales[
            (products_with_sales['current_stock'] > 20) &
            (products_with_sales['quantity'] < 5)
        ]

        if len(slow_movers) > 0:
            insights.append(Insight(
                insight_type='recommendation',
                title=f"{len(slow_movers)} Slow-Moving Products",
                description=f"These products have high stock but low sales. "
                          f"Consider discounts or bundling strategies.",
                priority='medium',
                action_required=True,
                related_products=slow_movers['product_id'].tolist(),
                confidence_score=0.70
            ))

        return insights

    def get_insights_by_priority(self, priority: str = None) -> List[Insight]:
        """Filter insights by priority"""
        if priority:
            return [i for i in self.insights if i.priority == priority]
        return self.insights
