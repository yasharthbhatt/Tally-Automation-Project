"""
StockSense - Smart Inventory Intelligence for Tally
AI-Powered Analytics | Smart Inventory. Smarter Business.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent))

from data_ingestion.tally_parser_custom import TallyCustomParser
from ai_engine.forecasting import DemandForecaster
from ai_engine.customer_segmentation import CustomerSegmentation
from ai_engine.advanced_analytics import AdvancedAnalytics
from ai_engine.llm_engine import LLMEngine
from insights.insight_generator import InsightGenerator
from automation.automation_engine import AutomationEngine
from config.packages import PACKAGES, get_available_tabs
from subscription.streamlit_components import (
    render_subscription_page, check_feature_access,
    render_plan_badge, render_upgrade_prompt
)
from subscription import get_subscription_manager

# Page config
st.set_page_config(
    page_title="StockSense - AI-Powered Inventory Intelligence",
    page_icon="🧠",
    layout="wide"
)

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'data' not in st.session_state:
    st.session_state.data = None
if 'results' not in st.session_state:
    st.session_state.results = None
if 'package' not in st.session_state:
    st.session_state.package = 'enterprise'  # Default to enterprise for demo
if 'llm_engine' not in st.session_state:
    # Initialize LLM engine if API keys are available
    llm_provider = os.getenv("LLM_PROVIDER", "openai")
    st.session_state.llm_engine = LLMEngine(provider=llm_provider)
if 'user_id' not in st.session_state:
    # Simple user ID for demo (in production, use proper auth)
    import hashlib
    import platform
    user_id = hashlib.md5(f"{platform.node()}".encode()).hexdigest()[:8]
    st.session_state.user_id = user_id
if 'show_subscription_page' not in st.session_state:
    st.session_state.show_subscription_page = False


def load_tally_data(product_file, customer_file):
    """Load and parse Tally export files"""
    parser = TallyCustomParser()

    # Parse files
    price_df, adoption_df, stock_df = parser.parse_product_reports(product_file)
    ledger_df = parser.parse_customer_ledger(customer_file)

    # Create unified datasets
    unified = parser.create_unified_datasets(price_df, adoption_df, stock_df, ledger_df)

    # Store raw data too
    unified['raw'] = {
        'price': price_df,
        'adoption': adoption_df,
        'stock': stock_df,
        'ledger': ledger_df
    }

    return unified


def run_analysis(data):
    """Run AI analysis"""
    results = {}

    products_df = data['products']
    customers_df = data['customers']
    transactions_df = data['transactions']

    # 1. Demand Forecasting
    with st.spinner("Running demand forecasting..."):
        forecaster = DemandForecaster()
        forecaster.train(transactions_df)

        forecasts = []
        for _, product in products_df.iterrows():
            try:
                forecast = forecaster.forecast_demand(
                    product['product_id'],
                    product['name'],
                    int(product['current_stock']),
                    transactions_df,
                    days_ahead=30
                )
                forecasts.append(forecast)
            except Exception as e:
                st.warning(f"Could not forecast for {product['name']}: {str(e)}")

        results['forecasts'] = forecasts

    # 2. Customer Segmentation
    with st.spinner("Analyzing customers..."):
        segmenter = CustomerSegmentation()
        rfm_df = segmenter.calculate_rfm(transactions_df, customers_df)
        rfm_df = segmenter.segment_customers(rfm_df)
        segment_insights = segmenter.get_segment_insights(rfm_df)

        results['rfm_df'] = rfm_df
        results['segment_insights'] = segment_insights

    # 3. Generate Insights
    with st.spinner("Generating insights..."):
        insight_gen = InsightGenerator()
        insights = insight_gen.generate_all_insights(
            products_df, customers_df, transactions_df, forecasts, rfm_df
        )
        results['insights'] = insights

    # 4. Automation
    automation = AutomationEngine()
    automation_results = automation.process_insights(insights)
    reorder_df = automation.generate_reorder_recommendations(forecasts)

    results['automation'] = automation_results
    results['reorder_df'] = reorder_df

    # 5. Advanced Analytics
    with st.spinner("Running advanced analytics..."):
        advanced = AdvancedAnalytics()

        # Stock risk analysis
        risk_df = advanced.calculate_stock_risk(products_df, transactions_df)
        results['risk_df'] = risk_df

        # Smart reorder
        smart_reorder_df = advanced.calculate_smart_reorder(risk_df, products_df)
        results['smart_reorder_df'] = smart_reorder_df

        # Dead stock detection
        dead_stock_df = advanced.detect_dead_stock(products_df, transactions_df)
        results['dead_stock_df'] = dead_stock_df

        # Customer intelligence
        customer_intel = advanced.customer_intelligence(transactions_df, customers_df)
        results['customer_intel'] = customer_intel

        # Price intelligence
        price_intel = advanced.price_intelligence(data['raw']['price'], data['raw']['stock'])
        results['price_intel'] = price_intel

        # Generate alerts
        alerts = advanced.generate_alerts(risk_df, smart_reorder_df, price_intel)
        results['alerts'] = alerts

    return results


def main():
    st.title("🧠 StockSense")
    st.markdown("### Smart Inventory. Smarter Business.")
    st.caption("AI-Powered Analytics for Tally ERP")

    # Check if user wants to see subscription page
    if st.session_state.get('show_subscription_page', False):
        render_subscription_page(st.session_state.user_id)
        if st.button("← Back to Dashboard"):
            st.session_state.show_subscription_page = False
            st.experimental_rerun()
        return

    # Sidebar
    with st.sidebar:
        # User/Subscription info
        st.markdown("### 👤 Your Account")
        st.caption(f"User ID: {st.session_state.user_id}")
        render_plan_badge(st.session_state.user_id)

        if st.button("💳 Manage Subscription", key="sidebar_manage_subscription"):
            st.session_state.show_subscription_page = True
            st.experimental_rerun()

        st.markdown("---")

        # Package Selection
        st.header("📦 Select Package")

        package_options = {
            'essential': '📦 Essential (₹1,499/mo)',
            'professional': '💼 Professional (₹3,499/mo)',
            'enterprise': '🚀 Enterprise (₹5,999/mo)',
            'ai_plus': '🤖 AI Plus (₹9,999/mo)'
        }

        selected_package = st.selectbox(
            "Choose your plan:",
            options=list(package_options.keys()),
            format_func=lambda x: package_options[x],
            index=3  # Default to AI Plus
        )

        st.session_state.package = selected_package

        # Show package info
        package_info = PACKAGES[selected_package]
        with st.expander("ℹ️ Package Details"):
            st.write(f"**{package_info['name']}**")
            st.write(package_info['description'])
            st.write(f"**Price:** {package_info['price']}")
            st.write("**Features:**")
            for feature in package_info['features']:
                st.write(f"• {feature}")

        st.markdown("---")

        st.header("📁 Upload Tally Exports")

        st.markdown("**Product Reports**")
        product_file = st.file_uploader(
            "product_wise_reports.xlsx",
            type=['xlsx'],
            key='product'
        )

        st.markdown("**Customer Reports**")
        customer_file = st.file_uploader(
            "sample_tally_customer_report.xlsx",
            type=['xlsx'],
            key='customer'
        )

        if product_file and customer_file:
            if st.button("🚀 Process & Analyze"):
                try:
                    with st.spinner("Loading Tally data..."):
                        data = load_tally_data(product_file, customer_file)
                        st.session_state.data = data
                        st.session_state.data_loaded = True

                    # Run analysis
                    results = run_analysis(data)
                    st.session_state.results = results

                    st.success("✅ Analysis complete!")

                except Exception as e:
                    st.error(f"Error: {e}")
                    import traceback
                    st.code(traceback.format_exc())

    # Main content
    if st.session_state.data_loaded and st.session_state.results is not None:
        data = st.session_state.data
        results = st.session_state.results
        package = st.session_state.package

        # Show package info at top
        package_info = PACKAGES[package]
        st.info(f"📦 Current Package: **{package_info['name']}** - {package_info['description']}")

        # Determine tabs based on package
        tab_list = [
            "🚨 Control Panel",
            "📊 Dashboard",
            "🔴 Stock Risk",
            "📦 Smart Reorder",
            "👥 Customer Intelligence",
            "💰 Price Intelligence",
            "📈 Analytics"
        ]

        # Add AI Assistant tab for AI Plus package
        if package == 'ai_plus':
            tab_list.append("🤖 AI Assistant")

        tabs = st.tabs(tab_list)

        # Control Panel Tab
        with tabs[0]:
            st.header("🚨 Control Panel - Quick Actions")

            # Show critical alerts
            if 'alerts' in results and results['alerts']:
                st.subheader("⚡ Critical Alerts")
                for alert in results['alerts'][:5]:  # Top 5 alerts
                    st.warning(alert)

            # Key metrics in 4 columns
            col1, col2, col3, col4 = st.columns(4)

            risk_df = results.get('risk_df', pd.DataFrame())
            smart_reorder_df = results.get('smart_reorder_df', pd.DataFrame())

            with col1:
                high_risk_count = len(risk_df[risk_df['risk_level'] == 'HIGH']) if not risk_df.empty else 0
                st.metric("🔴 HIGH RISK Items", high_risk_count)

            with col2:
                urgent_reorders = len(smart_reorder_df[smart_reorder_df['urgency'] == 'URGENT']) if not smart_reorder_df.empty else 0
                st.metric("🚨 URGENT Reorders", urgent_reorders)

            with col3:
                dead_stock_count = len(results.get('dead_stock_df', []))
                st.metric("📦 Dead Stock Items", dead_stock_count)

            with col4:
                total_revenue = data['ledger']['Debit (₹)'].sum()
                st.metric("💰 Total Revenue", f"₹{total_revenue:,.0f}")

            # Quick action panels
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📦 Today's Action Items")
                if not smart_reorder_df.empty:
                    urgent = smart_reorder_df[smart_reorder_df['urgency'] == 'URGENT']
                    if not urgent.empty:
                        for _, item in urgent.iterrows():
                            st.error(f"{item['urgency_icon']} **{item['product_name']}**")
                            st.write(f"   Order {item['reorder_quantity']} units (₹{item['estimated_cost']:,.0f})")
                            st.write(f"   Reason: {item['reason']}")
                    else:
                        st.success("✅ No urgent actions required today!")
                else:
                    st.info("No reorder data available")

            with col2:
                st.subheader("💰 Price Opportunities")
                price_intel = results.get('price_intel', {})
                buying_ops = price_intel.get('buying_opportunities', pd.DataFrame())

                if not buying_ops.empty:
                    for _, item in buying_ops.iterrows():
                        st.success(f"**{item['product']}**")
                        st.write(f"   {item['recommendation']}")
                        st.write(f"   Current: ₹{item['current_price']}, Change: {item['price_change_pct']:+.1f}%")
                else:
                    st.info("No special price opportunities right now")

        # Dashboard Tab
        with tabs[1]:
            st.header("Business Dashboard")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Products", len(data['products']))

            with col2:
                st.metric("Customers", len(data['customers']))

            with col3:
                total_stock = data['products']['current_stock'].sum()
                st.metric("Total Stock", f"{int(total_stock):,} units")

            with col4:
                total_revenue = data['ledger']['Debit (₹)'].sum()
                st.metric("Total Revenue", f"₹{total_revenue:,.0f}")

            # Stock Summary
            st.subheader("📦 Stock Overview")
            stock_viz = data['products'][['name', 'current_stock', 'min_stock', 'max_stock']].copy()

            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Current Stock',
                x=stock_viz['name'],
                y=stock_viz['current_stock'],
                marker_color='steelblue'
            ))
            fig.add_trace(go.Scatter(
                name='Min Stock',
                x=stock_viz['name'],
                y=stock_viz['min_stock'],
                mode='lines',
                line=dict(color='red', dash='dash')
            ))
            fig.update_layout(title='Stock Levels vs. Min Stock', barmode='group')
            st.plotly_chart(fig, use_container_width=True)

            # Customer Activity
            st.subheader("👥 Top Customers by Revenue")
            top_customers = data['ledger'].groupby('Customer Name')['Debit (₹)'].sum().nlargest(10)
            fig = px.bar(top_customers, orientation='h', title='Top 10 Customers')
            fig.update_xaxes(title='Revenue (₹)')
            st.plotly_chart(fig, use_container_width=True)

        # Stock Risk Tab
        with tabs[2]:
            st.header("🔴 Stock Risk Panel")

            risk_df = results.get('risk_df', pd.DataFrame())

            if not risk_df.empty:
                # Risk summary
                col1, col2, col3 = st.columns(3)

                with col1:
                    high_risk = len(risk_df[risk_df['risk_level'] == 'HIGH'])
                    st.metric("🔴 HIGH RISK", high_risk)

                with col2:
                    medium_risk = len(risk_df[risk_df['risk_level'] == 'MEDIUM'])
                    st.metric("🟡 MEDIUM RISK", medium_risk)

                with col3:
                    low_risk = len(risk_df[risk_df['risk_level'] == 'LOW'])
                    st.metric("🟢 LOW RISK", low_risk)

                # Risk table
                st.subheader("Stock Status by Days Left")

                # Add color coding
                def color_risk(row):
                    if row['risk_level'] == 'HIGH':
                        return f"{row['risk_icon']} {row['product_name']}"
                    elif row['risk_level'] == 'MEDIUM':
                        return f"{row['risk_icon']} {row['product_name']}"
                    else:
                        return f"{row['risk_icon']} {row['product_name']}"

                display_df = risk_df[['product_name', 'current_stock', 'min_stock', 'daily_consumption', 'days_left', 'risk_level']].copy()
                display_df.columns = ['Product', 'Current Stock', 'Min Stock', 'Daily Usage', 'Days Left', 'Risk']
                st.dataframe(display_df)

                # Chart of days left
                fig = px.bar(risk_df, x='product_name', y='days_left',
                           color='risk_level',
                           color_discrete_map={'HIGH': '#FF4B4B', 'MEDIUM': '#FFA500', 'LOW': '#00CC00'},
                           title='Stock Days Remaining',
                           labels={'days_left': 'Days Until Stock-Out', 'product_name': 'Product'})
                st.plotly_chart(fig, use_container_width=True)

                # Dead stock section
                dead_stock_df = results.get('dead_stock_df', pd.DataFrame())
                if not dead_stock_df.empty:
                    st.subheader("📦 Dead Stock Alert")
                    st.warning(f"Found {len(dead_stock_df)} items with excess stock and low sales")
                    st.dataframe(dead_stock_df)
            else:
                st.info("No stock risk data available")

        # Smart Reorder Tab
        with tabs[3]:
            st.header("📦 Smart Reorder Engine")

            smart_reorder_df = results.get('smart_reorder_df', pd.DataFrame())

            if not smart_reorder_df.empty:
                st.subheader("💡 Reorder Formula Used:")
                st.code("Reorder Qty = (Daily Consumption × Lead Time Days) + Safety Stock")

                # Urgency breakdown
                col1, col2, col3 = st.columns(3)

                with col1:
                    urgent_count = len(smart_reorder_df[smart_reorder_df['urgency'] == 'URGENT'])
                    st.metric("🚨 URGENT", urgent_count)

                with col2:
                    soon_count = len(smart_reorder_df[smart_reorder_df['urgency'] == 'SOON'])
                    st.metric("⚠️ SOON", soon_count)

                with col3:
                    total_cost = smart_reorder_df['estimated_cost'].sum()
                    st.metric("💰 Total Cost", f"₹{total_cost:,.0f}")

                # Reorder recommendations
                st.subheader("📋 Reorder Recommendations")

                for urgency in ['URGENT', 'SOON', 'NORMAL']:
                    urgency_items = smart_reorder_df[smart_reorder_df['urgency'] == urgency]

                    if not urgency_items.empty:
                        with st.expander(f"{urgency_items.iloc[0]['urgency_icon']} {urgency} - {len(urgency_items)} items"):
                            for _, item in urgency_items.iterrows():
                                st.markdown(f"**{item['product_name']}**")
                                col1, col2, col3, col4 = st.columns(4)
                                with col1:
                                    st.write(f"Order: **{item['reorder_quantity']}** units")
                                with col2:
                                    st.write(f"Current: {item['current_stock']}")
                                with col3:
                                    st.write(f"Days left: {item['days_left']:.0f}")
                                with col4:
                                    st.write(f"Cost: ₹{item['estimated_cost']:,.0f}")
                                st.write(f"_{item['reason']}_")
                                st.markdown("---")

                # Download button
                csv = smart_reorder_df.to_csv(index=False)
                st.download_button(
                    "📥 Download Reorder List",
                    csv,
                    "smart_reorder_list.csv",
                    "text/csv"
                )
            else:
                st.info("No reorder recommendations available")

        # Customer Intelligence Tab
        with tabs[4]:
            st.header("👥 Customer Intelligence")

            customer_intel = results.get('customer_intel', {})

            # Top customers by product
            st.subheader("Top Customers by Product")
            top_customers_by_product = customer_intel.get('top_customers_by_product', {})

            if top_customers_by_product:
                for product_id, customers in list(top_customers_by_product.items())[:5]:
                    if customers:
                        product_name = customers[0].get('product_name', product_id)
                        with st.expander(f"📦 Top buyers - {product_id}"):
                            for cust in customers[:5]:
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.write(f"**{cust['customer_name']}**")
                                with col2:
                                    st.write(f"Qty: {cust['quantity']}")
                                with col3:
                                    st.write(f"₹{cust['amount']:,.0f}")

            # Cross-sell opportunities
            st.subheader("🎯 Cross-Sell Opportunities")
            cross_sell = customer_intel.get('cross_sell_opportunities', [])

            if cross_sell:
                st.info("💡 Customers buying Product A but not Product B - Opportunity to cross-sell!")
                for opp in cross_sell[:5]:
                    st.write(f"• Customers buying **{opp['buying_product']}** → Suggest **{opp['suggest_product']}**")
                    st.write(f"  Potential: {opp['customer_count']} customers")
                    st.markdown("---")
            else:
                st.info("No cross-sell opportunities detected")

            # Low activity customers
            st.subheader("⚠️ Low Activity Customers")
            low_activity = customer_intel.get('low_activity_customers', pd.DataFrame())

            if not low_activity.empty:
                st.warning(f"Found {len(low_activity)} customers with low activity")
                display_cols = ['name', 'days_since_purchase', 'total_purchases']
                available_cols = [col for col in display_cols if col in low_activity.columns]
                if available_cols:
                    st.dataframe(low_activity[available_cols].head(10))
            else:
                st.success("All customers are active!")

            # Customer segments (RFM)
            if 'rfm_df' in results:
                st.subheader("👥 Customer Segmentation")

                segment_counts = results['rfm_df']['segment'].value_counts()
                fig = px.pie(values=segment_counts.values, names=segment_counts.index,
                           title='Customer Segments', hole=0.4)
                st.plotly_chart(fig, use_container_width=True)

                # Segment details
                st.subheader("Segment Analytics")
                for segment, metrics in results['segment_insights'].items():
                    with st.expander(f"{segment} - {metrics['customer_count']} customers"):
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Avg Recency", f"{metrics['avg_recency']:.0f} days")
                        with col2:
                            st.metric("Avg Frequency", f"{metrics['avg_frequency']:.1f}")
                        with col3:
                            st.metric("Avg Value", f"₹{metrics['avg_monetary']:.0f}")
                        with col4:
                            st.metric("Revenue %", f"{metrics['revenue_percentage']:.1f}%")

            # Customer adoption
            st.subheader("Product Adoption by Customer")
            adoption_df = data['raw']['adoption']
            fig = px.bar(adoption_df.nlargest(15, 'Quantity Purchased'),
                        x='Quantity Purchased', y='Customer Name',
                        color='Product', orientation='h',
                        title='Top 15 Customer-Product Combinations')
            st.plotly_chart(fig, use_container_width=True)

        # Price Intelligence Tab
        with tabs[5]:
            st.header("💰 Price Intelligence")

            price_intel = results.get('price_intel', {})
            price_insights_df = price_intel.get('price_insights', pd.DataFrame())

            if not price_insights_df.empty:
                # Summary metrics
                col1, col2, col3 = st.columns(3)

                with col1:
                    high_priority = len(price_insights_df[price_insights_df['priority'] == 'HIGH'])
                    st.metric("📉 Buying Opportunities", high_priority)

                with col2:
                    volatile = len(price_intel.get('volatile_products', []))
                    st.metric("📊 Volatile Products", volatile)

                with col3:
                    avg_change = price_insights_df['price_change_pct'].mean()
                    st.metric("Avg Price Change", f"{avg_change:+.1f}%")

                # Price recommendations
                st.subheader("💡 Smart Pricing Actions")

                for _, item in price_insights_df.iterrows():
                    with st.expander(f"**{item['product']}** - {item['recommendation'][:30]}..."):
                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.metric("Current Price", f"₹{item['current_price']}")
                            delta = item['price_change_pct']
                            st.metric("Change", f"{delta:+.1f}%", delta=f"{delta:.1f}%")

                        with col2:
                            st.metric("Avg Price", f"₹{item['avg_price']}")
                            st.metric("Range", f"₹{item['min_price']} - ₹{item['max_price']}")

                        with col3:
                            st.metric("Current Stock", f"{item['current_stock']} units")
                            st.metric("Priority", item['priority'])

                        st.info(item['recommendation'])

                # Price trends chart
                st.subheader("📈 Price Trends")
                price_df = data['raw']['price']
                selected_product = st.selectbox("Select Product", price_df['Product'].unique(), key='price_intel_select')

                product_prices = price_df[price_df['Product'] == selected_product].sort_values('Date')
                fig = px.line(product_prices, x='Date', y='Price (₹)',
                            title=f'Price Trend: {selected_product}',
                            markers=True)

                # Add average line
                avg_price = product_prices['Price (₹)'].mean()
                fig.add_hline(y=avg_price, line_dash="dash", line_color="red",
                            annotation_text=f"Avg: ₹{avg_price:.0f}")

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No price intelligence data available")

        # Analytics Tab
        with tabs[6]:
            st.header("📈 Advanced Analytics")

            # Sales trends
            st.subheader("💰 Sales Trends")

            ledger_df = data['ledger']
            daily_sales = ledger_df.groupby('Date')['Debit (₹)'].sum().reset_index()
            daily_sales = daily_sales.sort_values('Date')

            fig = px.line(daily_sales, x='Date', y='Debit (₹)',
                        title='Daily Sales Revenue',
                        markers=True)
            st.plotly_chart(fig, use_container_width=True)

            # Monthly summary
            ledger_df['Month'] = ledger_df['Date'].dt.to_period('M').astype(str)
            monthly_sales = ledger_df.groupby('Month')['Debit (₹)'].sum().reset_index()

            col1, col2 = st.columns(2)

            with col1:
                fig = px.bar(monthly_sales, x='Month', y='Debit (₹)',
                           title='Monthly Sales')
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Product category performance
                if 'category' in data['products'].columns:
                    transactions_df = data['transactions']
                    category_sales = transactions_df.merge(
                        data['products'][['product_id', 'category']],
                        on='product_id'
                    )
                    category_revenue = category_sales.groupby('category')['total_amount'].sum()

                    fig = px.pie(values=category_revenue.values,
                               names=category_revenue.index,
                               title='Revenue by Category')
                    st.plotly_chart(fig, use_container_width=True)

            # Stock efficiency
            st.subheader("📦 Stock Efficiency Metrics")

            col1, col2, col3 = st.columns(3)

            with col1:
                total_stock_value = (data['products']['current_stock'] * data['products']['unit_price']).sum()
                st.metric("Total Stock Value", f"₹{total_stock_value:,.0f}")

            with col2:
                avg_days_stock = results.get('risk_df', pd.DataFrame()).get('days_left', pd.Series([0])).mean()
                st.metric("Avg Stock Days", f"{avg_days_stock:.0f}")

            with col3:
                total_revenue = data['ledger']['Debit (₹)'].sum()
                stock_turnover = total_revenue / max(total_stock_value, 1)
                st.metric("Stock Turnover", f"{stock_turnover:.2f}x")

            # Export all data
            st.subheader("📥 Export Reports")

            col1, col2, col3 = st.columns(3)

            with col1:
                if not results.get('smart_reorder_df', pd.DataFrame()).empty:
                    csv = results['smart_reorder_df'].to_csv(index=False)
                    st.download_button("Download Reorder List", csv, "reorder_list.csv", "text/csv")

            with col2:
                if not results.get('risk_df', pd.DataFrame()).empty:
                    csv = results['risk_df'].to_csv(index=False)
                    st.download_button("Download Risk Report", csv, "stock_risk.csv", "text/csv")

            with col3:
                if not price_insights_df.empty:
                    csv = price_insights_df.to_csv(index=False)
                    st.download_button("Download Price Report", csv, "price_intelligence.csv", "text/csv")

        # AI Assistant Tab (AI Plus Package only)
        if package == 'ai_plus':
            with tabs[7]:
                st.header("🤖 AI Assistant - Natural Language Intelligence")

                # Check subscription access
                if not check_feature_access(st.session_state.user_id, 'ai_assistant', show_prompt=True):
                    st.info("💡 Try AI Assistant features or upgrade to unlock unlimited access")
                    # Show limited demo
                else:
                    # Full access
                    pass

                # Check if LLM is configured
                import os
                has_api_key = os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")

                if not has_api_key:
                    st.warning("⚠️ AI Assistant requires API key configuration")
                    with st.expander("📖 How to Enable AI Assistant"):
                        st.markdown("""
                        ### Setup Instructions:

                        1. **Get an API Key:**
                           - OpenAI: https://platform.openai.com/api-keys
                           - Anthropic: https://console.anthropic.com/

                        2. **Add to .env file:**
                           ```
                           OPENAI_API_KEY=your_key_here
                           # or
                           ANTHROPIC_API_KEY=your_key_here
                           ```

                        3. **Install LLM libraries:**
                           ```bash
                           pip install openai anthropic
                           ```

                        4. **Restart the dashboard**

                        ### What You'll Get:
                        - 🤖 Natural language queries
                        - 📝 Automated report generation
                        - 💬 Conversational AI assistant
                        - 🎯 Smart recommendations
                        """)
                else:
                    st.success("✅ AI Assistant is enabled!")

                    # Natural Language Query Section
                    st.subheader("💬 Ask Questions in Plain English")

                    st.write("**Examples:**")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.info("• Which products are at high risk?")
                        st.info("• What should I reorder today?")
                        st.info("• Show me my top 5 customers")
                    with col2:
                        st.info("• Which products have price drops?")
                        st.info("• Who are my at-risk customers?")
                        st.info("• Give me a business summary")

                    # Query input
                    user_query = st.text_input("Ask me anything about your inventory:",
                                              placeholder="e.g., Which products will stock out soon?")

                    if st.button("🔍 Get Answer"):
                        if user_query:
                            with st.spinner("AI is thinking..."):
                                # Build enhanced context for LLM
                                risk_df = results.get('risk_df', pd.DataFrame())
                                reorder_df = results.get('smart_reorder_df', pd.DataFrame())

                                # Get specific high-risk products
                                high_risk_items = []
                                if not risk_df.empty:
                                    high_risk = risk_df[risk_df['risk_level'] == 'HIGH']
                                    for _, item in high_risk.iterrows():
                                        high_risk_items.append({
                                            'name': item['product_name'],
                                            'days_left': item['days_left'],
                                            'current_stock': item['current_stock']
                                        })

                                # Get specific urgent reorders
                                urgent_items = []
                                if not reorder_df.empty:
                                    urgent = reorder_df[reorder_df['urgency'] == 'URGENT']
                                    for _, item in urgent.iterrows():
                                        urgent_items.append({
                                            'name': item['product_name'],
                                            'quantity': item['reorder_quantity'],
                                            'cost': item['estimated_cost'],
                                            'reason': item['reason']
                                        })

                                # Build customer data
                                customer_data = []
                                rfm_df = results.get('rfm_df', pd.DataFrame())
                                if not rfm_df.empty:
                                    for _, cust in rfm_df.head(10).iterrows():  # Top 10 customers
                                        customer_data.append({
                                            'name': cust.get('name', 'Unknown Customer'),
                                            'segment': cust.get('segment', 'Unknown'),
                                            'total_spent': cust.get('monetary', 0),
                                            'purchase_count': cust.get('frequency', 0),
                                            'days_since_last': cust.get('recency', 0)
                                        })

                                # Build segment summary
                                segment_summary = {}
                                if not rfm_df.empty and 'segment' in rfm_df.columns:
                                    segment_summary = rfm_df['segment'].value_counts().to_dict()

                                context = {
                                    'products_count': len(data['products']),
                                    'high_risk_products': len(high_risk_items),
                                    'high_risk_details': high_risk_items[:5],  # Top 5
                                    'urgent_reorders': len(urgent_items),
                                    'urgent_reorder_details': urgent_items[:5],  # Top 5
                                    'alerts': results.get('alerts', [])[:5],  # Top 5 alerts
                                    'revenue': data['ledger']['Debit (₹)'].sum(),
                                    'top_products': data['products'].nlargest(5, 'current_stock')['name'].tolist() if 'current_stock' in data['products'].columns else [],
                                    'customer_count': len(data['customers']),
                                    'customer_data': customer_data,
                                    'segment_summary': segment_summary,
                                    'transactions': data['transactions']
                                }

                                # Get answer from LLM
                                llm_engine = st.session_state.llm_engine
                                if llm_engine.enabled:
                                    answer = llm_engine.natural_language_query(user_query, context)
                                    st.success("🤖 AI Assistant:")
                                    st.write(answer)
                                else:
                                    st.error("❌ LLM engine is not enabled. Please check your API key configuration in .env file.")
                        else:
                            st.warning("Please enter a question")

                    st.markdown("---")

                    # Automated Report Generation
                    st.subheader("📝 Generate AI Reports")

                    col1, col2 = st.columns(2)

                    with col1:
                        if st.button("📊 Generate Executive Summary"):
                            with st.spinner("Generating report..."):
                                llm_engine = st.session_state.llm_engine
                                if llm_engine.enabled:
                                    report = llm_engine.generate_narrative_report(results)
                                    st.success("📊 Executive Summary")
                                    st.write(report)
                                else:
                                    st.error("❌ LLM engine is not enabled. Please check your API key configuration.")

                    with col2:
                        if st.button("🎯 Get Smart Recommendations"):
                            with st.spinner("Analyzing..."):
                                llm_engine = st.session_state.llm_engine
                                if llm_engine.enabled:
                                    context = {
                                        'products_count': len(data['products']),
                                        'high_risk_products': len(results.get('risk_df', pd.DataFrame())[results.get('risk_df', pd.DataFrame())['risk_level'] == 'HIGH']) if not results.get('risk_df', pd.DataFrame()).empty else 0,
                                        'urgent_reorders': len(results.get('smart_reorder_df', pd.DataFrame())[results.get('smart_reorder_df', pd.DataFrame())['urgency'] == 'URGENT']) if not results.get('smart_reorder_df', pd.DataFrame()).empty else 0,
                                        'alerts': results.get('alerts', []),
                                        'revenue': data['ledger']['Debit (₹)'].sum()
                                    }
                                    recommendations = llm_engine.smart_recommendations(context)
                                    st.success("🎯 Smart Recommendations")
                                    for rec in recommendations:
                                        st.write(f"• {rec}")
                                else:
                                    st.error("❌ LLM engine is not enabled. Please check your API key configuration.")

                    st.markdown("---")

                    # Chatbot Interface
                    st.subheader("💬 AI Chat Assistant")

                    if 'chat_messages' not in st.session_state:
                        st.session_state.chat_messages = []

                    # Display chat history
                    if st.session_state.chat_messages:
                        st.write("**Conversation History:**")
                        for i, msg in enumerate(st.session_state.chat_messages):
                            if msg["role"] == "user":
                                st.info(f"👤 You: {msg['content']}")
                            else:
                                st.success(f"🤖 AI: {msg['content']}")

                    # Chat input
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        prompt = st.text_input("Chat with AI about your business:", key="chat_input")
                    with col2:
                        send_button = st.button("Send")

                    if send_button and prompt:
                        st.session_state.chat_messages.append({"role": "user", "content": prompt})

                        # Build enhanced context for chat
                        risk_df = results.get('risk_df', pd.DataFrame())
                        reorder_df = results.get('smart_reorder_df', pd.DataFrame())

                        # Get specific high-risk products
                        high_risk_items = []
                        if not risk_df.empty:
                            high_risk = risk_df[risk_df['risk_level'] == 'HIGH']
                            for _, item in high_risk.iterrows():
                                high_risk_items.append({
                                    'name': item['product_name'],
                                    'days_left': item['days_left'],
                                    'current_stock': item['current_stock']
                                })

                        # Get specific urgent reorders
                        urgent_items = []
                        if not reorder_df.empty:
                            urgent = reorder_df[reorder_df['urgency'] == 'URGENT']
                            for _, item in urgent.iterrows():
                                urgent_items.append({
                                    'name': item['product_name'],
                                    'quantity': item['reorder_quantity'],
                                    'cost': item['estimated_cost'],
                                    'reason': item['reason']
                                })

                        # Build customer data
                        customer_data = []
                        rfm_df = results.get('rfm_df', pd.DataFrame())
                        if not rfm_df.empty:
                            for _, cust in rfm_df.head(10).iterrows():  # Top 10 customers
                                customer_data.append({
                                    'name': cust.get('name', 'Unknown Customer'),
                                    'segment': cust.get('segment', 'Unknown'),
                                    'total_spent': cust.get('monetary', 0),
                                    'purchase_count': cust.get('frequency', 0),
                                    'days_since_last': cust.get('recency', 0)
                                })

                        # Build segment summary
                        segment_summary = {}
                        if not rfm_df.empty and 'segment' in rfm_df.columns:
                            segment_summary = rfm_df['segment'].value_counts().to_dict()

                        context = {
                            'products_count': len(data['products']),
                            'high_risk_products': len(high_risk_items),
                            'high_risk_details': high_risk_items[:5],
                            'urgent_reorders': len(urgent_items),
                            'urgent_reorder_details': urgent_items[:5],
                            'alerts': results.get('alerts', [])[:5],
                            'revenue': data['ledger']['Debit (₹)'].sum(),
                            'top_products': data['products'].nlargest(5, 'current_stock')['name'].tolist() if 'current_stock' in data['products'].columns else [],
                            'customer_count': len(data['customers']),
                            'customer_data': customer_data,
                            'segment_summary': segment_summary,
                            'transactions': data['transactions']
                        }

                        # Get response from LLM
                        llm_engine = st.session_state.llm_engine
                        if llm_engine.enabled:
                            response = llm_engine.chat_interface(st.session_state.chat_messages, context)
                        else:
                            response = "❌ LLM engine is not enabled. Please check your API key configuration in .env file."

                        st.session_state.chat_messages.append({"role": "assistant", "content": response})

                        st.experimental_rerun()

                    # Feature Preview
                    st.markdown("---")
                    st.subheader("🚀 Coming Soon in AI Plus")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.info("🌐 Multi-language\nAsk in Hindi/English")

                    with col2:
                        st.info("🎤 Voice Commands\nSpeak your queries")

                    with col3:
                        st.info("📱 Mobile App\nAI on the go")

    else:
        # Welcome screen
        st.info("👈 Upload your Tally export files to get started with StockSense")

        # Hero section
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("⚡ AI Analysis", "< 30 sec", help="Get insights in under 30 seconds")
        with col2:
            st.metric("🎯 Accuracy", "95%+", help="Highly accurate demand forecasts")
        with col3:
            st.metric("💰 ROI", "10-20x", help="Average return on investment")

        with st.expander("ℹ️ Quick Start Guide"):
            st.markdown("""
            ### How to Use StockSense

            1. **Export from Tally**:
               - Export product-wise reports (Price Fluctuation, Customer Adoption, Stock Summary)
               - Export customer ledger report

            2. **Upload Files**:
               - Upload `product_wise_reports.xlsx`
               - Upload `sample_tally_customer_report.xlsx`

            3. **Process & Analyze**:
               - Click the "Process & Analyze" button
               - Wait for AI analysis to complete (~30 seconds)

            4. **Explore Insights**:
               - View dashboards, forecasts, and recommendations
               - Ask questions in natural language (AI Plus)
               - Download reorder lists
            """)

    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        st.markdown("""
        <div style='text-align: center; color: #666;'>
            <p>🧠 <strong>StockSense</strong></p>
            <p style='font-size: 0.8em;'>Smart Inventory. Smarter Business.</p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
