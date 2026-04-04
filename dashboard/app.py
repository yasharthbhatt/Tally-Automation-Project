"""
Streamlit dashboard for Inventory Intelligence System
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from data_ingestion.tally_parser import TallyParser
from ai_engine.forecasting import DemandForecaster
from ai_engine.customer_segmentation import CustomerSegmentation
from insights.insight_generator import InsightGenerator
from automation.automation_engine import AutomationEngine
from loguru import logger


# Page configuration
st.set_page_config(
    page_title="Inventory Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False


def load_data(uploaded_file):
    """Load and process uploaded data"""
    parser = TallyParser()

    with st.spinner("Parsing data..."):
        customers_df, products_df, transactions_df = parser.parse_excel(uploaded_file)

    # Validate data
    issues = parser.validate_data(customers_df, products_df, transactions_df)

    return customers_df, products_df, transactions_df, issues


def run_ai_analysis(customers_df, products_df, transactions_df):
    """Run AI analysis on the data"""
    results = {}

    # Demand Forecasting
    with st.spinner("Running demand forecasting..."):
        forecaster = DemandForecaster()
        forecaster.train(transactions_df)

        forecasts = []
        for _, product in products_df.head(10).iterrows():  # Forecast top 10 products
            forecast = forecaster.forecast_demand(
                product['product_id'],
                product['name'],
                product['current_stock'],
                transactions_df,
                days_ahead=30
            )
            forecasts.append(forecast)

        results['forecasts'] = forecasts

    # Customer Segmentation
    with st.spinner("Segmenting customers..."):
        segmenter = CustomerSegmentation()
        rfm_df = segmenter.calculate_rfm(transactions_df, customers_df)
        rfm_df = segmenter.segment_customers(rfm_df)
        segment_insights = segmenter.get_segment_insights(rfm_df)

        results['rfm_df'] = rfm_df
        results['segment_insights'] = segment_insights

    # Generate Insights
    with st.spinner("Generating insights..."):
        insight_gen = InsightGenerator()
        insights = insight_gen.generate_all_insights(
            products_df, customers_df, transactions_df, forecasts, rfm_df
        )

        results['insights'] = insights

    # Automation
    with st.spinner("Processing automation..."):
        automation = AutomationEngine()
        automation_results = automation.process_insights(insights)
        reorder_df = automation.generate_reorder_recommendations(forecasts)

        results['automation_results'] = automation_results
        results['reorder_df'] = reorder_df

    return results


def main():
    st.title("📊 Inventory Intelligence Dashboard")
    st.markdown("### AI-Powered Trading Insights from Tally Data")

    # Sidebar
    with st.sidebar:
        st.header("Upload Data")
        uploaded_file = st.file_uploader(
            "Upload Tally Export (Excel)",
            type=['xlsx', 'xls'],
            help="Excel file should contain sheets: Customers, Products, Transactions"
        )

        if uploaded_file:
            if st.button("Process Data"):
                try:
                    # Load data
                    customers_df, products_df, transactions_df, issues = load_data(uploaded_file)

                    # Check for issues
                    has_errors = any(len(v) > 0 for v in issues.values())
                    if has_errors:
                        st.error("Data validation issues found:")
                        for key, msgs in issues.items():
                            if msgs:
                                st.write(f"**{key}**: {', '.join(msgs)}")

                    # Store in session state
                    st.session_state.customers_df = customers_df
                    st.session_state.products_df = products_df
                    st.session_state.transactions_df = transactions_df
                    st.session_state.data_loaded = True

                    # Run AI analysis
                    results = run_ai_analysis(customers_df, products_df, transactions_df)
                    st.session_state.results = results

                    st.success("Data processed successfully!")

                except Exception as e:
                    st.error(f"Error processing file: {e}")
                    logger.error(f"Error: {e}")

    # Main content
    if st.session_state.data_loaded:
        tabs = st.tabs(["📈 Overview", "🔮 Forecasts", "👥 Customers", "💡 Insights", "🤖 Automation"])

        # Overview Tab
        with tabs[0]:
            st.header("Business Overview")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total Products", len(st.session_state.products_df))

            with col2:
                st.metric("Total Customers", len(st.session_state.customers_df))

            with col3:
                st.metric("Total Transactions", len(st.session_state.transactions_df))

            with col4:
                total_revenue = st.session_state.transactions_df['total_amount'].sum()
                st.metric("Total Revenue", f"${total_revenue:,.2f}")

            # Revenue over time
            st.subheader("Revenue Trend")
            daily_revenue = st.session_state.transactions_df.groupby('date')['total_amount'].sum().reset_index()
            fig = px.line(daily_revenue, x='date', y='total_amount', title='Daily Revenue')
            st.plotly_chart(fig, use_container_width=True)

            # Top products
            st.subheader("Top 10 Products by Revenue")
            top_products = st.session_state.transactions_df.groupby('product_id')['total_amount'].sum().nlargest(10)
            fig = px.bar(top_products, orientation='h', title='Top Products')
            st.plotly_chart(fig, use_container_width=True)

        # Forecasts Tab
        with tabs[1]:
            st.header("Demand Forecasts")

            if 'results' in st.session_state:
                forecasts = st.session_state.results['forecasts']

                # Display forecast cards
                for forecast in forecasts[:5]:
                    with st.expander(f"📦 {forecast.product_name}"):
                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.metric("Current Stock", forecast.current_stock)

                        with col2:
                            st.metric("Predicted Demand (30d)", f"{forecast.predicted_demand:.0f}")

                        with col3:
                            st.metric("Recommended Order", forecast.recommended_order_quantity)

                        # Risk indicator
                        risk_color = {'low': '🟢', 'medium': '🟡', 'high': '🔴'}
                        st.write(f"**Risk Level:** {risk_color[forecast.risk_level]} {forecast.risk_level.upper()}")

        # Customers Tab
        with tabs[2]:
            st.header("Customer Segmentation")

            if 'results' in st.session_state:
                rfm_df = st.session_state.results['rfm_df']
                segment_insights = st.session_state.results['segment_insights']

                # Segment distribution
                segment_counts = rfm_df['segment'].value_counts()
                fig = px.pie(values=segment_counts.values, names=segment_counts.index,
                           title='Customer Segments')
                st.plotly_chart(fig, use_container_width=True)

                # Segment details
                st.subheader("Segment Analytics")
                for segment, metrics in segment_insights.items():
                    with st.expander(f"📊 {segment} ({metrics['customer_count']} customers)"):
                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.metric("Avg Recency (days)", f"{metrics['avg_recency']:.0f}")

                        with col2:
                            st.metric("Avg Frequency", f"{metrics['avg_frequency']:.1f}")

                        with col3:
                            st.metric("Avg Monetary", f"${metrics['avg_monetary']:.2f}")

                        st.write(f"**Total Revenue:** ${metrics['total_revenue']:,.2f} "
                               f"({metrics['revenue_percentage']:.1f}% of total)")

        # Insights Tab
        with tabs[3]:
            st.header("AI-Generated Insights")

            if 'results' in st.session_state:
                insights = st.session_state.results['insights']

                # Filter by priority
                priority_filter = st.selectbox("Filter by Priority",
                                              ["All", "critical", "high", "medium", "low"])

                filtered_insights = insights if priority_filter == "All" else \
                                  [i for i in insights if i.priority == priority_filter]

                # Display insights
                priority_colors = {
                    'critical': '🔴',
                    'high': '🟠',
                    'medium': '🟡',
                    'low': '🟢'
                }

                for insight in filtered_insights:
                    priority_icon = priority_colors.get(insight.priority, '⚪')

                    with st.expander(f"{priority_icon} {insight.title}"):
                        st.write(insight.description)
                        st.write(f"**Type:** {insight.insight_type}")
                        st.write(f"**Confidence:** {insight.confidence_score:.0%}")

                        if insight.action_required:
                            st.warning("⚠️ Action Required")

        # Automation Tab
        with tabs[4]:
            st.header("Automation & Recommendations")

            if 'results' in st.session_state:
                automation_results = st.session_state.results['automation_results']
                reorder_df = st.session_state.results['reorder_df']

                # Summary metrics
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Alerts Sent", len(automation_results['alerts_sent']))

                with col2:
                    st.metric("Actions Created", len(automation_results['actions_taken']))

                with col3:
                    st.metric("Recommendations", len(automation_results['recommendations']))

                # Reorder recommendations
                st.subheader("📋 Automated Reorder Recommendations")

                if not reorder_df.empty:
                    st.dataframe(
                        reorder_df,
                        use_container_width=True,
                        hide_index=True
                    )

                    # Download button
                    csv = reorder_df.to_csv(index=False)
                    st.download_button(
                        "Download Reorder List",
                        csv,
                        "reorder_recommendations.csv",
                        "text/csv"
                    )
                else:
                    st.info("No reorder recommendations at this time.")

    else:
        # Welcome screen
        st.info("👈 Upload a Tally export file to get started")

        with st.expander("ℹ️ How to use"):
            st.markdown("""
            1. **Export data from Tally** as an Excel file
            2. Ensure the Excel file contains three sheets:
               - `Customers`: Customer information
               - `Products`: Product/inventory details
               - `Transactions`: Sales transactions
            3. **Upload the file** using the sidebar
            4. Click **Process Data** to run AI analysis
            5. Explore insights across different tabs
            """)


if __name__ == "__main__":
    main()
