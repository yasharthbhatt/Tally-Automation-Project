"""
Advanced Analytics Engine for Traders
- Stock-out prediction with days left
- Smart reorder engine
- Customer intelligence
- Price intelligence
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
from loguru import logger


class AdvancedAnalytics:
    """Advanced analytics for inventory intelligence"""

    def __init__(self, lead_time_days: int = 7):
        self.lead_time_days = lead_time_days
        self.safety_stock_multiplier = 1.5

    def calculate_stock_risk(self, products_df: pd.DataFrame,
                            transactions_df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate stock risk with days left for each product
        Returns: DataFrame with risk levels (HIGH/MEDIUM/LOW)
        """
        logger.info("Calculating stock risk...")

        risk_data = []

        for _, product in products_df.iterrows():
            product_id = product['product_id']
            current_stock = product['current_stock']

            # Calculate daily consumption from transactions
            product_txns = transactions_df[transactions_df['product_id'] == product_id]

            if len(product_txns) > 0:
                # Calculate daily average over last 30 days
                max_date = product_txns['date'].max()
                min_date = max_date - timedelta(days=30)
                recent_txns = product_txns[product_txns['date'] >= min_date]

                if len(recent_txns) > 0:
                    total_sold = recent_txns['quantity'].sum()
                    days_span = (recent_txns['date'].max() - recent_txns['date'].min()).days + 1
                    daily_consumption = total_sold / max(days_span, 1)
                else:
                    daily_consumption = 0
            else:
                daily_consumption = 0

            # Calculate days left
            if daily_consumption > 0:
                days_left = current_stock / daily_consumption
            else:
                days_left = 999  # No consumption data

            # Determine risk level
            if days_left < 7:
                risk_level = 'HIGH'
                risk_color = '🔴'
            elif days_left < 14:
                risk_level = 'MEDIUM'
                risk_color = '🟡'
            else:
                risk_level = 'LOW'
                risk_color = '🟢'

            risk_data.append({
                'product_id': product_id,
                'product_name': product['name'],
                'current_stock': current_stock,
                'min_stock': product.get('min_stock', 0),
                'daily_consumption': round(daily_consumption, 2),
                'days_left': round(days_left, 1),
                'risk_level': risk_level,
                'risk_icon': risk_color
            })

        risk_df = pd.DataFrame(risk_data)
        risk_df = risk_df.sort_values('days_left')

        logger.info(f"Stock risk calculated for {len(risk_df)} products")
        return risk_df

    def calculate_smart_reorder(self, risk_df: pd.DataFrame,
                                products_df: pd.DataFrame) -> pd.DataFrame:
        """
        Smart reorder engine with formula:
        Reorder Qty = (Daily Consumption × Lead Time) + Safety Stock
        """
        logger.info("Calculating smart reorder quantities...")

        reorder_data = []

        for _, row in risk_df.iterrows():
            daily_consumption = row['daily_consumption']

            if daily_consumption > 0:
                # Reorder formula
                lead_time_qty = daily_consumption * self.lead_time_days
                safety_stock = daily_consumption * self.safety_stock_multiplier
                reorder_qty = int(lead_time_qty + safety_stock)

                # Get product details
                product_info = products_df[products_df['product_id'] == row['product_id']]
                unit_price = product_info['unit_price'].values[0] if len(product_info) > 0 else 0

                # Calculate urgency
                if row['days_left'] <= self.lead_time_days:
                    urgency = 'URGENT'
                    urgency_icon = '🚨'
                elif row['days_left'] <= 14:
                    urgency = 'SOON'
                    urgency_icon = '⚠️'
                else:
                    urgency = 'NORMAL'
                    urgency_icon = '📦'

                reorder_data.append({
                    'urgency': urgency,
                    'urgency_icon': urgency_icon,
                    'product_name': row['product_name'],
                    'current_stock': row['current_stock'],
                    'days_left': row['days_left'],
                    'daily_consumption': daily_consumption,
                    'reorder_quantity': reorder_qty,
                    'estimated_cost': round(reorder_qty * unit_price, 2),
                    'reason': f"Stock will run out in {row['days_left']:.0f} days"
                })

        reorder_df = pd.DataFrame(reorder_data)

        # Sort by urgency
        urgency_order = {'URGENT': 0, 'SOON': 1, 'NORMAL': 2}
        if not reorder_df.empty:
            reorder_df['urgency_rank'] = reorder_df['urgency'].map(urgency_order)
            reorder_df = reorder_df.sort_values('urgency_rank').drop('urgency_rank', axis=1)

        logger.info(f"Generated {len(reorder_df)} reorder recommendations")
        return reorder_df

    def detect_dead_stock(self, products_df: pd.DataFrame,
                         transactions_df: pd.DataFrame,
                         days_threshold: int = 60) -> pd.DataFrame:
        """
        Detect dead stock (items with high stock but no sales)
        """
        logger.info("Detecting dead stock...")

        dead_stock_data = []

        for _, product in products_df.iterrows():
            product_id = product['product_id']
            current_stock = product['current_stock']
            min_stock = product.get('min_stock', 0)

            # Check if stock is above minimum
            if current_stock > min_stock * 2:
                # Check recent sales
                product_txns = transactions_df[transactions_df['product_id'] == product_id]

                if len(product_txns) > 0:
                    last_sale_date = product_txns['date'].max()
                    days_since_sale = (datetime.now() - last_sale_date).days
                else:
                    days_since_sale = 999

                if days_since_sale > days_threshold:
                    dead_stock_data.append({
                        'product_name': product['name'],
                        'current_stock': current_stock,
                        'min_stock': min_stock,
                        'days_since_sale': days_since_sale,
                        'excess_stock': current_stock - min_stock,
                        'recommendation': 'Consider discount or bundling'
                    })

        dead_stock_df = pd.DataFrame(dead_stock_data)
        logger.info(f"Found {len(dead_stock_df)} dead stock items")
        return dead_stock_df

    def customer_intelligence(self, transactions_df: pd.DataFrame,
                            customers_df: pd.DataFrame) -> Dict:
        """
        Customer intelligence with buying patterns and cross-sell opportunities
        """
        logger.info("Analyzing customer intelligence...")

        # Top customers per product
        top_customers_by_product = {}
        for product_id in transactions_df['product_id'].unique():
            product_txns = transactions_df[transactions_df['product_id'] == product_id]
            top_customers = product_txns.groupby('customer_id').agg({
                'quantity': 'sum',
                'total_amount': 'sum'
            }).nlargest(5, 'total_amount')

            # Get customer names
            customer_list = []
            for cust_id in top_customers.index:
                cust_info = customers_df[customers_df['customer_id'] == cust_id]
                if len(cust_info) > 0:
                    customer_list.append({
                        'customer_name': cust_info['name'].values[0],
                        'quantity': int(top_customers.loc[cust_id, 'quantity']),
                        'amount': top_customers.loc[cust_id, 'total_amount']
                    })

            top_customers_by_product[product_id] = customer_list

        # Cross-sell opportunities (customers who buy A but not B)
        cross_sell_opportunities = []

        # Get product pairs
        product_ids = transactions_df['product_id'].unique()
        for i, prod1 in enumerate(product_ids):
            for prod2 in product_ids[i+1:]:
                # Customers buying prod1
                customers_prod1 = set(transactions_df[transactions_df['product_id'] == prod1]['customer_id'])
                # Customers buying prod2
                customers_prod2 = set(transactions_df[transactions_df['product_id'] == prod2]['customer_id'])

                # Customers buying prod1 but not prod2
                cross_sell_customers = customers_prod1 - customers_prod2

                if len(cross_sell_customers) > 0:
                    cross_sell_opportunities.append({
                        'buying_product': prod1,
                        'suggest_product': prod2,
                        'customer_count': len(cross_sell_customers),
                        'customers': list(cross_sell_customers)[:5]  # Top 5
                    })

        # Low activity customers
        if 'last_purchase_date' in customers_df.columns:
            customers_df['days_since_purchase'] = (datetime.now() - customers_df['last_purchase_date']).dt.days
            low_activity = customers_df[customers_df['days_since_purchase'] > 30].nsmallest(10, 'days_since_purchase')
        else:
            low_activity = pd.DataFrame()

        return {
            'top_customers_by_product': top_customers_by_product,
            'cross_sell_opportunities': cross_sell_opportunities,
            'low_activity_customers': low_activity
        }

    def price_intelligence(self, purchases_df: pd.DataFrame,
                          products_df: pd.DataFrame) -> Dict:
        """
        Price intelligence derived from purchase item-wise register.
        purchases_df columns: date, product_name, product_id, rate
        products_df columns: product_id, name, current_stock
        """
        logger.info("Analyzing price intelligence...")

        if purchases_df.empty or 'rate' not in purchases_df.columns:
            empty = pd.DataFrame()
            return {'price_insights': empty, 'volatile_products': empty, 'buying_opportunities': empty}

        price_insights = []

        for product_name in purchases_df['product_name'].unique():
            product_prices = (
                purchases_df[purchases_df['product_name'] == product_name]
                .sort_values('date')
            )

            if len(product_prices) < 2:
                continue

            latest_price = product_prices['rate'].iloc[-1]
            previous_price = product_prices['rate'].iloc[-2]
            avg_price = product_prices['rate'].mean()
            min_price = product_prices['rate'].min()
            max_price = product_prices['rate'].max()

            price_change = ((latest_price - previous_price) / previous_price) * 100 if previous_price else 0

            product_info = products_df[products_df['name'] == product_name]
            current_stock = product_info['current_stock'].values[0] if len(product_info) > 0 else 0

            if price_change < -5:
                recommendation = "📉 PRICE DROPPED → Buy more stock"
                priority = 'HIGH'
            elif price_change > 5:
                recommendation = "📈 PRICE RISING → Reduce holding, sell quickly"
                priority = 'MEDIUM'
            elif latest_price < avg_price * 0.9:
                recommendation = "💰 Below average → Good buying opportunity"
                priority = 'MEDIUM'
            elif latest_price > avg_price * 1.1:
                recommendation = "⚠️ Above average → Monitor closely"
                priority = 'LOW'
            else:
                recommendation = "✅ Stable pricing"
                priority = 'LOW'

            price_insights.append({
                'product': product_name,
                'current_price': latest_price,
                'price_change_pct': round(price_change, 2),
                'avg_price': round(avg_price, 2),
                'min_price': min_price,
                'max_price': max_price,
                'current_stock': current_stock,
                'recommendation': recommendation,
                'priority': priority
            })

        price_insights_df = pd.DataFrame(price_insights)

        if price_insights_df.empty:
            return {'price_insights': price_insights_df, 'volatile_products': price_insights_df, 'buying_opportunities': price_insights_df}

        return {
            'price_insights': price_insights_df,
            'volatile_products': price_insights_df[price_insights_df['price_change_pct'].abs() > 10],
            'buying_opportunities': price_insights_df[price_insights_df['priority'] == 'HIGH']
        }

    def generate_alerts(self, risk_df: pd.DataFrame,
                       reorder_df: pd.DataFrame,
                       price_intelligence: Dict) -> List[str]:
        """
        Generate actionable alerts for traders
        """
        alerts = []

        # Stock-out alerts
        urgent_items = risk_df[risk_df['risk_level'] == 'HIGH']
        for _, item in urgent_items.iterrows():
            alerts.append(
                f"🚨 URGENT: {item['product_name']} will stock out in {item['days_left']:.0f} days "
                f"(Current: {item['current_stock']} units, Daily usage: {item['daily_consumption']:.1f})"
            )

        # Reorder alerts
        urgent_reorders = reorder_df[reorder_df['urgency'] == 'URGENT'].head(3)
        for _, item in urgent_reorders.iterrows():
            alerts.append(
                f"📦 REORDER TODAY: Order {item['reorder_quantity']} units of {item['product_name']} "
                f"(Estimated cost: ₹{item['estimated_cost']:,.0f})"
            )

        # Price alerts
        price_insights = price_intelligence.get('price_insights', pd.DataFrame())
        buying_ops = price_insights[price_insights['priority'] == 'HIGH']
        for _, item in buying_ops.iterrows():
            alerts.append(item['recommendation'] + f" - {item['product']}")

        return alerts
