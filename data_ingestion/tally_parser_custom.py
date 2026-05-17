"""
Parser for actual Tally export files:
  - Cr. party ledger.xlsx
  - purchase item wise .xlsx
  - sales .xlsx
  - sales item wise.xlsx
"""
import pandas as pd
import numpy as np
from typing import Dict, Tuple
from loguru import logger
from datetime import datetime


class TallyCustomParser:
    """Parser for actual Tally export format (multi-sheet item-wise registers)"""

    # ------------------------------------------------------------------ #
    #  Public parse methods                                                #
    # ------------------------------------------------------------------ #

    def parse_party_ledger(self, file_path) -> pd.DataFrame:
        """
        Parse Cr. party ledger.xlsx
        Each sheet = one credit party. Returns combined ledger with party_name column.
        """
        logger.info(f"Parsing party ledger: {file_path}")
        xl = pd.ExcelFile(file_path)
        frames = []
        for sheet in xl.sheet_names:
            raw = pd.read_excel(file_path, sheet_name=sheet, header=None)
            df = self._parse_ledger_sheet(raw, sheet)
            frames.append(df)
        out = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
        logger.info(f"Party ledger: {len(out)} rows, {out['party_name'].nunique()} parties")
        return out

    def parse_purchase_item_wise(self, file_path) -> pd.DataFrame:
        """
        Parse purchase item wise .xlsx
        Each sheet = one product stock register. Returns combined purchase inwards.
        """
        logger.info(f"Parsing purchase item wise: {file_path}")
        xl = pd.ExcelFile(file_path)
        frames = []
        for sheet in xl.sheet_names:
            raw = pd.read_excel(file_path, sheet_name=sheet, header=None)
            df = self._parse_stock_register(raw, sheet, direction='inwards')
            if df is not None:
                frames.append(df)
        out = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
        logger.info(f"Purchases: {len(out)} rows across {out['product_name'].nunique() if not out.empty else 0} products")
        return out

    def parse_sales(self, file_path) -> pd.DataFrame:
        """
        Parse sales .xlsx (Cash Sales Register - daily totals)
        """
        logger.info(f"Parsing sales register: {file_path}")
        xl = pd.ExcelFile(file_path)
        frames = []
        for sheet in xl.sheet_names:
            raw = pd.read_excel(file_path, sheet_name=sheet, header=None)
            df = self._parse_sales_register(raw, sheet)
            frames.append(df)
        out = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
        logger.info(f"Sales register: {len(out)} rows")
        return out

    def parse_sales_item_wise(self, file_path) -> pd.DataFrame:
        """
        Parse sales item wise.xlsx
        Each sheet = one product stock register. Returns combined sales outwards.
        """
        logger.info(f"Parsing sales item wise: {file_path}")
        xl = pd.ExcelFile(file_path)
        frames = []
        for sheet in xl.sheet_names:
            raw = pd.read_excel(file_path, sheet_name=sheet, header=None)
            df = self._parse_stock_register(raw, sheet, direction='outwards')
            if df is not None:
                frames.append(df)
        out = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
        logger.info(f"Sales item wise: {len(out)} rows across {out['product_name'].nunique() if not out.empty else 0} products")
        return out

    # ------------------------------------------------------------------ #
    #  Unified dataset builder                                             #
    # ------------------------------------------------------------------ #

    def create_unified_datasets(
        self,
        party_ledger_df: pd.DataFrame,
        purchases_df: pd.DataFrame,
        sales_df: pd.DataFrame,
        sales_item_wise_df: pd.DataFrame,
    ) -> Dict[str, pd.DataFrame]:
        """
        Build unified datasets for the analytics engine from the 4 parsed DataFrames.

        Returned keys:
          products        - one row per product with stock & price info
          customers       - one row per credit party
          transactions    - sales item-wise rows enriched for RFM / segmentation
          purchases       - cleaned purchase inwards
          sales           - daily cash sales register
          ledger          - full party ledger
        """
        logger.info("Building unified datasets...")

        # ---- products ------------------------------------------------- #
        products_df = self._build_products(purchases_df, sales_item_wise_df)

        # ---- customers (from party ledger) ---------------------------- #
        customers_df = self._build_customers(party_ledger_df)

        # ---- transactions (from sales item wise) ---------------------- #
        transactions_df = self._build_transactions(sales_item_wise_df, products_df)

        logger.info(
            f"Unified: {len(products_df)} products, "
            f"{len(customers_df)} customers, "
            f"{len(transactions_df)} transactions"
        )

        return {
            "products": products_df,
            "customers": customers_df,
            "transactions": transactions_df,
            "purchases": purchases_df,
            "sales": sales_df,
            "ledger": party_ledger_df,
        }

    # ------------------------------------------------------------------ #
    #  Sheet-level parsers                                                 #
    # ------------------------------------------------------------------ #

    def _parse_ledger_sheet(self, raw: pd.DataFrame, party_name: str) -> pd.DataFrame:
        """
        Tally ledger sheet layout:
          rows 0-8  : header / metadata
          row 9     : column labels  [Date, Particulars, ..., Vch Type, Vch No., Debit, Credit]
          row 10+   : data  (some rows are sub-detail rows with NaT date)
        """
        # Find the header row (contains 'Date')
        header_row = self._find_header_row(raw, 'Date')
        if header_row is None:
            return pd.DataFrame()

        # Assign clean column names from the header row
        cols = raw.iloc[header_row].tolist()
        data = raw.iloc[header_row + 1:].copy()
        data.columns = range(len(data.columns))

        # Map positional columns: 0=Date, 1=Particulars, 5=Vch Type, 6=Vch No, 7=Debit, 8=Credit
        col_map = {0: 'date', 1: 'particulars', 5: 'vch_type', 6: 'vch_no', 7: 'debit', 8: 'credit'}
        data = data.rename(columns=col_map)

        keep = [c for c in col_map.values() if c in data.columns]
        data = data[keep].copy()

        # Keep only rows that have a real date (main transaction rows)
        data['date'] = pd.to_datetime(data['date'], errors='coerce')
        data = data[data['date'].notna()].copy()

        # Numeric
        data['debit'] = pd.to_numeric(data['debit'], errors='coerce').fillna(0)
        data['credit'] = pd.to_numeric(data['credit'], errors='coerce').fillna(0)

        # Drop summary/closing rows
        data = data[~data['particulars'].astype(str).str.contains('Closing Balance|Opening Balance', na=False)]

        data['party_name'] = party_name
        data['customer_id'] = 'CUST_' + party_name.replace(' ', '_').upper()

        return data.reset_index(drop=True)

    def _parse_stock_register(self, raw: pd.DataFrame, product_name: str, direction: str) -> pd.DataFrame:
        """
        Stock Item Register layout (purchase item wise / sales item wise):
          rows 0-6  : metadata
          row 7     : group header  [Date, Particulars, Vch Type, Vch No., Inwards, , , Outwards, , , Closing, , ]
          row 8     : sub-header   [, , , , Qty, Rate, Value, Qty, Rate, Value, Qty, Rate, Value]
          row 9+    : data

        direction='inwards'  → purchase transactions
        direction='outwards' → sales transactions
        """
        header_row = self._find_header_row(raw, 'Date')
        if header_row is None:
            return None

        sub_header_row = header_row + 1
        data_start = sub_header_row + 1

        # Build flat column names by combining rows 7 & 8
        group_row = raw.iloc[header_row].fillna('').tolist()
        sub_row = raw.iloc[sub_header_row].fillna('').tolist()

        flat_cols = []
        current_group = ''
        for g, s in zip(group_row, sub_row):
            g = str(g).strip()
            s = str(s).strip()
            if g and g not in ('nan', ''):
                current_group = g
            if s and s not in ('nan', ''):
                flat_cols.append(f"{current_group}_{s}" if current_group else s)
            else:
                flat_cols.append(current_group if current_group else '')

        data = raw.iloc[data_start:].copy()
        data.columns = flat_cols[:len(data.columns)]

        # Rename the fixed leading columns
        rename = {}
        for i, c in enumerate(data.columns):
            if i == 0:
                rename[c] = 'date'
            elif i == 1:
                rename[c] = 'particulars'
            elif i == 2:
                rename[c] = 'vch_type'
            elif i == 3:
                rename[c] = 'vch_no'
        data = data.rename(columns=rename)

        # Parse date; keep only main transaction rows
        data['date'] = pd.to_datetime(data['date'], errors='coerce')
        data = data[data['date'].notna()].copy()

        # Drop opening/closing/totals rows
        data = data[~data['particulars'].astype(str).str.contains(
            'Opening Balance|Closing Balance|Totals as per', na=False
        )]

        if direction == 'inwards':
            qty_col = self._find_col(data, 'Inwards_Quantity', 'Inward_Quantity', 'Inwards_Qty')
            rate_col = self._find_col(data, 'Inwards_Rate', 'Inward_Rate')
            val_col = self._find_col(data, 'Inwards_Value', 'Inward_Value')
        else:
            qty_col = self._find_col(data, 'Outwards_Quantity', 'Outward_Quantity', 'Outwards_Qty')
            rate_col = self._find_col(data, 'Outwards_Rate', 'Outward_Rate')
            val_col = self._find_col(data, 'Outwards_Value', 'Outward_Value')

        data['quantity'] = pd.to_numeric(data.get(qty_col), errors='coerce').fillna(0) if qty_col else 0
        data['rate'] = pd.to_numeric(data.get(rate_col), errors='coerce').fillna(0) if rate_col else 0
        data['value'] = pd.to_numeric(data.get(val_col), errors='coerce').fillna(0) if val_col else 0

        # Only rows with actual movement
        data = data[data['quantity'] > 0].copy()

        if data.empty:
            return None

        data['product_name'] = product_name
        data['product_id'] = 'PROD_' + product_name.replace(' ', '_').upper()

        out = data[['date', 'particulars', 'vch_type', 'vch_no',
                    'quantity', 'rate', 'value', 'product_name', 'product_id']].copy()
        out['vch_no'] = out['vch_no'].astype(str)
        return out.reset_index(drop=True)

    def _parse_sales_register(self, raw: pd.DataFrame, sheet_name: str) -> pd.DataFrame:
        """
        Cash Sales Register layout:
          rows 0-5  : metadata
          row 6     : header  [Date, Particulars, Vch Type, Vch No., Debit, Credit]
          row 7     : sub     [, , , , Amount, Amount]
          row 8+    : data
        """
        header_row = self._find_header_row(raw, 'Date')
        if header_row is None:
            return pd.DataFrame()

        data = raw.iloc[header_row + 2:].copy()
        data.columns = range(len(data.columns))

        col_map = {0: 'date', 1: 'particulars', 2: 'vch_type', 3: 'vch_no', 4: 'debit', 5: 'credit'}
        data = data.rename(columns=col_map)

        data['date'] = pd.to_datetime(data['date'], errors='coerce')
        data = data[data['date'].notna()].copy()

        # Drop totals row
        data = data[~data['particulars'].astype(str).str.lower().str.startswith('total')]

        data['debit'] = pd.to_numeric(data['debit'], errors='coerce').fillna(0)
        data['credit'] = pd.to_numeric(data['credit'], errors='coerce').fillna(0)
        data['register'] = sheet_name

        return data[['date', 'particulars', 'vch_type', 'vch_no', 'debit', 'credit', 'register']].reset_index(drop=True)

    # ------------------------------------------------------------------ #
    #  Unified dataset helpers                                             #
    # ------------------------------------------------------------------ #

    def _build_products(self, purchases_df: pd.DataFrame, sales_item_wise_df: pd.DataFrame) -> pd.DataFrame:
        """One row per product derived from item-wise registers."""
        dfs = []
        for df in [purchases_df, sales_item_wise_df]:
            if not df.empty and 'product_id' in df.columns:
                dfs.append(df[['product_id', 'product_name']].drop_duplicates())

        if not dfs:
            return pd.DataFrame(columns=['product_id', 'name', 'current_stock', 'unit_price'])

        products = pd.concat(dfs).drop_duplicates('product_id').rename(columns={'product_name': 'name'})

        # Approximate current stock from last closing row per product
        # Use the most recent purchase inward qty minus outward qty as a proxy
        if not sales_item_wise_df.empty and 'product_id' in sales_item_wise_df.columns:
            sold = sales_item_wise_df.groupby('product_id')['quantity'].sum().rename('total_sold')
            products = products.merge(sold, on='product_id', how='left')
        else:
            products['total_sold'] = 0

        if not purchases_df.empty and 'product_id' in purchases_df.columns:
            bought = purchases_df.groupby('product_id')['quantity'].sum().rename('total_bought')
            avg_purchase_rate = purchases_df.groupby('product_id')['rate'].mean().rename('unit_price')
            products = products.merge(bought, on='product_id', how='left')
            products = products.merge(avg_purchase_rate, on='product_id', how='left')
        else:
            products['total_bought'] = 0
            products['unit_price'] = 0

        products['current_stock'] = (
            products['total_bought'].fillna(0) - products['total_sold'].fillna(0)
        ).clip(lower=0)

        products['unit_price'] = products['unit_price'].fillna(0)
        products['min_stock'] = (products['current_stock'] * 0.2).round(0)
        products['max_stock'] = (products['current_stock'] * 2.0).round(0)

        return products[['product_id', 'name', 'current_stock', 'min_stock', 'max_stock', 'unit_price']].reset_index(drop=True)

    def _build_customers(self, ledger_df: pd.DataFrame) -> pd.DataFrame:
        """One row per credit party from the ledger."""
        if ledger_df.empty or 'party_name' not in ledger_df.columns:
            return pd.DataFrame(columns=['customer_id', 'name', 'total_debit', 'total_credit', 'purchase_count'])

        stats = ledger_df.groupby(['customer_id', 'party_name']).agg(
            total_debit=('debit', 'sum'),
            total_credit=('credit', 'sum'),
            purchase_count=('vch_no', 'count'),
            last_purchase_date=('date', 'max'),
        ).reset_index().rename(columns={'party_name': 'name'})

        return stats.reset_index(drop=True)

    def _build_transactions(self, sales_item_wise_df: pd.DataFrame, products_df: pd.DataFrame) -> pd.DataFrame:
        """Transaction rows from sales item wise, enriched for RFM analysis."""
        if sales_item_wise_df.empty:
            return pd.DataFrame(columns=[
                'transaction_id', 'date', 'customer_id', 'customer_name',
                'product_id', 'product_name', 'quantity', 'unit_price', 'total_amount'
            ])

        txns = sales_item_wise_df.copy()

        # 'particulars' is the customer / payment mode name
        txns['customer_name'] = txns['particulars'].astype(str).str.strip()
        txns['customer_id'] = 'CUST_' + txns['customer_name'].str.replace(' ', '_').str.upper()

        txns['total_amount'] = txns['value'].fillna(txns['quantity'] * txns['rate'])
        txns['unit_price'] = txns['rate']

        txns['transaction_id'] = ['TXN{:06d}'.format(i + 1) for i in range(len(txns))]

        return txns[[
            'transaction_id', 'date', 'customer_id', 'customer_name',
            'product_id', 'product_name', 'quantity', 'unit_price', 'total_amount', 'vch_no'
        ]].reset_index(drop=True)

    # ------------------------------------------------------------------ #
    #  Utility helpers                                                     #
    # ------------------------------------------------------------------ #

    def _find_header_row(self, raw: pd.DataFrame, keyword: str) -> int | None:
        for i, row in raw.iterrows():
            if any(str(v).strip() == keyword for v in row):
                return i
        return None

    def _find_col(self, df: pd.DataFrame, *candidates: str) -> str | None:
        for c in candidates:
            if c in df.columns:
                return c
        # fuzzy: check if candidate is a substring of any column
        for c in candidates:
            for col in df.columns:
                if c.lower() in str(col).lower():
                    return col
        return None
