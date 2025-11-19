#!/usr/bin/env python3
"""
clean_transform_pipeline.py

Cleans and transforms ecommerce CSVs:
 - customers.csv
 - products.csv
 - orders.csv

Outputs:
 - clean_customers.csv
 - clean_products.csv
 - clean_orders.csv
 - basic analytics printed to console
"""

import pandas as pd
import numpy as np
from datetime import datetime, timezone
import phonenumbers         # pip install phonenumbers
import re
from decimal import Decimal, ROUND_HALF_UP
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# ---------- CONFIG ----------
CUSTOMERS_CSV = "customers.csv"
PRODUCTS_CSV = "products.csv"
ORDERS_CSV = "orders.csv"

OUT_CUSTOMERS = "clean_customers.csv"
OUT_PRODUCTS = "clean_products.csv"
OUT_ORDERS = "clean_orders.csv"

# ---------- HELPER FUNCTIONS ----------

def safe_read_csv(path, **kwargs):
    """Read CSV with common safe defaults."""
    return pd.read_csv(path, dtype=str, keep_default_na=False, na_values=["", "NA", "NaN"], **kwargs)

def normalize_email(email):
    if pd.isna(email) or str(email).strip()=="":
        return np.nan
    e = str(email).strip().lower()
    # simple normalization: remove spaces
    e = re.sub(r"\s+", "", e)
    return e

def normalize_phone(phone, default_region="IN"):
    """Try to parse & format phone with phonenumbers. Return E.164 or original cleaned."""
    if pd.isna(phone) or str(phone).strip()=="":
        return np.nan
    s = str(phone)
    # remove common punctuation
    s_clean = re.sub(r"[^\d\+]", "", s)
    try:
        p = phonenumbers.parse(s_clean, default_region)
        if phonenumbers.is_valid_number(p):
            return phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.E164)
    except Exception:
        pass
    # fallback: return digits-only if reasonably long
    digits = re.sub(r"\D", "", s)
    return digits if len(digits) >= 8 else np.nan

def parse_date_safe(val):
    if pd.isna(val) or str(val).strip()=="":
        return pd.NaT
    try:
        return pd.to_datetime(val, utc=True)
    except Exception:
        try:
            # fallback parsing with dateutil
            return pd.to_datetime(val, infer_datetime_format=True, utc=True, errors='coerce')
        except Exception:
            return pd.NaT

def money_round(x, ndigits=2):
    try:
        d = Decimal(str(x)).quantize(Decimal(f"1.{'0'*ndigits}"), rounding=ROUND_HALF_UP)
        return float(d)
    except Exception:
        return np.nan

# ---------- CLEAN CUSTOMERS ----------
def clean_customers(df):
    # Ensure IDs are integers
    df = df.copy()
    # convert customer_id to int where possible
    df['customer_id'] = pd.to_numeric(df['customer_id'], errors='coerce').astype('Int64')
    # Normalize names
    df['name'] = df['name'].astype(str).str.strip().replace({'': np.nan})
    # Normalize email and phone
    df['email'] = df['email'].apply(normalize_email)
    df['phone'] = df['phone'].apply(normalize_phone)
    # Normalize city and state
    df['city'] = df['city'].astype(str).str.title().replace({'': np.nan})
    df['state'] = df['state'].astype(str).str.title().replace({'': np.nan})
    # Parse signup_date into datetime
    df['signup_date'] = df['signup_date'].apply(parse_date_safe)
    # Drop rows with no customer_id or no name
    before = len(df)
    df = df.dropna(subset=['customer_id', 'name'])
    after = len(df)
    print(f"customers: dropped {before-after} rows without id or name")
    # Deduplicate by email if available, else by phone, else by (name+signup_date)
    # Keep the first occurrence (could be adjusted to keep most recent)
    df = df.sort_values('signup_date')  # earliest signup first (or change as needed)
    df['dup_key'] = np.where(df['email'].notna(), df['email'], 
                             np.where(df['phone'].notna(), df['phone'], df['name'] + df['signup_date'].astype(str)))
    df = df[~df.duplicated('dup_key', keep='first')].drop(columns=['dup_key'])
    # Reset index
    df = df.reset_index(drop=True)
    return df

# ---------- CLEAN PRODUCTS ----------
def clean_products(df):
    df = df.copy()
    df['product_id'] = pd.to_numeric(df['product_id'], errors='coerce').astype('Int64')
    df['product_name'] = df['product_name'].astype(str).str.strip().replace({'': np.nan})
    df['category'] = df['category'].astype(str).str.title().replace({'': np.nan})
    df['brand'] = df['brand'].astype(str).str.title().replace({'': np.nan})
    # Convert price to numeric and round
    df['price'] = pd.to_numeric(df['price'], errors='coerce').apply(money_round)
    # Stock as integer
    df['stock_quantity'] = pd.to_numeric(df['stock_quantity'], errors='coerce').astype('Int64')
    # Drop products with no id or no name
    before = len(df)
    df = df.dropna(subset=['product_id', 'product_name'])
    print(f"products: dropped {before-len(df)} rows without id or name")
    # Deduplicate by product_name or product_id
    df = df.drop_duplicates(subset=['product_id'], keep='first')
    df = df.reset_index(drop=True)
    return df

# ---------- CLEAN ORDERS ----------
def clean_orders(df, valid_customer_ids, valid_product_ids, product_prices=None):
    df = df.copy()
    df['order_id'] = pd.to_numeric(df['order_id'], errors='coerce').astype('Int64')
    df['customer_id'] = pd.to_numeric(df['customer_id'], errors='coerce').astype('Int64')
    df['product_id'] = pd.to_numeric(df['product_id'], errors='coerce').astype('Int64')
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').astype('Int64').fillna(1).astype(int)
    # Parse date/time
    # support both order_date (YYYY-MM-DD) and order_timestamp if present
    if 'order_timestamp' in df.columns:
        df['order_timestamp'] = df['order_timestamp'].apply(parse_date_safe)
    else:
        # fallback to order_date
        df['order_timestamp'] = df.get('order_date', pd.Series([None]*len(df))).apply(parse_date_safe)
    # Normalize shipping city
    df['shipping_city'] = df['shipping_city'].astype(str).str.title().replace({'': np.nan})
    # Payment method and status normalization
    df['payment_method'] = df.get('payment_method', pd.Series(['Unknown']*len(df))).astype(str).str.title()
    df['status'] = df.get('status', pd.Series(['Unknown']*len(df))).astype(str).str.title()

    # Remove orders that reference non-existent customers or products.
    before = len(df)
    df = df[df['customer_id'].isin(valid_customer_ids)]
    df = df[df['product_id'].isin(valid_product_ids)]
    after = len(df)
    print(f"orders: dropped {before-after} rows that referenced missing customers/products")

    # Compute order_value by joining product price if provided
    if product_prices is not None:
        # product_prices: dict product_id -> price
        def compute_value(row):
            pid = int(row['product_id'])
            price = product_prices.get(pid, np.nan)
            if pd.isna(price):
                return np.nan
            return money_round(price * int(row['quantity']))
        df['order_value'] = df.apply(compute_value, axis=1)
    else:
        df['order_value'] = np.nan

    # If order_timestamp missing, set to now (timezone-aware)
    df['order_timestamp'] = df['order_timestamp'].fillna(pd.to_datetime(datetime.now(timezone.utc), utc=True))
    # Sort by timestamp
    df = df.sort_values('order_timestamp').reset_index(drop=True)

    # Handle duplicates: real systems often dedupe by order_id or (customer_id, product_id, timestamp)
    df = df.drop_duplicates(subset=['order_id'], keep='first')
    df = df.reset_index(drop=True)
    return df

# ---------- ANALYTICS / CHECKS ----------
def analytics(customers_df, products_df, orders_df):
    print("\n=== Basic Analytics / Data Checks ===")
    print(f"Customers: {len(customers_df)} rows")
    print(f"Products:  {len(products_df)} rows")
    print(f"Orders:    {len(orders_df)} rows")

    # Missing prices
    missing_price_count = products_df['price'].isna().sum()
    print(f"Products with missing price: {missing_price_count}")

    # Ensure order_timestamp is datetime (safe conversion if strings)
    if 'order_timestamp' in orders_df.columns:
        try:
            orders_df['order_timestamp'] = pd.to_datetime(orders_df['order_timestamp'], utc=True, errors='coerce')
        except Exception:
            orders_df['order_timestamp'] = orders_df['order_timestamp'].apply(parse_date_safe)

    # Top 5 products by units sold / revenue (requires order_value)
    if 'order_value' in orders_df.columns and orders_df['order_value'].notna().any():
        revenue_by_product = orders_df.groupby('product_id', as_index=False).agg(
            units_sold = ('quantity', 'sum'),
            revenue = ('order_value', 'sum')
        ).sort_values('revenue', ascending=False)
        print("\nTop products by revenue (top 5):")
        top = revenue_by_product.merge(products_df[['product_id','product_name']], on='product_id', how='left')
        print(top[['product_id','product_name','units_sold','revenue']].head(5).to_string(index=False))
    else:
        print("order_value missing: cannot compute revenue-based analytics.")

    # Monthly revenue (if timestamps)
    try:
        if 'order_timestamp' in orders_df.columns and orders_df['order_timestamp'].notna().any():
            orders_df['month'] = orders_df['order_timestamp'].dt.to_period('M')
            monthly = orders_df.groupby('month', as_index=False)['order_value'].sum().sort_values('month')
            print("\nMonthly revenue (sample):")
            print(monthly.head(6).to_string(index=False))
        else:
            print("Could not compute monthly revenue (missing timestamps/order_value)")
    except Exception:
        print("Could not compute monthly revenue (missing timestamps/order_value)")

    # Top customers by lifetime value
    if 'order_value' in orders_df.columns:
        clv = orders_df.groupby('customer_id', as_index=False)['order_value'].sum().sort_values('order_value', ascending=False)
        clv_top = clv.head(5).merge(customers_df[['customer_id','name']], on='customer_id', how='left')
        print("\nTop customers by lifetime value (top 5):")
        print(clv_top[['customer_id','name','order_value']].to_string(index=False))

# ---------- MAIN EXECUTION ----------
def main():
    # 1) Load raw CSVs (strings safe)
    print("Loading CSVs...")
    raw_customers = safe_read_csv(CUSTOMERS_CSV)
    raw_products = safe_read_csv(PRODUCTS_CSV)
    raw_orders = safe_read_csv(ORDERS_CSV)

    # 2) Clean each
    print("Cleaning customers...")
    clean_cust = clean_customers(raw_customers)
    print("Cleaning products...")
    clean_prod = clean_products(raw_products)
    print("Cleaning orders...")
    prod_price_map = dict(zip(clean_prod['product_id'].astype(int), clean_prod['price']))
    clean_ord = clean_orders(raw_orders, valid_customer_ids=set(clean_cust['customer_id'].dropna().astype(int)),
                             valid_product_ids=set(clean_prod['product_id'].dropna().astype(int)),
                             product_prices=prod_price_map)

    # 3) Save cleaned outputs
    print(f"Saving cleaned CSVs: {OUT_CUSTOMERS}, {OUT_PRODUCTS}, {OUT_ORDERS} ...")
    clean_cust.to_csv(OUT_CUSTOMERS, index=False, date_format='%Y-%m-%dT%H:%M:%SZ')
    clean_prod.to_csv(OUT_PRODUCTS, index=False)

    # 4) Run analytics and checks BEFORE formatting timestamps to strings
    analytics(clean_cust, clean_prod, clean_ord)

    # Ensure order_timestamp saved as ISO string for downstream systems
    clean_ord['order_timestamp'] = pd.to_datetime(clean_ord['order_timestamp'], utc=True).dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    clean_ord.to_csv(OUT_ORDERS, index=False)

    print("\nClean & transform pipeline finished. Clean files written to current folder.")

if __name__ == "__main__":
    main()

