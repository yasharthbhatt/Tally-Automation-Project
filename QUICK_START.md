# Quick Start Guide

## 🚀 Running the Application

### Start the Dashboard
```bash
source .venv/bin/activate
streamlit run app_tally.py
```

The dashboard will open at: **http://localhost:8501**

## 📁 Your Data Files

Your Tally exports are in the `data/` directory:
- `product_wise_reports.xlsx`
- `sample_tally_customer_report.xlsx`

## 💡 Key Features

### 1. Upload & Process
- Upload both Tally export files
- Click "Process & Analyze"
- Wait for AI analysis (~30 seconds)

### 2. Explore Tabs

**📊 Dashboard**
- Overview metrics (products, customers, stock, revenue)
- Stock level visualizations
- Top customers by revenue

**📈 Price & Stock Analysis**
- Price trend charts for each product
- Stock status table with alerts
- Historical price analysis

**👥 Customer Insights**
- Customer segmentation (Champions, Loyal, At Risk, etc.)
- RFM analysis (Recency, Frequency, Monetary)
- Product adoption patterns

**🔮 Forecasts**
- 30-day demand predictions
- Recommended reorder quantities
- Risk levels (Low/Medium/High)

**💡 AI Insights**
- Critical alerts for low stock
- Stockout risk warnings
- Customer engagement recommendations
- Sales pattern analysis

**🤖 Automation**
- Automated reorder recommendations
- Prioritized action items
- Downloadable CSV reports

## 📊 Understanding Your Data

### Products Analyzed
- Rice Premium, Rice Standard
- Mustard Oil, Refined Oil
- Stock levels and price trends

### Customer Segments
- **Champions**: High value, frequent buyers
- **Loyal Customers**: Regular purchasers
- **At Risk**: Haven't purchased recently
- **Lost Customers**: Need re-engagement

### AI Predictions
- Forecasts based on historical patterns
- Considers seasonality and trends
- Provides confidence intervals

## 🎯 Common Tasks

### Get Reorder Recommendations
1. Go to "Automation" tab
2. View prioritized reorder list
3. Download as CSV
4. Share with procurement team

### Analyze Price Trends
1. Go to "Price & Stock Analysis"
2. Select product from dropdown
3. View price chart over time
4. Check current vs historical prices

### Identify At-Risk Customers
1. Go to "Customer Insights"
2. Look at "At Risk" segment
3. View customer details
4. Plan re-engagement campaigns

### Monitor Stock Levels
1. Go to "Dashboard"
2. View stock levels chart
3. Red line = minimum stock threshold
4. Check for items below min

## 🔄 Updating Data

To analyze new Tally exports:
1. Export latest data from Tally
2. Upload new files in sidebar
3. Click "Process & Analyze" again
4. All insights will be refreshed

## 📥 Exporting Results

**Download Options:**
- Reorder recommendations (CSV)
- Customer segments (view in app)
- Charts (right-click → Save image)

## 🆘 Troubleshooting

**Dashboard won't start?**
```bash
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app_tally.py
```

**Upload fails?**
- Check Excel file format
- Ensure sheets are named correctly:
  - Product file: 'Price Fluctuation', 'Customer Adoption', 'Stock Summary'
  - Customer file: 'Customer Ledger Report'

**No forecasts showing?**
- Need at least 7 transaction records per product
- Check if transaction data is available

## 📞 Next Steps

1. **Test with your data**: Upload and process your files
2. **Review insights**: Check AI-generated recommendations
3. **Export reports**: Download reorder lists
4. **Iterate**: Upload new data weekly/monthly

## 🎨 Customization

Want to modify thresholds?
- Edit `.env` file:
  - `LOW_STOCK_THRESHOLD=10`
  - `REORDER_POINT_MULTIPLIER=1.5`

## 📚 Project Structure

```
├── app_tally.py              # Main dashboard application
├── data/                     # Your Tally export files
├── data_ingestion/           # Data parsing logic
│   └── tally_parser_custom.py
├── ai_engine/                # ML models
│   ├── forecasting.py
│   └── customer_segmentation.py
├── insights/                 # Insight generation
│   └── insight_generator.py
├── automation/               # Automation engine
│   └── automation_engine.py
└── models/                   # Data schemas
    └── schemas.py
```

Happy Trading! 📈
