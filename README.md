# 🧠 StockSense

**Smart Inventory. Smarter Business.**

AI-powered inventory management and customer intelligence system for traders working with Tally data.

## Features

- **📊 Data Ingestion**: Parse Tally exports (Excel/XML)
- **🤖 AI-Powered Forecasting**: Predict product demand using ML
- **👥 Customer Segmentation**: RFM analysis and intelligent clustering
- **💡 Smart Insights**: Automated business intelligence
- **🔔 Automation**: Alerts, reorder recommendations, and action items
- **📈 Interactive Dashboard**: Real-time visualizations and analytics

## Architecture

```
Tally → Export Data (Excel/XML)
        ↓
AI Layer (Forecasting, Segmentation, Analysis)
        ↓
Dashboard + Automation + Insights
```

## 🚀 Quick Installation

### For New Installations:

**Windows:**
1. Double-click `install.bat`
2. Double-click `run_dashboard.bat`

**Mac/Linux:**
1. Open Terminal
2. Run: `./install.sh`
3. Run: `./run_dashboard.sh`

**Dashboard opens at:** `http://localhost:8501`

📖 **Detailed instructions:** See [INSTALLATION.md](INSTALLATION.md)

---

## Installation (Manual)

2. **Activate virtual environment**
```bash
source .venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Usage

### Running the Dashboard

```bash
streamlit run dashboard/app.py
```

The dashboard will open in your browser at `http://localhost:8501`

### Data Format

Your Tally export Excel file should contain three sheets:

#### 1. Customers Sheet
| customer_id | name | email | phone | total_purchases | purchase_count | last_purchase_date |
|-------------|------|-------|-------|-----------------|----------------|-------------------|

#### 2. Products Sheet
| product_id | name | category | sku | current_stock | unit_price | cost_price | reorder_level | supplier |
|------------|------|----------|-----|---------------|------------|------------|---------------|----------|

#### 3. Transactions Sheet
| transaction_id | date | customer_id | product_id | quantity | unit_price | total_amount | payment_method |
|----------------|------|-------------|------------|----------|------------|--------------|----------------|

## Project Structure

```
├── data_ingestion/       # Tally data parsers
│   └── tally_parser.py
├── ai_engine/           # ML models and AI logic
│   ├── forecasting.py
│   └── customer_segmentation.py
├── insights/            # Insight generation
│   └── insight_generator.py
├── automation/          # Automation engine
│   └── automation_engine.py
├── dashboard/           # Streamlit dashboard
│   └── app.py
├── models/              # Data schemas
│   └── schemas.py
├── utils/               # Helper functions
├── data/                # Data storage
└── config/              # Configuration
```

## Key Components

### 1. Demand Forecasting
- Time-series analysis
- ML-based predictions
- Rolling statistics
- Confidence intervals

### 2. Customer Segmentation
- RFM (Recency, Frequency, Monetary) analysis
- K-means clustering
- Segment profiling

### 3. Insights Generation
- Stock alerts
- Customer risk analysis
- Sales patterns
- Product performance

### 4. Automation
- Critical alerts
- Reorder recommendations
- Action items
- Priority-based notifications

## Sample Insights

- **Stock Alerts**: Low stock warnings and stockout predictions
- **Customer Insights**: At-risk customers, champions, loyalty metrics
- **Sales Patterns**: Trends, seasonality, top performers
- **Recommendations**: Reorder quantities, pricing strategies

## Configuration

Edit `.env` file to customize:
- `LOW_STOCK_THRESHOLD`: Minimum stock level for alerts
- `REORDER_POINT_MULTIPLIER`: Safety stock multiplier
- API keys for advanced AI features (optional)

## Future Enhancements

- [ ] Real-time Tally integration
- [ ] Multi-warehouse support
- [ ] Advanced pricing optimization
- [ ] Integration with ordering systems
- [ ] Mobile app
- [ ] Email/SMS notifications
- [ ] Export reports to PDF

## Support

For issues or questions, please refer to the documentation or contact support.

## License

MIT License
