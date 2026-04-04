"""
Parse Tally exports (Excel/XML) into structured data
"""
import pandas as pd
import xmltodict
from pathlib import Path
from typing import Dict, List, Tuple
from loguru import logger
from models.schemas import CustomerData, ProductData, Transaction


class TallyParser:
    """Parser for Tally export files"""

    def __init__(self):
        self.customers: List[CustomerData] = []
        self.products: List[ProductData] = []
        self.transactions: List[Transaction] = []

    def parse_excel(self, file_path: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Parse Excel file exported from Tally
        Expected sheets: 'Customers', 'Products', 'Transactions'
        """
        try:
            excel_file = pd.ExcelFile(file_path)
            logger.info(f"Reading Excel file: {file_path}")
            logger.info(f"Available sheets: {excel_file.sheet_names}")

            # Parse customer data
            customers_df = None
            if 'Customers' in excel_file.sheet_names:
                customers_df = pd.read_excel(file_path, sheet_name='Customers')
                customers_df = self._clean_dataframe(customers_df)
                logger.info(f"Loaded {len(customers_df)} customers")

            # Parse product data
            products_df = None
            if 'Products' in excel_file.sheet_names:
                products_df = pd.read_excel(file_path, sheet_name='Products')
                products_df = self._clean_dataframe(products_df)
                logger.info(f"Loaded {len(products_df)} products")

            # Parse transaction data
            transactions_df = None
            if 'Transactions' in excel_file.sheet_names:
                transactions_df = pd.read_excel(file_path, sheet_name='Transactions')
                transactions_df = self._clean_dataframe(transactions_df)
                logger.info(f"Loaded {len(transactions_df)} transactions")

            return customers_df, products_df, transactions_df

        except Exception as e:
            logger.error(f"Error parsing Excel: {e}")
            raise

    def parse_xml(self, file_path: str) -> Dict:
        """Parse XML file exported from Tally"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                xml_content = f.read()

            data = xmltodict.parse(xml_content)
            logger.info(f"Parsed XML file: {file_path}")
            return data

        except Exception as e:
            logger.error(f"Error parsing XML: {e}")
            raise

    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize dataframe"""
        # Remove empty rows
        df = df.dropna(how='all')

        # Strip whitespace from column names
        df.columns = df.columns.str.strip()

        # Convert date columns
        date_columns = ['date', 'last_purchase_date', 'last_restock_date', 'transaction_date']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        return df

    def validate_data(self, customers_df: pd.DataFrame,
                     products_df: pd.DataFrame,
                     transactions_df: pd.DataFrame) -> Dict[str, List[str]]:
        """Validate parsed data and return issues"""
        issues = {
            'customers': [],
            'products': [],
            'transactions': []
        }

        # Validate customers
        if customers_df is not None:
            required_customer_cols = ['customer_id', 'name']
            missing_cols = [col for col in required_customer_cols if col not in customers_df.columns]
            if missing_cols:
                issues['customers'].append(f"Missing columns: {missing_cols}")

        # Validate products
        if products_df is not None:
            required_product_cols = ['product_id', 'name', 'current_stock']
            missing_cols = [col for col in required_product_cols if col not in products_df.columns]
            if missing_cols:
                issues['products'].append(f"Missing columns: {missing_cols}")

        # Validate transactions
        if transactions_df is not None:
            required_transaction_cols = ['transaction_id', 'date', 'customer_id', 'product_id', 'quantity']
            missing_cols = [col for col in required_transaction_cols if col not in transactions_df.columns]
            if missing_cols:
                issues['transactions'].append(f"Missing columns: {missing_cols}")

        return issues
