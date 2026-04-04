"""
Custom parser for actual Tally export files
Handles: product_wise_reports.xlsx and sample_tally_customer_report.xlsx
"""
import pandas as pd
from typing import Tuple, Dict
from loguru import logger
from datetime import datetime


class TallyCustomParser:
    """Parser for actual Tally export format"""

    def parse_product_reports(self, file_path: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Parse product_wise_reports.xlsx
        Returns: price_fluctuation_df, customer_adoption_df, stock_summary_df
        """
        logger.info(f"Parsing product reports: {file_path}")

        # Read all sheets
        price_fluctuation_df = pd.read_excel(file_path, sheet_name='Price Fluctuation')
        customer_adoption_df = pd.read_excel(file_path, sheet_name='Customer Adoption')
        stock_summary_df = pd.read_excel(file_path, sheet_name='Stock Summary')

        # Clean and standardize data
        price_fluctuation_df = self._clean_price_fluctuation(price_fluctuation_df)
        customer_adoption_df = self._clean_customer_adoption(customer_adoption_df)
        stock_summary_df = self._clean_stock_summary(stock_summary_df)

        logger.info(f"Loaded: {len(price_fluctuation_df)} price records, "
                   f"{len(customer_adoption_df)} adoption records, "
                   f"{len(stock_summary_df)} products")

        return price_fluctuation_df, customer_adoption_df, stock_summary_df

    def parse_customer_ledger(self, file_path: str) -> pd.DataFrame:
        """
        Parse sample_tally_customer_report.xlsx
        Returns: customer_ledger_df
        """
        logger.info(f"Parsing customer ledger: {file_path}")

        ledger_df = pd.read_excel(file_path, sheet_name='Customer Ledger Report')
        ledger_df = self._clean_customer_ledger(ledger_df)

        logger.info(f"Loaded: {len(ledger_df)} ledger entries")

        return ledger_df

    def _clean_price_fluctuation(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean price fluctuation data"""
        df = df.copy()

        # Convert date
        df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y', errors='coerce')

        # Remove any null rows
        df = df.dropna(subset=['Product', 'Price (₹)'])

        # Ensure price is numeric
        df['Price (₹)'] = pd.to_numeric(df['Price (₹)'], errors='coerce')

        return df

    def _clean_customer_adoption(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean customer adoption data"""
        df = df.copy()

        # Remove null rows
        df = df.dropna(subset=['Customer Name', 'Product', 'Quantity Purchased'])

        # Ensure quantity is numeric
        df['Quantity Purchased'] = pd.to_numeric(df['Quantity Purchased'], errors='coerce')

        # Create customer ID
        df['customer_id'] = df['Customer Name'].apply(
            lambda x: 'CUST_' + x.replace(' ', '_').upper()
        )

        # Create product ID
        df['product_id'] = df['Product'].apply(
            lambda x: 'PROD_' + x.replace(' ', '_').upper()
        )

        return df

    def _clean_stock_summary(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean stock summary data"""
        df = df.copy()

        # Remove null rows
        df = df.dropna(subset=['Product'])

        # Ensure numeric columns
        for col in ['Min Stock', 'Max Stock', 'Current Stock']:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # Create product ID
        df['product_id'] = df['Product'].apply(
            lambda x: 'PROD_' + x.replace(' ', '_').upper()
        )

        return df

    def _clean_customer_ledger(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean customer ledger data"""
        df = df.copy()

        # Convert date
        df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y', errors='coerce')

        # Ensure numeric columns
        for col in ['Debit (₹)', 'Credit (₹)', 'Balance (₹)']:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # Create customer ID
        df['customer_id'] = df['Customer Name'].apply(
            lambda x: 'CUST_' + x.replace(' ', '_').upper()
        )

        return df

    def create_unified_datasets(self,
                               price_df: pd.DataFrame,
                               adoption_df: pd.DataFrame,
                               stock_df: pd.DataFrame,
                               ledger_df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Transform Tally data into unified format for AI analysis
        """
        logger.info("Creating unified datasets...")

        # 1. Products DataFrame
        products_df = stock_df[['product_id', 'Product', 'Min Stock', 'Max Stock', 'Current Stock']].copy()
        products_df.columns = ['product_id', 'name', 'min_stock', 'max_stock', 'current_stock']

        # Add latest price
        latest_prices = price_df.sort_values('Date').groupby('Product').last()['Price (₹)']
        products_df['unit_price'] = products_df['name'].map(latest_prices)

        # Add category (infer from product name)
        products_df['category'] = products_df['name'].apply(self._infer_category)

        # 2. Customers DataFrame
        customer_names = set(adoption_df['Customer Name'].unique()) | set(ledger_df['Customer Name'].unique())
        customers_df = pd.DataFrame([
            {
                'customer_id': 'CUST_' + name.replace(' ', '_').upper(),
                'name': name
            }
            for name in customer_names
        ])

        # Add customer stats from ledger
        customer_stats = ledger_df.groupby('customer_id').agg({
            'Debit (₹)': 'sum',
            'Date': 'max',
            'Voucher No': 'count'
        }).reset_index()
        customer_stats.columns = ['customer_id', 'total_purchases', 'last_purchase_date', 'purchase_count']

        customers_df = customers_df.merge(customer_stats, on='customer_id', how='left')
        customers_df['total_purchases'] = customers_df['total_purchases'].fillna(0)
        customers_df['purchase_count'] = customers_df['purchase_count'].fillna(0)

        # 3. Transactions DataFrame (from customer adoption)
        transactions_df = adoption_df[['customer_id', 'product_id', 'Customer Name', 'Product', 'Quantity Purchased']].copy()

        # Rename to standard column name
        transactions_df = transactions_df.rename(columns={'Quantity Purchased': 'quantity'})

        # Add price information
        avg_prices = price_df.groupby('Product')['Price (₹)'].mean().to_dict()
        transactions_df['unit_price'] = transactions_df['Product'].map(avg_prices)
        transactions_df['total_amount'] = transactions_df['quantity'] * transactions_df['unit_price']

        # Add estimated dates (spread across ledger date range)
        if not ledger_df.empty:
            min_date = ledger_df['Date'].min()
            max_date = ledger_df['Date'].max()
            date_range = pd.date_range(start=min_date, end=max_date, periods=len(transactions_df))
            transactions_df['date'] = date_range
        else:
            transactions_df['date'] = datetime.now()

        transactions_df['transaction_id'] = [f'TXN{i:06d}' for i in range(1, len(transactions_df) + 1)]

        # 4. Time series data for forecasting
        timeseries_df = price_df.merge(
            stock_df[['product_id', 'Product', 'Current Stock']],
            on='Product',
            how='left'
        )

        logger.info(f"Created unified datasets: "
                   f"{len(products_df)} products, "
                   f"{len(customers_df)} customers, "
                   f"{len(transactions_df)} transactions")

        return {
            'products': products_df,
            'customers': customers_df,
            'transactions': transactions_df,
            'timeseries': timeseries_df,
            'ledger': ledger_df
        }

    def _infer_category(self, product_name: str) -> str:
        """Infer product category from name"""
        name_lower = product_name.lower()

        if 'rice' in name_lower:
            return 'Grains'
        elif 'oil' in name_lower:
            return 'Oils'
        elif 'wheat' in name_lower or 'flour' in name_lower:
            return 'Grains'
        elif 'dal' in name_lower or 'lentil' in name_lower:
            return 'Pulses'
        elif 'sugar' in name_lower or 'salt' in name_lower:
            return 'Condiments'
        else:
            return 'General'
